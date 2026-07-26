<script setup lang="ts">
import { computed, ref } from 'vue';
import DataTable, {
  type DataTableColumn,
} from '@/components/DataTable.vue';
import MetricCard from '../MetricCard.vue';
import { useEstimationStore } from '../../stores/estimation';

const estimation = useEstimationStore();

const metrics = computed(() => [
  { label: 'RMSE', value: estimation.rmse.toFixed(6) },
  { label: 'Fit', value: estimation.fit == null ? '--' : estimation.fit.toFixed(6) },
  { label: 'Cost', value: estimation.cost.toFixed(6) },
  { label: 'Iterations', value: String(estimation.iterations) },
]);

// Scalar parameters 表（容器-7，与迭代历史同构，列名按设计稿原样）
// TODO: 设计稿后 5 列列名均为 K_brake（疑复制未改），按原稿保留待确认
const columns: DataTableColumn[] = [
  { key: 'step', title: 'Step', width: 48 },
  { key: 'cost', title: 'Cost' },
  { key: 'ki', title: 'Ki' },
  { key: 'kp', title: 'Kp' },
  { key: 'tau', title: 'Tau' },
  { key: 'wn', title: 'wn' },
  { key: 'kBrake1', title: 'K_brake' },
  { key: 'kBrake2', title: 'K_brake' },
  { key: 'kBrake3', title: 'K_brake' },
  { key: 'kBrake4', title: 'K_brake' },
  { key: 'kBrake5', title: 'K_brake' },
];

// 设计稿基准态：第 6 行（下标 5）选中
const selectedIndex = ref(5);
</script>

<template>
  <div class="report">
    <div class="report__metrics">
      <MetricCard
        v-for="metric in metrics"
        :key="metric.label"
        :label="metric.label"
        :value="metric.value"
      />
    </div>
    <h3 class="report__section-title">Scalar parameters</h3>
    <DataTable
      class="report__table"
      :columns="columns"
      :rows="estimation.iterationHistory"
      :selected-index="selectedIndex"
      row-key="step"
      @select="selectedIndex = $event"
    />
    <p class="report__message">{{ estimation.reportMessage }}</p>
  </div>
</template>

<style scoped>
.report {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-base);
  height: 100%;
  padding: var(--spacing-base);
  box-sizing: border-box;
  overflow-y: auto;
}

.report__metrics {
  display: flex;
  align-items: stretch;
  flex: none;
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

.report__section-title {
  margin: 0;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-regular);
  color: var(--color-text-muted);
}

.report__table {
  flex: 1;
  min-height: 0;
}

.report__message {
  flex: none;
  margin: 0;
  padding: var(--spacing-sm) var(--spacing-base);
  background: var(--color-surface);
  border-radius: var(--radius-base);
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  white-space: pre-line;
}
</style>

<script setup lang="ts">
import { ref } from 'vue';
import DataTable, {
  type DataTableColumn,
} from '@/components/DataTable.vue';
import { useEstimationStore } from '../../stores/estimation';

const estimation = useEstimationStore();

const columns: DataTableColumn[] = [
  { key: 'parameter', title: 'Parameter' },
  { key: 'dSseTrain', title: 'ΔSSE (train)' },
  { key: 'dSseValidation', title: 'ΔSSE (validation)' },
  { key: 'dSseTotal', title: 'ΔSSE (total)' },
];

function summary(p: { train: number; validation: number; total: number }): string {
  return `(Train=${p.train}, Validation=${p.validation}, Total=${p.total})`;
}

// 容器-9 设计稿中两张表的 tau_brake 行（下标 5）均高亮
const initialSelected = ref(5);
const bestSelected = ref(5);
</script>

<template>
  <div class="sensitivity">
    <p class="sensitivity__ratio">
      Perturbation ratio: {{ estimation.perturbationRatio }}
    </p>

    <section class="sensitivity__block">
      <h3 class="sensitivity__title">
        Initial point
        <span class="sensitivity__summary">{{ summary(estimation.initialPoint) }}</span>
      </h3>
      <DataTable
        class="sensitivity__table"
        :columns="columns"
        :rows="estimation.sensitivityRows"
        :selected-index="initialSelected"
        row-key="parameter"
        @select="initialSelected = $event"
      />
    </section>

    <section class="sensitivity__block">
      <h3 class="sensitivity__title">
        Best point
        <span class="sensitivity__summary">{{ summary(estimation.bestPoint) }}</span>
      </h3>
      <DataTable
        class="sensitivity__table"
        :columns="columns"
        :rows="estimation.sensitivityRows"
        :selected-index="bestSelected"
        row-key="parameter"
        @select="bestSelected = $event"
      />
    </section>
  </div>
</template>

<style scoped>
.sensitivity {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-base);
  height: 100%;
  padding: var(--spacing-base);
  box-sizing: border-box;
  overflow-y: auto;
}

.sensitivity__ratio {
  flex: none;
  margin: 0;
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
}

.sensitivity__block {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  padding: var(--spacing-base);
  background: var(--color-surface);
  border-radius: var(--radius-base);
}

.sensitivity__title {
  flex: none;
  margin: 0;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
}

.sensitivity__summary {
  margin-left: var(--spacing-sm);
  font-weight: var(--font-weight-regular);
  color: var(--color-text-muted);
}

.sensitivity__table {
  flex: 1;
  min-height: 0;
}
</style>

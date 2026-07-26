<script setup lang="ts">
import { computed, ref } from 'vue';
import DataTable, {
  type DataTableColumn,
} from '@/components/DataTable.vue';
import AppSelect from '@/components/AppSelect.vue';
import AppButton from '@/components/AppButton.vue';
import ChartPlaceholder from '@/components/ChartPlaceholder.vue';
import { useEstimationStore } from '../../stores/estimation';
import { useDatasetStore } from '../../stores/dataset';

const estimation = useEstimationStore();
const dataset = useDatasetStore();

// Result 下拉 ×2（容器-10；两个下拉的差异待确认）
// TODO: 交互待确认 —— 两个 Result 下拉各自语义（对比基准 vs 编辑对象？）无画板佐证
const resultOptions = computed(() =>
  estimation.results.map((r) => {
    const v = r.name.replace(' ', '');
    return { label: v, value: v };
  }),
);
const resultA = ref('Result#1');
const resultB = ref('Result#1');

const columns: DataTableColumn[] = [
  { key: 'parameter', title: 'Parameter' },
  { key: 'value', title: 'Value' },
  { key: 'initial', title: 'Initial' },
  { key: 'lower', title: 'Lower' },
  { key: 'upper', title: 'Upper' },
];

// 容器-10 设计稿中 tau_brake 行（下标 5）高亮
const selectedIndex = ref(5);

/** TODO: 交互待确认 —— Reset/Evaluate/Save 确切行为无画板佐证，暂为占位 */
function noop(): void {
  /* placeholder */
}

// Cost companies 子 Tab（容器-10：Total Cost 激活）
const costTabs = ['Total Cost', 'Dataset', 'Output'] as const;
const activeCostTab = ref<(typeof costTabs)[number]>('Total Cost');

// Output curves 头部两个下拉（数据集文件 / 信号）
const curveDataset = ref('no_drive_reference_cropped_stop');
const curveSignal = ref('v_hat_kmh');
const datasetOptions = computed(() =>
  dataset.datasetFiles.map((f) => ({ label: f, value: f })),
);
const signalOptions = [
  { label: 'v_hat_kmh', value: 'v_hat_kmh' },
  { label: 'ax_motion', value: 'ax_motion' },
  { label: 'pitch_hat', value: 'pitch_hat' },
];

// TODO: 图表库 —— mock 曲线，接入图表库后渲染
const decay = (offset: number): number[] =>
  Array.from({ length: 20 }, (_, i) =>
    Number((3.5 * Math.exp(-i / 2.2) + offset).toFixed(3)),
  );
</script>

<template>
  <div class="manual">
    <div class="manual__toolbar">
      <AppSelect v-model:value="resultA" :options="resultOptions" />
      <AppSelect v-model:value="resultB" :options="resultOptions" />
      <span class="manual__spacer" />
      <AppButton @click="noop">Reset</AppButton>
      <AppButton type="primary" @click="noop">Evaluate</AppButton>
      <AppButton @click="noop">Save</AppButton>
    </div>

    <DataTable
      class="manual__table"
      :columns="columns"
      :rows="estimation.manualParams"
      :selected-index="selectedIndex"
      row-key="parameter"
      @select="selectedIndex = $event"
    />

    <div class="manual__bottom">
      <section class="manual__cost">
        <header class="manual__cost-header">
          <h3 class="manual__card-title">Cost companies</h3>
          <nav class="manual__cost-tabs">
            <button
              v-for="tab in costTabs"
              :key="tab"
              type="button"
              class="manual__cost-tab"
              :class="{ 'is-active': activeCostTab === tab }"
              @click="activeCostTab = tab"
            >
              {{ tab }}
            </button>
          </nav>
        </header>
        <ul class="manual__cost-list">
          <li
            v-for="(item, i) in estimation.costItems"
            :key="i"
            class="manual__cost-row"
          >
            <span>{{ item.label }}</span>
            <span class="manual__cost-value">{{ item.text }}</span>
          </li>
        </ul>
      </section>

      <ChartPlaceholder
        class="manual__chart"
        title="Output curves"
        :legends="[
          { label: 'v_hat_kmh(Measured)', color: 'var(--color-success)' },
          { label: 'v_hat_kmh(Auto result)', color: 'var(--color-info)' },
          { label: 'v_hat_kmh(Manual draft)', color: 'var(--color-danger)' },
        ]"
        :series="[
          { name: 'Measured', data: decay(0) },
          { name: 'Auto result', data: decay(0.02) },
          { name: 'Manual draft', data: decay(-0.02) },
        ]"
      >
        <template #toolbar>
          <AppSelect v-model:value="curveDataset" :options="datasetOptions" />
          <AppSelect v-model:value="curveSignal" :options="signalOptions" />
        </template>
      </ChartPlaceholder>
    </div>
  </div>
</template>

<style scoped>
.manual {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-base);
  height: 100%;
  padding: var(--spacing-base);
  box-sizing: border-box;
  overflow-y: auto;
}

.manual__toolbar {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex: none;
}

.manual__spacer {
  flex: 1;
}

.manual__table {
  flex: 1;
  min-height: 0;
}

.manual__bottom {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-base);
  flex: none;
  min-height: 260px;
}

.manual__cost {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  padding: var(--spacing-base);
  background: var(--color-surface);
  border-radius: var(--radius-base);
}

.manual__cost-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-base);
}

.manual__card-title {
  margin: 0;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
}

.manual__cost-tabs {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.manual__cost-tab {
  position: relative;
  padding: var(--spacing-xs) 0;
  border: none;
  background: transparent;
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  cursor: pointer;
}

.manual__cost-tab.is-active {
  color: var(--color-primary);
  font-weight: var(--font-weight-bold);
}

.manual__cost-tab.is-active::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 2px;
  background: var(--color-primary);
}

.manual__cost-list {
  flex: 1;
  margin: 0;
  padding: 0;
  list-style: none;
  overflow-y: auto;
}

.manual__cost-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-base);
  padding: var(--spacing-sm) 0;
  font-size: var(--font-size-base);
  color: var(--color-text);
}

.manual__cost-value {
  color: var(--color-text-secondary);
}
</style>

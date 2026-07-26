<script setup lang="ts">
import { ref } from 'vue';
import ChartPlaceholder from '@/components/ChartPlaceholder.vue';
import DataTable, {
  type DataTableColumn,
} from '@/components/DataTable.vue';
import AppSelect from '@/components/AppSelect.vue';
import AppCheckbox from '@/components/AppCheckbox.vue';
import { useEstimationStore } from '../../stores/estimation';

const estimation = useEstimationStore();

// 数据表 11 列（容器-2）
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

const showScaled = ref(false);
/** TODO: 交互待确认 —— "+5" 下拉候选项无画板证据，默认实现为追加参数曲线 */
const extraParam = ref('+5');
const extraParamOptions = [{ label: '+5', value: '+5' }];

// TODO: 图表库 —— 曲线为 mock 序列，接入图表库后渲染
const costSeries = [40, 32, 26, 20, 15, 11, 8, 6, 4, 3, 2.4, 2, 1.7, 1.5, 1.3, 1.2, 1.1, 1, 0.95, 0.9];
const gradientNormSeries = [1.8, 1.5, 1.2, 0.95, 0.72, 0.55, 0.42, 0.3, 0.22, 0.15, 0.1, 0.07, 0.05, 0.04, 0.03, 0.025, 0.02, 0.015, 0.012, 0.01];
const kpSeries = [52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41.5, 41, 40.5, 40, 39.5, 39, 38.8, 38.5, 38];
const klSeries = [170, 165, 160, 155, 150, 145, 140, 136, 132, 128, 124, 120, 117, 114, 111, 108, 106, 105, 104, 105];
const tauSeries = [155, 152, 149, 146, 143, 140, 137, 134, 131, 128, 125, 122, 119, 116, 113, 110, 107, 104, 101, 100];
</script>

<template>
  <div class="convergence">
    <div class="convergence__charts">
      <ChartPlaceholder
        title="Convergence Monitor"
        :legends="[{ label: 'Cost' }, { label: 'Gradient norm' }]"
        :series="[
          { name: 'Cost', data: costSeries },
          { name: 'Gradient norm', data: gradientNormSeries },
        ]"
      />
      <ChartPlaceholder
        title="Convergence Monitor"
        :legends="[
          { label: 'kp' },
          { label: 'kl', color: 'var(--color-success)' },
          { label: 'tau' },
        ]"
        :series="[
          { name: 'kp', data: kpSeries },
          { name: 'kl', data: klSeries },
          { name: 'tau', data: tauSeries },
        ]"
      >
        <template #toolbar>
          <AppSelect v-model:value="extraParam" :options="extraParamOptions" />
          <AppCheckbox v-model:checked="showScaled" label="Show scaled parameters" />
        </template>
      </ChartPlaceholder>
    </div>
    <DataTable
      class="convergence__table"
      :columns="columns"
      :rows="estimation.iterationHistory"
      :selected-index="selectedIndex"
      row-key="step"
      @select="selectedIndex = $event"
    />
  </div>
</template>

<style scoped>
.convergence {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-base);
  height: 100%;
  padding: var(--spacing-base);
  box-sizing: border-box;
  overflow-y: auto;
}

.convergence__charts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-base);
  flex: none;
}

.convergence__table {
  flex: 1;
  min-height: 0;
}
</style>

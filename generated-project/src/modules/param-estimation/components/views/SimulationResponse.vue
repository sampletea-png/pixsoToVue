<script setup lang="ts">
import { computed } from 'vue';
import ChartPlaceholder from '@/components/ChartPlaceholder.vue';
import AppSelect from '@/components/AppSelect.vue';
import { useDatasetStore } from '../../stores/dataset';

const dataset = useDatasetStore();

const options = computed(() =>
  dataset.datasetFiles.map((f) => ({ label: f, value: f })),
);

// 图例与标题按容器-8 原稿；两图的 T2(measured) 曲线为绿色
const inputLegends = [
  { label: 'T1(Measure)' },
  { label: 'T2(measured)', color: 'var(--color-success)' },
  { label: 'v_init_kmh(measured)' },
];
const signalLegends = [
  { label: 'v_hatkmh(measured)' },
  { label: 'T2(measured)', color: 'var(--color-success)' },
  { label: 'v_init_kmh(measured)' },
];

// TODO: 图表库 —— mock 曲线，接入图表库后渲染
const mock = (n: number, base: number, amp: number): number[] =>
  Array.from({ length: n }, (_, i) =>
    Number((base + amp * Math.sin(i / 2)).toFixed(2)),
  );
</script>

<template>
  <div class="simulation">
    <div class="simulation__picker">
      <span class="simulation__label">Dataset</span>
      <AppSelect
        v-model:value="dataset.currentDataset"
        :options="options"
        class="simulation__select"
      />
    </div>
    <ChartPlaceholder
      title="Simulation input curves"
      :legends="inputLegends"
      :series="[
        { name: 'T1(Measure)', data: mock(24, 0, 800) },
        { name: 'T2(measured)', data: mock(24, -200, 500) },
        { name: 'v_init_kmh(measured)', data: mock(24, 3, 2) },
      ]"
    />
    <!-- TODO: 设计稿图表标题原文 "Signal curve·v_hat_kmh"（间隔号），按原稿保留 -->
    <ChartPlaceholder
      title="Signal curve·v_hat_kmh"
      :legends="signalLegends"
      :series="[
        { name: 'v_hatkmh(measured)', data: mock(24, 3, 2.5) },
        { name: 'T2(measured)', data: mock(24, -200, 500) },
        { name: 'v_init_kmh(measured)', data: mock(24, 3, 2) },
      ]"
    />
  </div>
</template>

<style scoped>
.simulation {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-base);
  height: 100%;
  padding: var(--spacing-base);
  box-sizing: border-box;
  overflow-y: auto;
}

.simulation__picker {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex: none;
}

.simulation__label {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
}

.simulation__select {
  min-width: 280px;
}

.simulation :deep(.chart-placeholder) {
  flex: 1;
  min-height: 0;
}
</style>

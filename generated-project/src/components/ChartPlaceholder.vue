<script lang="ts">
export interface ChartLegend {
  label: string;
  /** 图例色点颜色；缺省按 tokens 调色板循环 */
  color?: string;
}

export interface ChartSeries {
  name: string;
  data: number[];
}
</script>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    title?: string;
    legends?: ChartLegend[];
    /** TODO: 图表库 —— 曲线数据已透传，待接入图表库（如 ECharts）后渲染 */
    series?: ChartSeries[];
  }>(),
  {
    title: '',
    legends: () => [],
    series: () => [],
  },
);

/** 图例默认色循环（取自 tokens 图表色板） */
const PALETTE = [
  'var(--color-info)',
  'var(--color-danger)',
  'var(--color-warning)',
  'var(--color-success)',
  'var(--color-primary)',
];

const normalizedLegends = computed<Array<Required<ChartLegend>>>(() =>
  props.legends.map((l, i) => ({
    label: l.label,
    color: l.color ?? PALETTE[i % PALETTE.length],
  })),
);
</script>

<template>
  <section class="chart-placeholder">
    <header class="chart-placeholder__header">
      <span v-if="title" class="chart-placeholder__title">{{ title }}</span>
      <div class="chart-placeholder__legends">
        <span
          v-for="legend in normalizedLegends"
          :key="legend.label"
          class="chart-placeholder__legend"
        >
          <i
            class="chart-placeholder__dot"
            :style="{ backgroundColor: legend.color }"
          />
          {{ legend.label }}
        </span>
      </div>
      <div v-if="$slots.toolbar" class="chart-placeholder__toolbar">
        <slot name="toolbar" />
      </div>
    </header>
    <div class="chart-placeholder__body">
      <!-- TODO: 图表库 —— 待用户确认后引入（候选 ECharts），渲染 series 折线 -->
      <span class="chart-placeholder__text">Chart placeholder</span>
    </div>
  </section>
</template>

<style scoped>
.chart-placeholder {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  padding: var(--spacing-base);
  background: var(--color-surface);
  border-radius: var(--radius-base);
  font-size: var(--font-size-base);
  color: var(--color-text);
}

.chart-placeholder__header {
  display: flex;
  align-items: center;
  gap: var(--spacing-base);
}

.chart-placeholder__title {
  flex: none;
  font-weight: var(--font-weight-bold);
}

.chart-placeholder__legends {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  min-width: 0;
}

.chart-placeholder__legend {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  color: var(--color-text-secondary);
  white-space: nowrap;
}

.chart-placeholder__dot {
  flex: none;
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.chart-placeholder__toolbar {
  flex: none;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.chart-placeholder__body {
  flex: 1;
  min-height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px dashed var(--color-border-strong);
  border-radius: var(--radius-base);
  background: var(--color-bg-subtle);
}

.chart-placeholder__text {
  color: var(--color-text-muted);
}
</style>

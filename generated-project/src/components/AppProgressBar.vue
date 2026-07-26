<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  /** 0–100 */
  percent: number;
}>();

const clamped = computed<number>(() =>
  Math.min(100, Math.max(0, props.percent)),
);
</script>

<template>
  <div
    class="app-progress"
    role="progressbar"
    :aria-valuenow="clamped"
    aria-valuemin="0"
    aria-valuemax="100"
  >
    <div class="app-progress__fill" :style="{ width: `${clamped}%` }" />
  </div>
</template>

<style scoped>
/* 状态栏进度条：默认 200×4 */
.app-progress {
  width: 200px;
  height: 4px;
  border-radius: var(--radius-sm);
  background: var(--color-border);
  overflow: hidden;
}

.app-progress__fill {
  height: 100%;
  border-radius: var(--radius-sm);
  background: var(--color-primary);
  transition: width 0.2s ease;
}
</style>

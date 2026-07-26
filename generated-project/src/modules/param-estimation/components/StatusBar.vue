<script setup lang="ts">
import AppProgressBar from '@/components/AppProgressBar.vue';
import { useEstimationStore } from '../stores/estimation';

const estimation = useEstimationStore();
</script>

<template>
  <footer class="status-bar">
    <div class="status-bar__left">
      <span class="status-bar__label">Run</span>
      <span class="status-bar__value">{{ estimation.runState }}</span>
      <span class="status-bar__divider" />
      <span class="status-bar__value">Iteration: {{ estimation.iteration }}</span>
      <span class="status-bar__divider" />
      <span class="status-bar__value">Step: {{ estimation.step }}</span>
    </div>
    <div class="status-bar__right">
      <span class="status-bar__label">Algorithm progress</span>
      <AppProgressBar :percent="estimation.progress" />
      <!-- TODO: 设计稿原文 "competed Iteration 69"（疑 completed 笔误），按原稿保留 -->
      <span class="status-bar__value"
        >competed Iteration {{ estimation.completedIteration }}</span
      >
    </div>
  </footer>
</template>

<style scoped>
.status-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 28px;
  padding: 0 var(--spacing-base);
  background: var(--color-bg);
  border-top: 1px solid var(--color-border);
  font-size: var(--font-size-base);
}

.status-bar__left,
.status-bar__right {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.status-bar__label {
  color: var(--color-text-muted);
}

.status-bar__value {
  color: var(--color-text-secondary);
}

.status-bar__divider {
  width: 1px;
  height: 12px;
  background: var(--color-border-strong);
}
</style>

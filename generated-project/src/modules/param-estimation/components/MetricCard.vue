<script setup lang="ts">
defineProps<{
  label: string;
  /** 展示值（已格式化，如 "0.768418" / "--"） */
  value: string;
}>();
</script>

<template>
  <div class="metric-cell">
    <span class="metric-cell__label">{{ label }}</span>
    <span class="metric-cell__value">{{ value }}</span>
  </div>
</template>

<style scoped>
.metric-cell {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-base);
}

/* 单元格间 1px 竖分隔线（首格除外） */
.metric-cell + .metric-cell {
  border-left: 1px solid var(--color-border-strong);
}

.metric-cell__label {
  font-size: var(--font-size-base);
  color: var(--color-text-muted);
}

.metric-cell__value {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
}
</style>

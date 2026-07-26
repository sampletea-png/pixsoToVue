<script setup lang="ts">
import IconButton from '@/components/IconButton.vue';
import { useUiStore } from '../stores/ui';

const ui = useUiStore();
</script>

<template>
  <header class="title-bar">
    <div class="title-bar__brand">
      <!-- TODO: logo —— 设计稿为 BEH 渐变矢量 LOGO，暂用色块+文字占位 -->
      <span class="title-bar__logo">BEH</span>
      <h1 class="title-bar__title">Param Estimation Toolbox - HAS Behavior</h1>
    </div>
    <div class="title-bar__controls">
      <!-- TODO: 桌面窗口 min/max 在 Web 端无真实语义，仅作视觉装饰 -->
      <IconButton icon="minimize" />
      <IconButton icon="maximize" />
      <IconButton icon="close" @click="ui.closeToolboxVisible = true" />
    </div>
  </header>
</template>

<style scoped>
.title-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 32px;
  padding: 0 var(--spacing-base);
  background: var(--color-bg);
}

.title-bar__brand {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  min-width: 0;
}

.title-bar__logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: var(--radius-base);
  background: var(--color-primary);
  color: var(--color-surface);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-bold);
  transform: scale(0.9);
}

.title-bar__title {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.title-bar__controls {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}
</style>

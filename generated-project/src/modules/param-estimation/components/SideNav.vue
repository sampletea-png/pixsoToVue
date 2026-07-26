<script setup lang="ts">
import AppIcon from '@/components/AppIcon.vue';
import { useUiStore, type NavKey } from '../stores/ui';

const ui = useUiStore();

const navItems: Array<{ key: NavKey; label: string; icon: string }> = [
  { key: 'parameters', label: 'Parameters', icon: 'tuning' },
  { key: 'ports', label: 'Ports', icon: 'simulation' },
  { key: 'datasets', label: 'Datasets', icon: 'chart' },
  { key: 'results', label: 'EstimateResults', icon: 'refresh' },
];
</script>

<template>
  <nav class="side-nav">
    <button
      v-for="item in navItems"
      :key="item.key"
      type="button"
      class="side-nav__item"
      :class="{ 'is-active': ui.activeNav === item.key }"
      @click="ui.setNav(item.key)"
    >
      <AppIcon :name="item.icon" :size="16" />
      <span class="side-nav__label">{{ item.label }}</span>
    </button>
  </nav>
</template>

<style scoped>
.side-nav {
  display: flex;
  flex-direction: column;
  width: 56px;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
}

.side-nav__item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) 0;
  border: none;
  background: transparent;
  color: var(--color-icon);
  cursor: pointer;
}

.side-nav__item:hover {
  background: var(--color-bg-subtle);
}

/* 激活态左侧蓝色竖条 */
.side-nav__item.is-active {
  color: var(--color-primary);
}

.side-nav__item.is-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--color-primary);
}

/* 竖排文字（设计稿为旋转竖排） */
.side-nav__label {
  writing-mode: vertical-rl;
  font-size: var(--font-size-base);
  white-space: nowrap;
}
</style>

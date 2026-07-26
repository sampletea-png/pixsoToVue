<script setup lang="ts">
import AppIcon from '@/components/AppIcon.vue';
import { useUiStore, type TabKey } from '../stores/ui';

const ui = useUiStore();

const tabs: Array<{ key: TabKey; label: string; icon: string }> = [
  { key: 'convergence', label: 'Convergence Monitor', icon: 'chart' },
  { key: 'report', label: 'Report', icon: 'report' },
  { key: 'simulation', label: 'Simulation response', icon: 'simulation' },
  { key: 'sensitivity', label: 'Parameter Sensitivity', icon: 'sensitivity' },
  { key: 'manual', label: 'Manual tuning', icon: 'tuning' },
];
</script>

<template>
  <div class="main-tabs">
    <button
      v-for="tab in tabs"
      :key="tab.key"
      type="button"
      class="main-tabs__tab"
      :class="{ 'is-active': ui.activeTab === tab.key }"
      @click="ui.setTab(tab.key)"
    >
      <AppIcon :name="tab.icon" :size="16" />
      <span>{{ tab.label }}</span>
    </button>
  </div>
</template>

<style scoped>
.main-tabs {
  display: flex;
  align-items: stretch;
  height: 36px;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  overflow-x: auto;
}

.main-tabs__tab {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 0 var(--spacing-md);
  border: none;
  background: transparent;
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  cursor: pointer;
  white-space: nowrap;
}

.main-tabs__tab:hover {
  color: var(--color-text);
}

/* 激活态底部蓝条 */
.main-tabs__tab.is-active {
  color: var(--color-primary);
  font-weight: var(--font-weight-bold);
}

.main-tabs__tab.is-active::after {
  content: '';
  position: absolute;
  left: var(--spacing-sm);
  right: var(--spacing-sm);
  bottom: 0;
  height: 2px;
  background: var(--color-primary);
}
</style>

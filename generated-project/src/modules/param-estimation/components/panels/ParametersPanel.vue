<script setup lang="ts">
import IconButton from '@/components/IconButton.vue';
import { useUiStore } from '../../stores/ui';
import { useEstimationStore } from '../../stores/estimation';

const ui = useUiStore();
const estimation = useEstimationStore();
</script>

<template>
  <section class="panel">
    <header class="panel__header">
      <span class="panel__title">Parameters</span>
      <IconButton icon="edit" @click="ui.parametersVisible = true" />
    </header>
    <div class="panel__columns">
      <span>NAME</span>
      <span>Current Value</span>
    </div>
    <ul class="panel__list">
      <li
        v-for="(param, i) in estimation.parameters"
        :key="i"
        class="panel__row"
        :class="{ 'is-selected': ui.selectedParamIndex === i }"
        @click="ui.selectedParamIndex = i"
      >
        <span class="panel__name">{{ param.name }}</span>
        <span class="panel__value">{{ param.currentValue }}</span>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  font-size: var(--font-size-base);
  color: var(--color-text);
}

.panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-sm) var(--spacing-base);
}

.panel__title {
  font-weight: var(--font-weight-bold);
}

.panel__columns {
  display: flex;
  justify-content: space-between;
  padding: var(--spacing-xs) var(--spacing-base);
  color: var(--color-text-muted);
  border-bottom: 1px solid var(--color-border);
}

.panel__list {
  flex: 1;
  margin: 0;
  padding: 0;
  list-style: none;
  overflow-y: auto;
}

.panel__row {
  display: flex;
  justify-content: space-between;
  padding: var(--spacing-sm) var(--spacing-base);
  cursor: pointer;
}

.panel__row:nth-child(even) {
  background: var(--color-bg-subtle);
}

.panel__row:hover,
.panel__row.is-selected {
  background: var(--color-primary-light);
}

.panel__value {
  color: var(--color-text-secondary);
}
</style>

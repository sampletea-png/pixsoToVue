<script setup lang="ts">
import AppCheckbox from '@/components/AppCheckbox.vue';
import IconButton from '@/components/IconButton.vue';
import { useUiStore } from '../../stores/ui';
import { useDatasetStore } from '../../stores/dataset';

const ui = useUiStore();
const dataset = useDatasetStore();

function openWorkspace(index: number): void {
  ui.selectedDatasetIndex = index;
  ui.datasetWorkspaceVisible = true;
}

/** TODO: 交互待确认 —— 删除是否需二次确认无画板佐证，暂直接移除 */
function removeDataset(index: number): void {
  dataset.datasets.splice(index, 1);
}
</script>

<template>
  <section class="panel">
    <header class="panel__header">
      <span class="panel__title">Datasets</span>
      <span class="panel__actions">
        <!-- TODO: 交互待确认 —— 面板头部删除/导出按钮行为无画板佐证 -->
        <IconButton icon="delete" />
        <IconButton icon="export" />
      </span>
    </header>
    <div class="panel__columns">
      <span class="panel__col-name">NAME</span>
      <span>Fit</span>
      <span>Validate</span>
      <span class="panel__col-ops" />
    </div>
    <ul class="panel__list">
      <li
        v-for="(item, i) in dataset.datasets"
        :key="item.name"
        class="panel__row"
        :class="{ 'is-selected': ui.selectedDatasetIndex === i }"
        @click="ui.selectedDatasetIndex = i"
        @dblclick="openWorkspace(i)"
      >
        <span class="panel__col-name">{{ item.name }}</span>
        <AppCheckbox v-model:checked="item.fit" @click.stop />
        <AppCheckbox v-model:checked="item.validate" @click.stop />
        <span class="panel__col-ops">
          <IconButton icon="edit" @click.stop="openWorkspace(i)" />
          <IconButton icon="delete" @click.stop="removeDataset(i)" />
        </span>
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

.panel__actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.panel__columns {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
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
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs) var(--spacing-base);
  cursor: pointer;
}

.panel__row:nth-child(even) {
  background: var(--color-bg-subtle);
}

.panel__row:hover,
.panel__row.is-selected {
  background: var(--color-primary-light);
}

.panel__col-name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.panel__col-ops {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  width: 52px;
  justify-content: flex-end;
}
</style>

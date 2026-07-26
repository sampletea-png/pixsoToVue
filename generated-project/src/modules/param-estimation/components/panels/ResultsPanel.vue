<script setup lang="ts">
import AppCheckbox from '@/components/AppCheckbox.vue';
import IconButton from '@/components/IconButton.vue';
import { useUiStore } from '../../stores/ui';
import { useEstimationStore } from '../../stores/estimation';

const ui = useUiStore();
const estimation = useEstimationStore();

/** 行点击/行操作 → 打开 Apply estimation result 弹窗（容器-394，弹窗下阶段实现） */
function openApply(index: number): void {
  ui.selectedResultIndex = index;
  ui.applyResultVisible = true;
}

/** TODO: 交互待确认 —— 删除是否需二次确认无画板佐证，暂直接移除 */
function removeResult(index: number): void {
  estimation.results.splice(index, 1);
}
</script>

<template>
  <section class="panel">
    <header class="panel__header">
      <!-- TODO: 设计稿面板标题为 "Datasets" 但内容是 Result #1–#4（容器-9/10/394 存疑项），按原稿保留 -->
      <span class="panel__title-group">
        <!-- TODO: 交互待确认 —— 刷新按钮行为无画板佐证 -->
        <IconButton icon="refresh" />
        <span class="panel__title">Datasets</span>
      </span>
      <span class="panel__actions">
        <!-- TODO: 交互待确认 —— 删除按钮行为无画板佐证 -->
        <IconButton icon="delete" />
      </span>
    </header>
    <div class="panel__columns">
      <span class="panel__col-name">NAME</span>
      <span>Type</span>
      <span>Time</span>
      <span class="panel__col-ops" />
    </div>
    <ul class="panel__list">
      <li
        v-for="(result, i) in estimation.results"
        :key="result.id"
        class="panel__row"
        :class="{ 'is-selected': ui.selectedResultIndex === i }"
        @click="openApply(i)"
      >
        <AppCheckbox v-model:checked="result.checked" @click.stop />
        <span class="panel__col-name">{{ result.name }}</span>
        <span class="panel__type">{{ result.type }}</span>
        <span class="panel__time">{{ result.time }}</span>
        <span class="panel__col-ops">
          <!-- TODO: 交互待确认 —— 圆形「查看/定位」图标语义不明（低置信度），暂以 search 占位 -->
          <IconButton icon="search" @click.stop="openApply(i)" />
          <IconButton icon="delete" @click.stop="removeResult(i)" />
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

.panel__title-group {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
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

.panel__type,
.panel__time {
  color: var(--color-text-secondary);
}

.panel__col-ops {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}
</style>

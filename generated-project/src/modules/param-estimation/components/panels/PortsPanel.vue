<script setup lang="ts">
import AppCheckbox from '@/components/AppCheckbox.vue';
import AppSelect from '@/components/AppSelect.vue';
import { useDatasetStore } from '../../stores/dataset';

const dataset = useDatasetStore();

// 设计稿说明文案（容器-7 原文）
const description = 'Enable model ports and bind each one to a CSV header (click to edit).';

/** TODO: 交互待确认 —— v_init_kmh 行 CSV header 为下拉，候选项无画板佐证，暂以端口名占位 */
const csvHeaderOptions = [
  { label: 'v_init_kmh', value: 'v_init_kmh' },
  { label: 'T1', value: 'T1' },
  { label: 'ax_motion', value: 'ax_motion' },
];
</script>

<template>
  <section class="panel">
    <header class="panel__header">
      <span class="panel__title">Ports</span>
    </header>
    <p class="panel__desc">{{ description }}</p>

    <div class="panel__group">
      <h3 class="panel__group-title">Input ports</h3>
      <div class="panel__columns">
        <span>Fit</span>
        <span class="panel__col-port">Port</span>
        <span>CSV header</span>
      </div>
      <ul class="panel__list">
        <li v-for="(port, i) in dataset.inputPorts" :key="i" class="panel__row">
          <AppCheckbox v-model:checked="port.fit" />
          <span class="panel__col-port">{{ port.port }}</span>
          <AppSelect
            v-if="port.editable"
            v-model:value="port.csvHeader"
            :options="csvHeaderOptions"
          />
          <!-- TODO: 交互待确认 —— 其余行 "click to edit" 的编辑形式无画板佐证，暂只读 -->
          <span v-else class="panel__csv">{{ port.csvHeader }}</span>
        </li>
      </ul>
    </div>

    <div class="panel__group">
      <h3 class="panel__group-title">Out ports</h3>
      <div class="panel__columns">
        <span>Fit</span>
        <span class="panel__col-port">Port</span>
        <span>CSV header</span>
      </div>
      <ul class="panel__list">
        <li v-for="(port, i) in dataset.outputPorts" :key="i" class="panel__row">
          <AppCheckbox v-model:checked="port.fit" />
          <span class="panel__col-port">{{ port.port }}</span>
          <span class="panel__csv">{{ port.csvHeader }}</span>
        </li>
      </ul>
    </div>
  </section>
</template>

<style scoped>
.panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow-y: auto;
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

.panel__desc {
  margin: 0;
  padding: 0 var(--spacing-base) var(--spacing-sm);
  color: var(--color-text-secondary);
  border-bottom: 1px solid var(--color-border);
}

.panel__group {
  padding-top: var(--spacing-sm);
}

.panel__group-title {
  margin: 0;
  padding: 0 var(--spacing-base) var(--spacing-xs);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-bold);
}

.panel__columns {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs) var(--spacing-base);
  color: var(--color-text-muted);
}

.panel__list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.panel__row {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs) var(--spacing-base);
}

.panel__row:nth-child(even) {
  background: var(--color-bg-subtle);
}

.panel__col-port {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.panel__csv {
  color: var(--color-text-secondary);
}
</style>

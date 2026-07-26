<script setup lang="ts">
import AppDialog from '@/components/AppDialog.vue';
import AppButton from '@/components/AppButton.vue';
import AppInput from '@/components/AppInput.vue';
import IconButton from '@/components/IconButton.vue';
import ChartPlaceholder from '@/components/ChartPlaceholder.vue';
import { useUiStore } from '../../stores/ui';
import { useDatasetStore } from '../../stores/dataset';

// 容器-392：Dataset workspace 弹窗（1280×720，左数据集列表 + 中参数表 + 右曲线）
const ui = useUiStore();
const dataset = useDatasetStore();

function close(): void {
  ui.datasetWorkspaceVisible = false;
}

function selectDataset(name: string): void {
  dataset.currentDataset = name;
}

// TODO: 交互待确认 —— 新增数据集参数的形态（空行/选择器）无画板佐证，暂追加空行
function addParam(): void {
  dataset.datasetParams.push({ name: 'param', value: 0 });
}

// TODO: 交互待确认 —— 删除是否需二次确认无画板佐证，暂直接移除
function removeParam(index: number): void {
  dataset.datasetParams.splice(index, 1);
}

function addCurveParam(): void {
  // TODO: 交互待确认 —— Curves 头 "+ Add parameter" 作用于图表曲线（中置信度），无后续画板
}

function plotSimulation(): void {
  // TODO: 交互待确认 —— 触发仿真并刷新曲线，与状态栏进度联动为推断，暂占位
}
</script>

<template>
  <AppDialog
    :title="`Dataset workspace: ${dataset.currentDataset}`"
    :width="1280"
    @close="close"
  >
    <div class="workspace">
      <!-- 左栏：数据集列表（单选高亮） -->
      <aside class="workspace__datasets">
        <h3 class="workspace__col-title">Datasets</h3>
        <ul class="workspace__dataset-list">
          <li
            v-for="name in dataset.datasetFiles"
            :key="name"
            class="workspace__dataset-item"
            :class="{ 'is-selected': name === dataset.currentDataset }"
            @click="selectDataset(name)"
          >
            {{ name }}
          </li>
        </ul>
      </aside>

      <!-- 中栏：参数编辑表 -->
      <section class="workspace__params">
        <header class="workspace__params-header">
          <h3 class="workspace__col-title">Parameters</h3>
          <button type="button" class="workspace__text-btn" @click="addParam">
            + Add parameters
          </button>
        </header>
        <div class="workspace__params-columns">
          <span>NAME</span>
          <span>Current Value</span>
        </div>
        <ul class="workspace__param-list">
          <li
            v-for="(param, i) in dataset.datasetParams"
            :key="i"
            class="workspace__param-row"
          >
            <IconButton icon="delete" @click="removeParam(i)" />
            <span class="workspace__param-name">{{ param.name }}</span>
            <AppInput
              class="workspace__param-input"
              :value="param.value"
              @update:value="param.value = Number.parseFloat($event) || 0"
            />
          </li>
        </ul>
      </section>

      <!-- 右栏：曲线 -->
      <section class="workspace__curves">
        <header class="workspace__curves-header">
          <h3 class="workspace__col-title">Curves</h3>
          <span class="workspace__curves-actions">
            <AppButton @click="addCurveParam">+ Add parameter</AppButton>
            <AppButton type="primary" @click="plotSimulation">
              Plot&amp;Simulation
            </AppButton>
          </span>
        </header>
        <ChartPlaceholder
          class="workspace__chart"
          title="Simulation input curves"
          :legends="[
            { label: 'T1(Measure)' },
            { label: 'T2(measured)' },
            { label: 'v_init_kmh(measured)' },
          ]"
        />
        <ChartPlaceholder
          class="workspace__chart"
          title="Signal curve·v_hat_kmh"
          :legends="[
            { label: 'v_hatkmh(measured)' },
            { label: 'T2(measured)', color: 'var(--color-success)' },
            { label: 'v_init_kmh(measured)' },
          ]"
        />
      </section>
    </div>
  </AppDialog>
</template>

<style scoped>
.workspace {
  display: flex;
  gap: var(--spacing-md);
  height: 640px;
}

.workspace__col-title {
  margin: 0;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-bold);
}

.workspace__datasets {
  flex: none;
  width: 220px;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  border-right: 1px solid var(--color-border);
  padding-right: var(--spacing-base);
}

.workspace__dataset-list {
  flex: 1;
  margin: 0;
  padding: 0;
  list-style: none;
  overflow-y: auto;
}

.workspace__dataset-item {
  padding: var(--spacing-sm);
  cursor: pointer;
  border-radius: var(--radius-base);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.workspace__dataset-item:hover {
  background: var(--color-primary-light);
}

.workspace__dataset-item.is-selected {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.workspace__params {
  flex: none;
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.workspace__params-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.workspace__text-btn {
  padding: 0;
  border: none;
  background: transparent;
  color: var(--color-primary);
  font-size: var(--font-size-base);
  cursor: pointer;
}

.workspace__params-columns {
  display: flex;
  justify-content: space-between;
  padding: var(--spacing-xs) var(--spacing-sm);
  color: var(--color-text-muted);
  border-bottom: 1px solid var(--color-border);
}

.workspace__param-list {
  flex: 1;
  margin: 0;
  padding: 0;
  list-style: none;
  overflow-y: auto;
}

.workspace__param-row {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs) 0;
}

.workspace__param-row:nth-child(even) {
  background: var(--color-bg-subtle);
}

.workspace__param-name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.workspace__param-input {
  width: 105px;
  flex: none;
}

.workspace__curves {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.workspace__curves-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.workspace__curves-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.workspace__chart {
  flex: 1;
  min-height: 0;
}
</style>

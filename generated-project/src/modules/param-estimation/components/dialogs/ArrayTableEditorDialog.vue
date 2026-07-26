<script setup lang="ts">
import { computed, ref } from 'vue';
import AppDialog from '@/components/AppDialog.vue';
import AppButton from '@/components/AppButton.vue';
import AppInput from '@/components/AppInput.vue';
import AppSelect from '@/components/AppSelect.vue';
import ChartPlaceholder from '@/components/ChartPlaceholder.vue';
import { useUiStore } from '../../stores/ui';

// 容器-438/439：1D Array Table Editor 二级弹窗（1080×676）
// 两种形态由 Display 下拉驱动：
//   "initial Value" → 容器-438（两列网格 X Value/value + 折线图预览）
//   其余值          → 容器-439（9×5 全 0 网格 + X/Y/Z 范围 + 热力图 colorbar）
const ui = useUiStore();

// TODO: 标题数组名应与 ParametersDialog 触发卡片联动，当前固定 mock 第一张卡片
const tableName = ref('.pitch_model_1.Param');

// TODO: 设计稿 Display 下拉值为 "initial Value"（大小写原样），选项列表无画板佐证，按合理默认
const displayMode = ref('initial Value');
const displayOptions = [
  { label: 'initial Value', value: 'initial Value' },
  { label: 'Lower bound', value: 'Lower bound' },
  { label: 'Upper bound', value: 'Upper bound' },
];

/** true = 容器-438 形态（initial Value）；false = 容器-439 形态 */
const isInitialMode = computed<boolean>(() => displayMode.value === 'initial Value');

// ── 容器-438 形态：两列网格（X Value 1–9 + value 列，第 6 行选中高亮） ──
interface InitialRow {
  index: number;
  selected: boolean;
  value: string;
}

const INITIAL_VALUES = ['0.6', '0.8', '0.08', '0.05', '0.03', '0.04', '0.6', '0', '0'];

function makeInitialRows(): InitialRow[] {
  return INITIAL_VALUES.map((v, i) => ({
    index: i + 1,
    selected: i === 5,
    value: v,
  }));
}

const initialRows = ref<InitialRow[]>(makeInitialRows());

// ── 容器-439 形态：9 行 × 5 列可编辑网格（单元格初值全 "0"，第 6 行选中高亮） ──
interface GridRow {
  index: number;
  selected: boolean;
  cells: string[];
}

const GRID_COLS = 5;

function makeRows(): GridRow[] {
  return Array.from({ length: 9 }, (_, i) => ({
    index: i + 1,
    selected: i === 5,
    cells: Array.from({ length: GRID_COLS }, () => '0'),
  }));
}

const gridRows = ref<GridRow[]>(makeRows());

type BoundMode = 'fixed' | 'relative';
type BoundTarget = 'lower' | 'upper' | null;

const boundMode = ref<BoundMode>('fixed');
// TODO: 交互待确认 —— Lower/Upper bound 按钮按「切换当前编辑的边界对象」实现（中置信度）；
// 设计稿两按钮默认均为次按钮灰底，故初始无激活对象
const boundTarget = ref<BoundTarget>(null);

// X/Y/Z 范围（容器-439：初值全 "1"）
const axisRange = ref({
  x: { min: '1', max: '1' },
  y: { min: '1', max: '1' },
  z: { min: '1', max: '1' },
});

function toggleRowSelected(row: { selected: boolean }): void {
  row.selected = !row.selected;
}

function selectAll(): void {
  const rows = isInitialMode.value ? initialRows.value : gridRows.value;
  rows.forEach((r) => {
    r.selected = true;
  });
}

function deselectAll(): void {
  const rows = isInitialMode.value ? initialRows.value : gridRows.value;
  rows.forEach((r) => {
    r.selected = false;
  });
}

function resetValues(): void {
  if (isInitialMode.value) {
    initialRows.value = makeInitialRows();
  } else {
    gridRows.value = makeRows();
  }
}

function applySelected(): void {
  // TODO: 交互待确认 —— 将 Bound settings 应用到选中单元格的具体语义无画板佐证
}

function fitToData(): void {
  // TODO: 交互待确认 —— 按网格数据自动填充范围，mock 实现：取单元格数值 min/max
  const values = gridRows.value.flatMap((r) => r.cells.map(Number));
  axisRange.value.y.min = String(Math.min(...values));
  axisRange.value.y.max = String(Math.max(...values));
}

function close(): void {
  ui.arrayEditorVisible = false;
}
</script>

<template>
  <AppDialog
    :title="`1D Array Table Editor - ${tableName}`"
    :width="1080"
    @close="close"
  >
    <div class="array-editor">
      <!-- 工具行 -->
      <div class="array-editor__toolbar">
        <span class="array-editor__label">Display</span>
        <AppSelect v-model:value="displayMode" :options="displayOptions" />
        <AppButton @click="selectAll">Select all</AppButton>
        <AppButton @click="deselectAll">Deselect all</AppButton>
        <AppButton @click="resetValues">Reset</AppButton>
        <span class="array-editor__hint">
          Right-click cells to select or deselect
        </span>
      </div>

      <!-- Bound settings 行 -->
      <div class="array-editor__bounds">
        <span class="array-editor__label">Bound settings</span>
        <div class="array-editor__segmented" role="group">
          <button
            type="button"
            class="array-editor__segment"
            :class="{ 'is-active': boundMode === 'fixed' }"
            @click="boundMode = 'fixed'"
          >
            Fixed value
          </button>
          <button
            type="button"
            class="array-editor__segment"
            :class="{ 'is-active': boundMode === 'relative' }"
            @click="boundMode = 'relative'"
          >
            Relative to the initial
          </button>
        </div>
        <span class="array-editor__divider" />
        <AppButton
          :type="boundTarget === 'lower' ? 'primary' : 'default'"
          @click="boundTarget = 'lower'"
        >
          Lower bound
        </AppButton>
        <AppButton
          :type="boundTarget === 'upper' ? 'primary' : 'default'"
          @click="boundTarget = 'upper'"
        >
          Upper bound
        </AppButton>
        <span class="array-editor__divider" />
        <AppButton type="primary" @click="applySelected">
          Apply selected
        </AppButton>
      </div>

      <!-- 容器-438 形态：两列网格 + 折线图预览 -->
      <div v-if="isInitialMode" class="array-editor__body">
        <table class="array-editor__grid">
          <thead>
            <tr>
              <th>X Value</th>
              <th>value</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="row in initialRows"
              :key="row.index"
              :class="{ 'is-selected': row.selected }"
              @contextmenu.prevent="toggleRowSelected(row)"
            >
              <th>{{ row.index }}</th>
              <td>
                <AppInput v-model:value="row.value" />
              </td>
            </tr>
          </tbody>
        </table>

        <ChartPlaceholder
          class="array-editor__chart"
          :legends="[
            { label: 'Initial values', color: 'var(--color-info)' },
            { label: 'Lower bound', color: 'var(--color-success)' },
            { label: 'Upper bound', color: 'var(--color-warning)' },
          ]"
        />
      </div>

      <!-- 容器-439 形态：9×5 网格 + 范围表单 + 热力图预览 -->
      <div v-else class="array-editor__body">
        <table class="array-editor__grid">
          <thead>
            <tr>
              <th>Y Value</th>
              <th v-for="c in GRID_COLS" :key="c">{{ c }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="row in gridRows"
              :key="row.index"
              :class="{ 'is-selected': row.selected }"
              @contextmenu.prevent="toggleRowSelected(row)"
            >
              <th>{{ row.index }}</th>
              <td v-for="(cell, ci) in row.cells" :key="ci">
                <AppInput v-model:value="row.cells[ci]" />
              </td>
            </tr>
          </tbody>
        </table>

        <div class="array-editor__side">
          <div class="array-editor__range">
            <div
              v-for="axis in ['x', 'y', 'z'] as const"
              :key="axis"
              class="array-editor__range-group"
            >
              <div class="array-editor__range-row">
                <span class="array-editor__label">{{ axis.toUpperCase() }} min</span>
                <AppInput v-model:value="axisRange[axis].min" />
              </div>
              <div class="array-editor__range-row">
                <span class="array-editor__label">{{ axis.toUpperCase() }} max</span>
                <AppInput v-model:value="axisRange[axis].max" />
              </div>
            </div>
            <AppButton
              class="array-editor__fit"
              type="primary"
              @click="fitToData"
            >
              Fit to Data
            </AppButton>
          </div>
          <!-- TODO: 图表库 —— 容器-439 右侧为热力图预览 + 竖向彩虹 colorbar（红→黄→绿→蓝），
               待引入图表库后渲染；此处用灰底占位 + CSS 渐变还原 colorbar -->
          <div class="array-editor__heatmap">
            <span class="array-editor__colorbar" />
          </div>
        </div>
      </div>
    </div>
  </AppDialog>
</template>

<style scoped>
.array-editor {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-base);
}

.array-editor__label {
  flex: none;
  color: var(--color-text-secondary);
}

.array-editor__toolbar,
.array-editor__bounds {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.array-editor__hint {
  margin-left: auto;
  color: var(--color-text-muted);
}

.array-editor__segmented {
  display: inline-flex;
  border: 1px solid var(--color-border-input);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.array-editor__segment {
  height: 24px;
  padding: 0 var(--spacing-base);
  border: none;
  background: var(--color-surface);
  color: var(--color-text);
  font-size: var(--font-size-base);
  cursor: pointer;
}

.array-editor__segment + .array-editor__segment {
  border-left: 1px solid var(--color-border-input);
}

.array-editor__segment.is-active {
  background: var(--color-primary);
  color: var(--color-surface);
}

.array-editor__divider {
  flex: none;
  width: 1px;
  height: 16px;
  background: var(--color-border-strong);
}

.array-editor__body {
  display: flex;
  gap: var(--spacing-md);
  min-height: 0;
}

.array-editor__grid {
  flex: none;
  border-collapse: collapse;
}

.array-editor__grid th {
  padding: var(--spacing-xs) var(--spacing-sm);
  background: var(--color-bg);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-regular);
  text-align: center;
}

.array-editor__grid td {
  padding: var(--spacing-xs);
}

.array-editor__grid td .app-input {
  width: 70px;
}

.array-editor__grid tbody tr:nth-child(even) th,
.array-editor__grid tbody tr:nth-child(even) td {
  background: var(--color-bg-subtle);
}

.array-editor__grid tbody tr.is-selected th,
.array-editor__grid tbody tr.is-selected td {
  background: var(--color-primary-light);
}

.array-editor__chart {
  flex: 1;
  min-width: 0;
}

.array-editor__side {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.array-editor__range {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
}

.array-editor__range-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.array-editor__range-row {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.array-editor__range-row .app-input {
  width: 56px;
}

.array-editor__fit {
  margin-left: auto;
}

.array-editor__heatmap {
  position: relative;
  flex: 1;
  min-height: 260px;
  background: var(--color-bg);
  border-radius: var(--radius-base);
}

.array-editor__colorbar {
  position: absolute;
  top: var(--spacing-base);
  right: var(--spacing-base);
  width: 24px;
  height: 180px;
  border-radius: var(--radius-sm);
  background: linear-gradient(
    180deg,
    var(--color-danger),
    var(--color-warning),
    var(--color-success),
    var(--color-info)
  );
}
</style>

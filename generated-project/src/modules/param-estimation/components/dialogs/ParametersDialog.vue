<script setup lang="ts">
import { computed, ref } from 'vue';
import AppDialog from '@/components/AppDialog.vue';
import AppButton from '@/components/AppButton.vue';
import AppCheckbox from '@/components/AppCheckbox.vue';
import IconButton from '@/components/IconButton.vue';
import DataTable, {
  type DataTableColumn,
} from '@/components/DataTable.vue';
import { useUiStore } from '../../stores/ui';

// 容器-385/11/396：Parameters 弹窗（空态 / 填充态 / 含数组卡片三态，数据驱动切换）
const ui = useUiStore();

type ParamRow = {
  name: string;
  current: number;
  initial: number;
  unit: string;
  description: string;
  lowerBound: number;
  upperBound: number;
  scale: number;
  meaning: string;
  fixed: boolean;
}

type ArrayCard = {
  name: string;
  info: string;
}

// 弹窗参数表 9 行 mock（容器-11/396 数据识别）
const params = ref<ParamRow[]>([
  { name: 'K_drive', current: 1.025397, initial: 0.6, unit: '—', description: '—', lowerBound: 0.01, upperBound: 20, scale: 1, meaning: 'pitch model Stage-1 longitudinal parameter', fixed: false },
  { name: 'Kbrake', current: 0.765554, initial: 0.8, unit: '—', description: '—', lowerBound: 0.01, upperBound: 20, scale: 1, meaning: 'pitch model Stage-1 longitudinal parameter', fixed: false },
  { name: 'Cv', current: 0.000151, initial: 0.08, unit: '—', description: '—', lowerBound: 0.0001, upperBound: 5, scale: 0.1, meaning: 'pitch model Stage-1 longitudinal parameter', fixed: false },
  { name: 'C_roll', current: 0.209244, initial: 0.05, unit: '—', description: '—', lowerBound: 0.000001, upperBound: 5, scale: 0.1, meaning: 'pitch model Stage-1 longitudinal parameter', fixed: false },
  { name: 'tau_drive', current: 0.124356, initial: 0.03, unit: '—', description: '—', lowerBound: 0.001, upperBound: 0.5, scale: 0.1, meaning: 'pitch model Stage-1 longitudinal parameter', fixed: false },
  { name: 'tau_brake', current: 0.006636, initial: 0.04, unit: '—', description: '—', lowerBound: 0.001, upperBound: 0.5, scale: 0.1, meaning: 'pitch model Stage-1 longitudinal parameter', fixed: false },
  { name: 'v_eps', current: 0.021103, initial: 0.6, unit: '—', description: '—', lowerBound: 0.02, upperBound: 2, scale: 0.5, meaning: 'pitch model Stage-1 longitudinal parameter', fixed: false },
  { name: 'K_ddrive', current: -0.000535, initial: 0, unit: '—', description: '—', lowerBound: -5, upperBound: 5, scale: 0.1, meaning: 'pitch model Stage-1 longitudinal parameter', fixed: false },
  { name: 'K_dbrake', current: 0.002793, initial: 0, unit: '—', description: '—', lowerBound: -5, upperBound: 5, scale: 0.1, meaning: 'pitch model Stage-1 longitudinal parameter', fixed: false },
]);

// 数组参数卡片（容器-396，2 张）
const arrayCards = ref<ArrayCard[]>([
  { name: '.pitch_model_1.Param', info: '1D array · 50 · 0/50 selected' },
  { name: '.pitch_model_1.Param_1', info: '2D array · 10 x 10 · 0/100 selected' },
]);

// 空态文案（容器-385 原文）
const EMPTY_HINT_LINES = [
  'No estimation parameters selected. Click "Add parameters",',
  'check items in the list, then click "Apply" to configure initial values and bounds in the main table.',
];

const columns: DataTableColumn[] = [
  { key: 'action', title: 'ACTION', width: 62 },
  { key: 'fixed', title: 'FIX', width: 60 },
  { key: 'name', title: 'PARAMETER' },
  { key: 'current', title: 'CURRENT' },
  { key: 'initial', title: 'INITIAL / FIXED' },
  { key: 'unit', title: 'UNIT' },
  { key: 'description', title: 'DESCRIPTION' },
  { key: 'lowerBound', title: 'LOWER BOUND' },
  { key: 'upperBound', title: 'UPPER BOUND' },
  { key: 'scale', title: 'SCALE' },
  { key: 'meaning', title: 'Physical meaning (optional)' },
];

const hasData = computed<boolean>(
  () => params.value.length > 0 || arrayCards.value.length > 0,
);

// TODO: 计数口径待确认 —— 设计稿底栏 "Selected estimation parameters: 11" 与表格 9 行不一致，
// 按 computed 实现：标量参数行数 + 数组卡片数（9 + 2 = 11，与设计稿吻合）
const selectedCount = computed<number>(
  () => params.value.length + arrayCards.value.length,
);

// 设计稿基准态：tau_brake 行（下标 5）高亮
const selectedRowIndex = ref(5);

function close(): void {
  ui.parametersVisible = false;
}

function openAddParameters(): void {
  ui.addParametersVisible = true;
}

function clearParameters(): void {
  // TODO: 交互待确认 —— 清空是否需二次确认无画板佐证，暂直接清空（联动空态）
  params.value = [];
  arrayCards.value = [];
}

function openArrayEditor(): void {
  ui.arrayEditorVisible = true;
}

function removeArrayCard(index: number): void {
  arrayCards.value.splice(index, 1);
}

function removeParam(index: number): void {
  params.value.splice(index, 1);
}
</script>

<template>
  <AppDialog title="Parameters" :width="1280" @close="close">
    <div class="params-dialog">
      <div class="params-dialog__toolbar">
        <AppButton type="primary" @click="openAddParameters">
          Add parameters
        </AppButton>
        <AppButton v-if="hasData" @click="clearParameters">
          Clear parameters
        </AppButton>
      </div>

      <!-- 空态（容器-385）：居中文案 + 仅 Add parameters 按钮 -->
      <div v-if="!hasData" class="params-dialog__empty">
        <p v-for="line in EMPTY_HINT_LINES" :key="line">{{ line }}</p>
      </div>

      <template v-else>
        <!-- 数组参数卡片列表（容器-396） -->
        <ul v-if="arrayCards.length > 0" class="params-dialog__cards">
          <li
            v-for="(card, i) in arrayCards"
            :key="card.name"
            class="params-dialog__card"
          >
            <div class="params-dialog__card-info">
              <span class="params-dialog__card-name">{{ card.name }}</span>
              <span class="params-dialog__card-meta">{{ card.info }}</span>
            </div>
            <span class="params-dialog__card-actions">
              <AppButton type="primary" @click="openArrayEditor">
                Detailed edit
              </AppButton>
              <AppButton @click="removeArrayCard(i)">Remove table</AppButton>
            </span>
          </li>
        </ul>

        <DataTable
          class="params-dialog__table"
          :columns="columns"
          :rows="params"
          :selected-index="selectedRowIndex"
          @select="selectedRowIndex = $event"
        >
          <!-- TODO: ACTION 列 DSL 为无语义矢量组（垃圾桶视觉），按删除实现（中置信度） -->
          <template #cell="{ row, column }">
            <IconButton
              v-if="column.key === 'action'"
              icon="delete"
              @click.stop="removeParam(params.indexOf(row as ParamRow))"
            />
            <AppCheckbox
              v-else-if="column.key === 'fixed'"
              v-model:checked="(row as ParamRow).fixed"
              @click.stop
            />
            <template v-else>{{ row[column.key] }}</template>
          </template>
        </DataTable>
      </template>
    </div>

    <template #footer>
      <span class="params-dialog__count">
        Selected estimation parameters: {{ selectedCount }}
      </span>
    </template>
  </AppDialog>
</template>

<style scoped>
.params-dialog {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-base);
}

.params-dialog__toolbar {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.params-dialog__empty {
  padding: var(--spacing-lg) 0;
  text-align: center;
  color: var(--color-text-muted);
}

.params-dialog__empty p {
  margin: 0;
  line-height: 20px;
}

.params-dialog__cards {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  margin: 0;
  padding: 0;
  list-style: none;
}

.params-dialog__card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-sm) var(--spacing-base);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-base);
}

.params-dialog__card-info {
  display: flex;
  align-items: baseline;
  gap: var(--spacing-base);
  min-width: 0;
}

.params-dialog__card-name {
  font-weight: var(--font-weight-bold);
}

.params-dialog__card-meta {
  color: var(--color-text-secondary);
}

.params-dialog__card-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex: none;
}

.params-dialog__table {
  max-height: 420px;
  border: 1px solid var(--color-border);
}

.params-dialog__count {
  margin-right: auto;
  color: var(--color-text-secondary);
}
</style>

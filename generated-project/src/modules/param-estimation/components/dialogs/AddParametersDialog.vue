<script setup lang="ts">
import { computed, ref } from 'vue';
import AppDialog from '@/components/AppDialog.vue';
import AppButton from '@/components/AppButton.vue';
import AppCheckbox from '@/components/AppCheckbox.vue';
import AppInput from '@/components/AppInput.vue';
import DataTable, {
  type DataTableColumn,
} from '@/components/DataTable.vue';
import { useUiStore } from '../../stores/ui';
import { useEstimationStore } from '../../stores/estimation';

// 容器-387：Add parameters 二级弹窗（过滤 + 多选 + Apply，1080×640）
const ui = useUiStore();
const estimation = useEstimationStore();

type CandidateParam = {
  checked: boolean;
  fullName: string;
  scope: string;
  type: string;
  valueUnit: string;
  description: string;
}

// 候选参数 mock（容器-387 数据识别）
// 勾选分布按设计稿：可见 9 行仅 C_roll / tau_brake / v_eps 三行勾选，
// 滚动区外再勾 7 行，合计 "10 selected"
const candidates = ref<CandidateParam[]>([
  { checked: false, fullName: 'K_drive', scope: 'model', type: 'double', valueUnit: '1.025397 -', description: 'param[0]' },
  { checked: false, fullName: 'Kbrake', scope: 'model', type: 'double', valueUnit: '0.000151 -', description: 'param_1[0,0]' },
  { checked: false, fullName: 'Cv', scope: 'model', type: 'double', valueUnit: '0.124356 -', description: '—' },
  { checked: true, fullName: 'C_roll', scope: 'model', type: 'double', valueUnit: '0.021103 -', description: '—' },
  { checked: false, fullName: 'tau_drive', scope: 'model', type: 'double', valueUnit: '-0.000535 -', description: '—' },
  { checked: true, fullName: 'tau_brake', scope: 'model', type: 'double', valueUnit: '0.013889 -', description: '—' },
  { checked: true, fullName: 'v_eps', scope: 'model', type: 'double', valueUnit: '1.874974 -', description: '—' },
  { checked: false, fullName: 'K_ddrive', scope: 'model', type: 'double', valueUnit: '1.680598 -', description: '—' },
  { checked: false, fullName: 'K_dbrake', scope: 'model', type: 'double', valueUnit: '0.262522 -', description: '—' },
  // ── 以下为滚动区外行（7 行勾选，合计 10 selected） ──
  { checked: true, fullName: '.pitch_model_1.Param', scope: 'model', type: 'double[50]', valueUnit: '—', description: '—' },
  { checked: true, fullName: '.pitch_model_1.Param_1', scope: 'model', type: 'double[10x10]', valueUnit: '—', description: '—' },
  { checked: true, fullName: 'pre_wn1', scope: 'model', type: 'double', valueUnit: '5.0562681 -', description: '—' },
  { checked: true, fullName: 'pre_Kax2', scope: 'model', type: 'double', valueUnit: '-3.059027 -', description: '—' },
  { checked: true, fullName: 'pre_wn2', scope: 'model', type: 'double', valueUnit: '3.1236052 -', description: '—' },
  { checked: true, fullName: 'Klow_brake', scope: 'model', type: 'double', valueUnit: '0 -', description: '—' },
  { checked: true, fullName: 'B_drive_release', scope: 'model', type: 'double', valueUnit: '0.262522 -', description: '—' },
]);

const filterText = ref('');

// TODO: 表头 "Descriptiom" 为设计稿原文拼写（疑 Description），按原稿保留
const columns: DataTableColumn[] = [
  { key: 'checked', title: '', width: 40 },
  { key: 'fullName', title: 'Full name' },
  { key: 'scope', title: 'Scope' },
  { key: 'type', title: 'Type' },
  { key: 'valueUnit', title: 'Value Unit' },
  { key: 'description', title: 'Descriptiom' },
];

// 按 full name / type / scope 过滤（placeholder 文案即事件说明）
const filteredCandidates = computed<CandidateParam[]>(() => {
  const kw = filterText.value.trim().toLowerCase();
  if (!kw) return candidates.value;
  return candidates.value.filter(
    (c) =>
      c.fullName.toLowerCase().includes(kw) ||
      c.type.toLowerCase().includes(kw) ||
      c.scope.toLowerCase().includes(kw) ||
      c.description.toLowerCase().includes(kw),
  );
});

const checkedCount = computed<number>(
  () => candidates.value.filter((c) => c.checked).length,
);
const visibleCount = computed<number>(() => filteredCandidates.value.length);

function selectAllFiltered(): void {
  filteredCandidates.value.forEach((c) => {
    c.checked = true;
  });
}

function clearFiltered(): void {
  filteredCandidates.value.forEach((c) => {
    c.checked = false;
  });
}

function close(): void {
  ui.addParametersVisible = false;
}

function apply(): void {
  // TODO: 简单 mock —— 勾选项并入参数表；与 ParametersDialog 大表（含 bounds/scale）
  // 的数据模型统一待后续阶段处理，此处按任务约定向 estimation.parameters 追加
  candidates.value
    .filter((c) => c.checked)
    .forEach((c) => {
      estimation.parameters.push({
        name: c.fullName,
        currentValue: Number.parseFloat(c.valueUnit) || 0,
      });
    });
  close();
}
</script>

<template>
  <AppDialog title="Add parameters" :width="1080" @close="close">
    <div class="add-params">
      <div class="add-params__filter-row">
        <AppInput
          v-model:value="filterText"
          class="add-params__filter"
          placeholder="Filter by full name, type, scope or id..."
        />
        <span class="add-params__count">
          {{ checkedCount }} selected · {{ visibleCount }} visible
        </span>
        <AppButton @click="selectAllFiltered">Select all(filtered)</AppButton>
        <AppButton @click="clearFiltered">Clear (filtered)</AppButton>
      </div>

      <DataTable
        class="add-params__table"
        :columns="columns"
        :rows="filteredCandidates"
        :row-class="(row) => ((row as CandidateParam).checked ? 'is-checked' : '')"
      >
        <template #cell="{ row, column }">
          <AppCheckbox
            v-if="column.key === 'checked'"
            v-model:checked="(row as CandidateParam).checked"
            @click.stop
          />
          <template v-else>{{ row[column.key] }}</template>
        </template>
      </DataTable>
    </div>

    <template #footer>
      <AppButton @click="close">Cancel</AppButton>
      <AppButton type="primary" @click="apply">Apply</AppButton>
    </template>
  </AppDialog>
</template>

<style scoped>
.add-params {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-base);
}

.add-params__filter-row {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.add-params__filter {
  width: 423px;
  flex: none;
}

.add-params__count {
  flex: 1;
  color: var(--color-text-secondary);
  white-space: nowrap;
}

.add-params__table {
  max-height: 440px;
  border: 1px solid var(--color-border);
}

/* 勾选行整行浅蓝高亮 */
.add-params__table :deep(.data-table__row.is-checked) td {
  background: var(--color-primary-light);
}
</style>

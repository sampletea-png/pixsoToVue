<script setup lang="ts">
import { ref } from 'vue';
import AppDialog from '@/components/AppDialog.vue';
import AppButton from '@/components/AppButton.vue';
import DataTable, {
  type DataTableColumn,
} from '@/components/DataTable.vue';
import { useUiStore } from '../../stores/ui';
import { useEstimationStore } from '../../stores/estimation';

// 容器-394：Apply estimation result 确认弹窗（960×600，Current/Target 对照表）
const ui = useUiStore();
const estimation = useEstimationStore();

// 弹窗信息行 mock（容器-394 数据识别；与结果列表勾选行不一致为设计稿本身不自洽，按原稿）
const resultInfo = [
  { label: 'Result', value: 'Result #1' },
  { label: 'Type', value: 'auto' },
  { label: 'Time', value: '09:27:06' },
  { label: 'Parameter count', value: '11' },
];

type ApplyParamRow = {
  name: string;
  currentValue: number;
  targetValue: number;
}

// 对照表 11 行（逐行取自容器-394 截图；设计稿参数名带 "·" 前缀与异常字符，按原稿保留）
const applyParams = ref<ApplyParamRow[]>([
  { name: '·pitch_model_1.K_drive', currentValue: 1.025397, targetValue: 0.863199 },
  { name: '·pitch_model1.K_brake', currentValue: 0.765554, targetValue: 0.917131 },
  { name: '·pitch_model1.C.v', currentValue: 0.000151, targetValue: 0.107317 },
  { name: '·pitch_model1._.rol', currentValue: 0.209244, targetValue: 0.000001 },
  { name: '·pitch_model1.ta_drive', currentValue: 0.124356, targetValue: 0.5 },
  { name: '·pitch_model1.tau_brake', currentValue: 0.006636, targetValue: 0.028172 },
  { name: '·pitchmodel1.y.eps', currentValue: 0.021103, targetValue: 0.02 },
  { name: '·pitch_model1._.drive', currentValue: -0.000535, targetValue: 0.160551 },
  { name: '·pitch_model1.K_dbrake', currentValue: 0.002793, targetValue: -0.022824 },
  { name: '·pitch_model1.Klow_brake', currentValue: 0, targetValue: 8 },
  { name: '·pitch_model1.B_drive_release', currentValue: 0.262522, targetValue: 0.136931 },
]);

const columns: DataTableColumn[] = [
  { key: 'name', title: 'Parameter' },
  { key: 'currentValue', title: 'Current value' },
  { key: 'targetValue', title: 'Target value' },
];

// 容器-394：·pitchmodel1.y.eps 行（下标 6）蓝色高亮
const highlightedIndex = ref(6);

function close(): void {
  ui.applyResultVisible = false;
}

function apply(): void {
  // 把 Target value 写回参数表：按参数名末段匹配（mock，名称口径不一致时跳过）
  // TODO: 设计稿参数名带 "·pitch_model_1." 前缀且部分含异常字符，与 store 参数名的映射规则待确认
  applyParams.value.forEach((row) => {
    const shortName = row.name.slice(row.name.lastIndexOf('.') + 1);
    const target = estimation.parameters.find((p) => p.name === shortName);
    if (target) target.currentValue = row.targetValue;
  });
  close();
}
</script>

<template>
  <AppDialog title="Apply estimation result" :width="960" @close="close">
    <div class="apply-result">
      <div class="apply-result__info">
        <span
          v-for="item in resultInfo"
          :key="item.label"
          class="apply-result__info-item"
        >
          <span class="apply-result__info-label">{{ item.label }}</span>
          <span class="apply-result__info-value">{{ item.value }}</span>
        </span>
      </div>
      <!-- TODO: 设计稿原文缺首字母 "he following..."（疑 The following），按原稿保留 -->
      <p class="apply-result__desc">
        he following parameters will be written back to the current model.
        Confirm before continuing.
      </p>
      <DataTable
        class="apply-result__table"
        :columns="columns"
        :rows="applyParams"
        :selected-index="highlightedIndex"
        @select="highlightedIndex = $event"
      />
    </div>

    <template #footer>
      <AppButton @click="close">Cancel</AppButton>
      <!-- TODO: 设计稿原文拼写 "Apply to modle"（疑 model），按原稿保留 -->
      <AppButton type="primary" @click="apply">Apply to modle</AppButton>
    </template>
  </AppDialog>
</template>

<style scoped>
.apply-result {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-base);
}

.apply-result__info {
  display: flex;
  align-items: center;
}

.apply-result__info-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: 0 var(--spacing-lg);
}

.apply-result__info-item:first-child {
  padding-left: 0;
}

/* 组间 1px 竖分隔线 */
.apply-result__info-item + .apply-result__info-item {
  border-left: 1px solid var(--color-border);
}

.apply-result__info-label {
  font-size: var(--font-size-base);
  color: var(--color-text-muted);
}

.apply-result__info-value {
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
}

.apply-result__desc {
  margin: 0;
  color: var(--color-text-secondary);
}

.apply-result__table {
  max-height: 380px;
  border: 1px solid var(--color-border);
}
</style>

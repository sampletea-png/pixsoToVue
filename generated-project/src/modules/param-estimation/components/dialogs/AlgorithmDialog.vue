<script setup lang="ts">
import { reactive } from 'vue';
import AppDialog from '@/components/AppDialog.vue';
import AppButton from '@/components/AppButton.vue';
import AppCheckbox from '@/components/AppCheckbox.vue';
import AppRadio from '@/components/AppRadio.vue';
import AppInput from '@/components/AppInput.vue';
import AppSelect from '@/components/AppSelect.vue';
import { useUiStore } from '../../stores/ui';

// 容器-390/391：Algorithm 算法设置弹窗（5 分组表单，Cancel / Apply）
const ui = useUiStore();

// 表单 mock 默认值即设计稿值（容器-390 数据识别）
const form = reactive({
  objectiveMetric: 'sse',
  dynPerfCalibration: true,
  trackingWeight: '1',
  overshootWeight: '0',
  smoothnessWeight: '0',
  steadyStateTailRatio: '0.2',
  curvatureWeight: '0',
  steadyStateWeight: '0',
  maxOvershoot: '0.2',
  arrayDeltaLimit: '1',
  maxIterations: '220',
  parameterTolerance: '1e-8',
  functionTolerance: '1e-8',
  parallelWorkers: '1e-8',
  useNumericJacobian: true,
  jacobianBaseStep: '0.00001',
  jacobianMode: 'forward',
  backend: 'ceres',
  solverType: 'trust-region',
  trustRegionStrategy: 'levenberg-marquardt',
  denseLinearSolver: 'dense-qr',
  robustLoss: 'linear',
  lossScale: '1',
  ceresThreads: '1',
  gradientTolerance: '1e-10',
  useNonmonotonicSteps: true,
});

// TODO: 设计稿 "Parallel workers" 显示值为 "1e-8"（疑复制串值，worker 数应为整数），按原稿保留
const parallelWorkerOptions = [
  { label: '1e-8', value: '1e-8' },
  { label: '1', value: '1' },
  { label: '2', value: '2' },
  { label: '4', value: '4' },
];

// TODO: Robust loss 选项列表无画板佐证，按合理默认
const robustLossOptions = [
  { label: 'Linear', value: 'linear' },
  { label: 'Huber', value: 'huber' },
  { label: 'Cauchy', value: 'cauchy' },
];

// Dynamic performance calibration 权重输入组（勾选联动禁用，中置信度 + TODO）
const weightFields = [
  { key: 'trackingWeight', label: 'Tracking weight' },
  { key: 'curvatureWeight', label: 'Curvature weight' },
  { key: 'overshootWeight', label: 'Overshoot weight' },
  { key: 'steadyStateWeight', label: 'Steady-state weight' },
  { key: 'smoothnessWeight', label: 'Smoothness weight' },
  { key: 'maxOvershoot', label: 'Max overshoot' },
  { key: 'steadyStateTailRatio', label: 'Steady-state tail ratio' },
  { key: 'arrayDeltaLimit', label: 'Array delta limit' },
] as const;

function close(): void {
  ui.algorithmVisible = false;
}

function apply(): void {
  // TODO: 交互待确认 —— Apply 是否触发估计重跑无画板佐证，暂仅关闭弹窗（表单值保留在组件内）
  close();
}

const solverTypeOptions = [
  { value: 'trust-region', label: 'Trust region (TRUST_REGION)' },
  { value: 'line-search', label: 'Line search (LINE_SEARCH)' },
];
const trustRegionOptions = [
  { value: 'levenberg-marquardt', label: 'Levenberg-Marquardt' },
  { value: 'dogleg', label: 'Dogleg' },
];
const denseSolverOptions = [
  { value: 'dense-qr', label: 'DENSE_QR' },
  { value: 'dense-normal-cholesky', label: 'DENSE_NORMAL_CHOLESKY' },
];

// 供模板 v-model 写入 reactive 表单（key 受 weightFields 约束）
const weights = form as unknown as Record<string, string>;
</script>

<template>
  <AppDialog title="Algorithm" :width="1080" @close="close">
    <div class="algorithm">
      <!-- Objective -->
      <section class="algorithm__section">
        <h3 class="algorithm__section-title">Objective</h3>
        <p class="algorithm__hint">
          Choose how the estimation compares simulated and measured outputs.
        </p>
        <div class="algorithm__row">
          <span class="algorithm__row-label">Objective metric</span>
          <AppRadio
            :checked="form.objectiveMetric === 'sse'"
            label="Sum Squared Error (SSE)"
            @update:checked="form.objectiveMetric = 'sse'"
          />
        </div>
        <div class="algorithm__row">
          <span class="algorithm__row-label algorithm__row-label--muted">
            Dynamic performance calibration
          </span>
          <AppCheckbox
            v-model:checked="form.dynPerfCalibration"
            label="Dynamic performance calibration"
          />
        </div>
        <p class="algorithm__hint">
          For array table calibration, add tracking, curvature, step-response
          and table smoothness penalties. Step-response terms only apply to
          step-like data.
        </p>
        <!-- TODO: 交互待确认 —— 勾选 calibration 联动禁用权重输入组（中置信度推断） -->
        <div class="algorithm__grid">
          <div v-for="field in weightFields" :key="field.key" class="algorithm__row">
            <span class="algorithm__row-label">{{ field.label }}</span>
            <AppInput
              v-model:value="weights[field.key]"
              :disabled="!form.dynPerfCalibration"
            />
          </div>
        </div>
      </section>

      <!-- General -->
      <section class="algorithm__section">
        <h3 class="algorithm__section-title">General</h3>
        <div class="algorithm__grid">
          <div class="algorithm__row">
            <span class="algorithm__row-label">Max iterations</span>
            <AppInput v-model:value="form.maxIterations" />
          </div>
          <div class="algorithm__row">
            <span class="algorithm__row-label">Function tolerance</span>
            <AppInput v-model:value="form.functionTolerance" />
          </div>
          <div class="algorithm__row">
            <span class="algorithm__row-label">Parameter tolerance</span>
            <AppInput v-model:value="form.parameterTolerance" />
          </div>
          <div class="algorithm__row">
            <span class="algorithm__row-label">Parallel workers</span>
            <AppSelect
              v-model:value="form.parallelWorkers"
              :options="parallelWorkerOptions"
            />
          </div>
        </div>
        <div class="algorithm__row">
          <span class="algorithm__row-label algorithm__row-label--muted">
            Use numeric Jacobian
          </span>
          <AppCheckbox
            v-model:checked="form.useNumericJacobian"
            label="Use numeric Jacobian"
          />
        </div>
      </section>

      <!-- Jacobian finite difference mode -->
      <section class="algorithm__section">
        <h3 class="algorithm__section-title">
          Jacobian finite difference mode
        </h3>
        <div class="algorithm__row">
          <span class="algorithm__row-label">
            Jacobian finite-difference base step (h)
          </span>
          <AppInput v-model:value="form.jacobianBaseStep" />
        </div>
        <div class="algorithm__row">
          <AppRadio
            :checked="form.jacobianMode === 'forward'"
            label="Forward difference"
            @update:checked="form.jacobianMode = 'forward'"
          />
          <AppRadio
            :checked="form.jacobianMode === 'central'"
            label="Central difference"
            @update:checked="form.jacobianMode = 'central'"
          />
        </div>
      </section>

      <!-- Least-squares backend -->
      <section class="algorithm__section">
        <h3 class="algorithm__section-title">Least-squares backend</h3>
        <div class="algorithm__row">
          <span class="algorithm__row-label">Backend</span>
          <AppRadio
            :checked="form.backend === 'ceres'"
            label="Ceres"
            @update:checked="form.backend = 'ceres'"
          />
          <AppRadio
            :checked="form.backend === 'acm'"
            label="Apache Commons Math"
            @update:checked="form.backend = 'acm'"
          />
        </div>
      </section>

      <!-- Ceres solver -->
      <!-- TODO: 交互待确认 —— Backend 切换为 Apache Commons Math 时本分组是否隐藏无画板佐证，暂恒显 -->
      <section class="algorithm__section">
        <h3 class="algorithm__section-title">Ceres solver</h3>
        <div class="algorithm__row">
          <span class="algorithm__row-label">Solver type</span>
          <AppRadio
            v-for="opt in solverTypeOptions"
            :key="opt.value"
            :checked="form.solverType === opt.value"
            :label="opt.label"
            @update:checked="form.solverType = opt.value"
          />
        </div>
        <div class="algorithm__row">
          <span class="algorithm__row-label">Trust-region strategy</span>
          <AppRadio
            v-for="opt in trustRegionOptions"
            :key="opt.value"
            :checked="form.trustRegionStrategy === opt.value"
            :label="opt.label"
            @update:checked="form.trustRegionStrategy = opt.value"
          />
        </div>
        <div class="algorithm__row">
          <span class="algorithm__row-label">Dense linear solver</span>
          <AppRadio
            v-for="opt in denseSolverOptions"
            :key="opt.value"
            :checked="form.denseLinearSolver === opt.value"
            :label="opt.label"
            @update:checked="form.denseLinearSolver = opt.value"
          />
        </div>
        <div class="algorithm__row">
          <span class="algorithm__row-label">Robust loss</span>
          <AppSelect
            v-model:value="form.robustLoss"
            :options="robustLossOptions"
          />
        </div>
        <div class="algorithm__grid">
          <div class="algorithm__row">
            <span class="algorithm__row-label">Loss scale</span>
            <AppInput v-model:value="form.lossScale" />
          </div>
          <div class="algorithm__row">
            <span class="algorithm__row-label">Ceres threads</span>
            <AppInput v-model:value="form.ceresThreads" />
          </div>
          <div class="algorithm__row">
            <span class="algorithm__row-label">Gradient tolerance (Ceres)</span>
            <AppInput v-model:value="form.gradientTolerance" />
          </div>
        </div>
        <div class="algorithm__row">
          <span class="algorithm__row-label algorithm__row-label--muted">
            Use nonmonotonic steps
          </span>
          <AppCheckbox
            v-model:checked="form.useNonmonotonicSteps"
            label="Use nonmonotonic steps"
          />
        </div>
      </section>
    </div>

    <template #footer>
      <AppButton @click="close">Cancel</AppButton>
      <AppButton type="primary" @click="apply">Apply</AppButton>
    </template>
  </AppDialog>
</template>

<style scoped>
.algorithm {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.algorithm__section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.algorithm__section-title {
  margin: 0;
  padding: var(--spacing-xs) 0;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-bold);
  border-bottom: 1px solid var(--color-border);
}

.algorithm__hint {
  margin: 0;
  color: var(--color-text-muted);
}

.algorithm__row {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.algorithm__row-label {
  flex: none;
  width: 200px;
  color: var(--color-text);
}

.algorithm__row-label--muted {
  color: var(--color-text-muted);
}

.algorithm__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: var(--spacing-lg);
  row-gap: var(--spacing-sm);
}
</style>

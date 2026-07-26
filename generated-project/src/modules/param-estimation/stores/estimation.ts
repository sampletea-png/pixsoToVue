import { defineStore } from 'pinia';
import { ref } from 'vue';

export type ParameterItem = {
  name: string;
  currentValue: number;
}

export type IterationRow = {
  step: number;
  cost: number;
  ki: number;
  kp: number;
  tau: number;
  wn: number;
  // 设计稿后 5 列列名均为 K_brake（疑复制未改），按原样保留
  // TODO: 设计稿列名重复待确认 —— 真实语义应为不同参数
  kBrake1: number;
  kBrake2: number;
  kBrake3: number;
  kBrake4: number;
  kBrake5: number;
}

export type SensitivityPoint = {
  train: number;
  validation: number;
  total: number;
}

export type SensitivityRow = {
  parameter: string;
  dSseTrain: number;
  dSseValidation: number;
  dSseTotal: number;
}

export type ResultItem = {
  id: number;
  name: string;
  type: string;
  time: string;
  checked: boolean;
}

export type ManualParamRow = {
  parameter: string;
  value: number;
  initial: number;
  lower: number;
  upper: number;
}

export type CostItem = {
  label: string;
  /** 展示文本，如 "59.0466 → 59.0466 (+0)" */
  text: string;
}

export type RunState = 'stopped' | 'running';

/**
 * 估计业务数据：参数表、迭代历史、指标、敏感度、结果列表、运行状态。
 * mock 数值取自 artifacts/02-analysis/容器-2/7/9/10/394.md「数据识别」。
 */
export const useEstimationStore = defineStore('param-estimation-estimation', () => {
  // 左侧面板参数表（容器-2，NAME/Current Value 两列 9 行）
  // TODO: 设计稿第 2 行与第 1 行同名 K_drive（疑为 K_brake 误录），按原稿保留待确认
  const parameters = ref<ParameterItem[]>([
    { name: 'K_drive', currentValue: 1.025397 },
    { name: 'K_drive', currentValue: 0.765554 },
    { name: 'C_v', currentValue: 1.025397 },
    { name: 'C_roll', currentValue: 0.765554 },
    { name: 'tau_drive', currentValue: 1.025397 },
    { name: 'tau_brake', currentValue: 0.765554 },
    // TODO: 设计稿原文参数名 v_e'p's / k_dbrake 大小写与引号异常，按原稿保留
    { name: "v_e'p's", currentValue: 1.025397 },
    { name: 'K_ddrive', currentValue: 0.765554 },
    { name: 'k_dbrake', currentValue: 1.025397 },
  ]);

  // 迭代历史（容器-2/容器-7，11 列 × 9 行，第 6 行选中）
  const iterationHistory = ref<IterationRow[]>([
    { step: 1, cost: 1.234, ki: 0.1234, kp: 0.5432, tau: 0.4567, wn: 5.234, kBrake1: 0.9334, kBrake2: 0.9334, kBrake3: 0.9334, kBrake4: 0.9334, kBrake5: 0.9334 },
    { step: 2, cost: 14.11, ki: 0.789, kp: 0.8765, tau: 0.2345, wn: 5.89, kBrake1: 0.7854, kBrake2: 0.7854, kBrake3: 0.7854, kBrake4: 0.7854, kBrake5: 0.7854 },
    { step: 3, cost: 5.6, ki: 0.456, kp: 0.1023, tau: 0.876, wn: 4.9, kBrake1: 0.9821, kBrake2: 0.9821, kBrake3: 0.9821, kBrake4: 0.9821, kBrake5: 0.9821 },
    { step: 4, cost: 11.34, ki: 0.9, kp: 0.987, tau: 0.123, wn: 5.123, kBrake1: 0.678, kBrake2: 0.678, kBrake3: 0.678, kBrake4: 0.678, kBrake5: 0.678 },
    { step: 5, cost: 2.34, ki: 0.3456, kp: 0.567, tau: 0.678, wn: 5.78, kBrake1: 0.8892, kBrake2: 0.8892, kBrake3: 0.8892, kBrake4: 0.8892, kBrake5: 0.8892 },
    { step: 6, cost: 13.5, ki: 0.234, kp: 0.321, tau: 0.543, wn: 5.432, kBrake1: 0.7654, kBrake2: 0.7654, kBrake3: 0.7654, kBrake4: 0.7654, kBrake5: 0.7654 },
    { step: 7, cost: 8.91, ki: 0.6789, kp: 0.789, tau: 0.901, wn: 5.56, kBrake1: 0.598, kBrake2: 0.598, kBrake3: 0.598, kBrake4: 0.598, kBrake5: 0.598 },
    { step: 8, cost: 11.34, ki: 0.3456, kp: 0.987, tau: 0.123, wn: 5.123, kBrake1: 0.678, kBrake2: 0.7854, kBrake3: 0.9821, kBrake4: 0.9821, kBrake5: 0.678 },
    { step: 9, cost: 11.34, ki: 0.3456, kp: 0.789, tau: 0.678, wn: 5.56, kBrake1: 0.678, kBrake2: 0.678, kBrake3: 0.8892, kBrake4: 0.678, kBrake5: 0.9334 },
  ]);

  // Report 指标（容器-7）
  const rmse = ref(0.768418);
  /** null 显示为 "--"（设计稿 Fit 值为空占位） */
  const fit = ref<number | null>(null);
  const cost = ref(59.046566);
  const iterations = ref(38);

  /** Report 状态消息条（容器-7 原文，含中英文混排，按原稿保留） */
  const reportMessage = ref(
    'Estimation finished. Ceres termination: CONVERGENCE；具体触发判据：参数增量相对尺度已满足用户在 Ceres 中配置的 parameter_tolerance。; optimizer iterations=37, residual evals=1501, SSE=60.3646.',
  );

  // 敏感度（容器-9/394；Initial/Best 两表设计稿数据相同，validation 列全 0，
  // train/total 数值逐行取自容器-9 截图）
  const perturbationRatio = ref(0.01);
  const initialPoint = ref<SensitivityPoint>({
    train: 4117.467967616531,
    validation: 0,
    total: 4117.467967616531,
  });
  const bestPoint = ref<SensitivityPoint>({
    train: 59.046565695501414,
    validation: 0,
    total: 59.046565695501414,
  });
  const sensitivityRows = ref<SensitivityRow[]>([
    { parameter: 'K_drive', dSseTrain: 438.3616584226363, dSseValidation: 0, dSseTotal: 438.3616584226363 },
    { parameter: 'K_brake', dSseTrain: 10.385982261017489, dSseValidation: 0, dSseTotal: 463.0409941139808 },
    { parameter: 'C_v', dSseTrain: 438.3616584226363, dSseValidation: 0, dSseTotal: 10.385982261017489 },
    { parameter: 'C_roll', dSseTrain: 14.427447020878844, dSseValidation: 0, dSseTotal: 12.271117240620242 },
    { parameter: 'tau_drive', dSseTrain: 438.3616584226363, dSseValidation: 0, dSseTotal: 14.427447020878844 },
    { parameter: 'tau_brake', dSseTrain: 29.171871118047875, dSseValidation: 0, dSseTotal: 29.171871118047875 },
    { parameter: 'v_eps', dSseTrain: 0.8810135542944408, dSseValidation: 0, dSseTotal: 23.508538015912336 },
    { parameter: 'K_ddrive', dSseTrain: 438.3616584226363, dSseValidation: 0, dSseTotal: 0.8810135542944408 },
    { parameter: 'K_dbrake', dSseTrain: 3.721450655130866, dSseValidation: 0, dSseTotal: 3.721450655130866 },
  ]);

  // 结果列表（容器-9/10/394：Result #1–#4，Result #4 勾选）
  const results = ref<ResultItem[]>([
    { id: 4, name: 'Result #4', type: 'Auto', time: '11:28:34', checked: true },
    { id: 3, name: 'Result #3', type: 'Auto', time: '10:21:54', checked: false },
    { id: 2, name: 'Result #2', type: 'Auto', time: '11:28:34', checked: false },
    { id: 1, name: 'Result #1', type: 'Auto', time: '11:28:34', checked: false },
  ]);

  // Manual tuning（容器-10）
  const manualParams = ref<ManualParamRow[]>([
    { parameter: 'K_drive', value: 0.852818, initial: 0.6, lower: 0.01, upper: 20 },
    { parameter: 'K_brake', value: 0.91612, initial: 0.8, lower: 0.01, upper: 20 },
    { parameter: 'C_v', value: 0.103311, initial: 0.08, lower: 0.0001, upper: 5 },
    { parameter: 'C_roll', value: 0.000001, initial: 0.05, lower: 0.000001, upper: 5 },
    { parameter: 'tau_drive', value: 0.20351, initial: 0.02, lower: 0.00000001, upper: 5 },
    { parameter: 'tau_brake', value: 0.91612, initial: 0.08, lower: 0.01, upper: 20 },
    { parameter: 'v_eps', value: 0.103311, initial: 0.08, lower: 0.0001, upper: 10 },
    { parameter: 'K_ddrive', value: 0.91612, initial: 0.08, lower: 0.0001, upper: 5 },
    { parameter: 'K_dbrake', value: 0.103311, initial: 0.02, lower: 0.001, upper: 5 },
  ]);
  // Cost companies（容器-10 原文 4 行；第 2/4 行同名 Fit SSE，按原稿保留）
  // TODO: 设计稿重复行名待确认
  const costItems = ref<CostItem[]>([
    { label: 'Total SSE', text: '59.0466 → 59.0466 (+0)' },
    { label: 'Fit SSE', text: '59.0466 → 59.0466 (+0)' },
    { label: 'Validation SSE', text: '0 → 0 (+0)' },
    { label: 'Fit SSE', text: '59.0466 → 59.0466 (+0)' },
  ]);

  // 运行状态（容器-2 基准：一次运行已结束）
  const runState = ref<RunState>('stopped');
  /** 0–100；基准态已完成 = 100 */
  const progress = ref(100);
  const iteration = ref(0);
  const step = ref(0);
  const completedIteration = ref(69);

  let timer: ReturnType<typeof setInterval> | null = null;

  /** TODO: run/mock —— 无真实算法，progress 简单递增到 100 后停止 */
  function run(): void {
    if (runState.value === 'running') return;
    runState.value = 'running';
    progress.value = 0;
    timer = setInterval(() => {
      progress.value = Math.min(100, progress.value + 2);
      if (progress.value >= 100) stopTimer();
    }, 100);
  }

  function stop(): void {
    stopTimer();
    runState.value = 'stopped';
    progress.value = 0;
  }

  function stopTimer(): void {
    if (timer !== null) {
      clearInterval(timer);
      timer = null;
    }
  }

  return {
    parameters,
    iterationHistory,
    rmse,
    fit,
    cost,
    iterations,
    reportMessage,
    perturbationRatio,
    initialPoint,
    bestPoint,
    sensitivityRows,
    results,
    manualParams,
    costItems,
    runState,
    progress,
    iteration,
    step,
    completedIteration,
    run,
    stop,
  };
});

import { defineStore } from 'pinia';
import { ref } from 'vue';

export type DatasetItem = {
  name: string;
  fit: boolean;
  validate: boolean;
  /** 关联的 CSV 数据文件（Simulation response 下拉数据源） */
  csvHeader: string;
}

export type PortItem = {
  port: string;
  fit: boolean;
  csvHeader: string;
  /** v_init_kmh 行的 CSV header 为下拉（容器-7），其余为文本 */
  editable: boolean;
}

export type DatasetParam = {
  name: string;
  value: number;
}

/**
 * 数据集业务数据：12 个数据集、端口绑定、数据集参数。
 * mock 数值取自 artifacts/02-analysis/容器-7/8/392.md「数据识别」。
 */
export const useDatasetStore = defineStore('param-estimation-dataset', () => {
  // 12 行数据集（容器-8；设计稿行序为 02,01,04,03,06,05,08,07,10,09,12,11）
  // TODO: 设计稿原文拼写 "Prewiew Dataset"（疑 Preview），按原稿保留待确认
  const DATASET_ORDER = [2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 12, 11];
  const datasets = ref<DatasetItem[]>(
    DATASET_ORDER.map((no) => ({
      name: `Prewiew Dataset ${String(no).padStart(2, '0')}`,
      // 编号 ≤10 的行 Fit 勾选；编号 11、12 的行 Validate 勾选
      fit: no <= 10,
      validate: no >= 11,
      csvHeader: '',
    })),
  );

  // Simulation response 当前查看的数据文件（容器-8 下拉值）
  const currentDataset = ref('with_drive_event_04_cycle_2_start_stop');

  /** 数据集下拉候选（容器-392 弹窗左栏 8 个数据文件名） */
  const datasetFiles = ref<string[]>([
    'with_drive_event_04_cycle_2_start_stop',
    'with_drive_event_03_full_start_stop',
    'with_drive_event_02',
    'with_drive_event_01',
    'natural_decay_event_02',
    'no_drive_reference_cropped_stop',
    'with_drive_event_03',
    'natural_decay_event_03',
  ]);

  // 端口绑定（容器-7：Input ports 3 行全勾选 + Out ports 7 行，仅 ax_motion 勾选）
  const inputPorts = ref<PortItem[]>([
    { port: 'T1', fit: true, csvHeader: 'T1', editable: false },
    { port: 'T1', fit: true, csvHeader: 'T1', editable: false },
    { port: 'v_init_kmh', fit: true, csvHeader: 'v_init_kmh', editable: true },
  ]);
  const outputPorts = ref<PortItem[]>([
    { port: 'a_imu_x_hat', fit: false, csvHeader: 'a_imu_x_hat', editable: false },
    { port: 'ax_vehicle', fit: false, csvHeader: 'ax_vehicle', editable: false },
    { port: 'ax_motion', fit: true, csvHeader: 'ax_motion', editable: false },
    { port: 'ax_free', fit: false, csvHeader: 'ax_free', editable: false },
    { port: 'v_init_kmh', fit: false, csvHeader: 'v_init_kmh', editable: false },
    { port: 'pitch_hat', fit: false, csvHeader: 'pitch_hat', editable: false },
    { port: 'v_init_kmh', fit: false, csvHeader: 'v_init_kmh', editable: false },
  ]);

  // 数据集参数（容器-392 弹窗中栏 8 行）
  const datasetParams = ref<DatasetParam[]>([
    { name: 'Ts', value: 0.01 },
    { name: 'torqueToKnm', value: 0.001 },
    { name: 'v_low_brake', value: 0.02 },
    { name: 'stop_v_eps', value: 0.0138888 },
    { name: 'tau_stop_ax', value: 0.04 },
    { name: 'pre_wn1', value: 5.0562681 },
    { name: 'pre_Kax2', value: -3.059027 },
    { name: 'pre_wn2', value: 3.1236052 },
  ]);

  return {
    datasets,
    currentDataset,
    datasetFiles,
    inputPorts,
    outputPorts,
    datasetParams,
  };
});

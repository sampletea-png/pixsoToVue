# 03 - 项目架构

> Phase 3 产物。输入：16 份 `02-analysis/*.md` + `03-shared-candidates.md`（258 个候选）。
> **经用户确认后才允许进入编码阶段。**

## 概述

- 项目名：`param-estimation-toolbox`，目标目录：`generated-project/`
- 技术栈：Vite + Vue3 + `<script setup>` + TS + Pinia + Vue Router（默认栈，无第三方 UI 库）
- 设计稿本质：单一桌面工具「Param Estimation Toolbox - HAS Behavior」的 16 个窗口状态 → **单页应用**
- 设计语言：tokens 来自 `01-design-tokens.md`（主色 #1a77fd、12px 基础字号、桌面端 1480×980 定宽布局）

## detect_shared 候选确认（摘要）

258 个候选中绝大多数是图标矢量碎片（`形状结合`、`编组`、16px 图标实例）——拒绝，统一由 `AppIcon` 占位处理。语义级确认：

| 候选 | 出现 | AI 确认 |
| --- | --- | --- |
| `Light/icon/16px/*`、`Icon/*` 系列 | ~400 | 采用 → `AppIcon`（name prop 占位） |
| `Light/button/icon/table-icon` | 60 | 采用 → `IconButton` |
| `选中/未选中` 复选实例 | ≥20 处 | 采用 → `AppCheckbox` / `AppRadio` |
| `Light/Input/drop-down` | 全部下拉 | 采用 → `AppSelect` |
| `Light/Input/normal/activated` | Algorithm 弹窗 11+ | 采用 → `AppInput` |
| LOGO + 标题 + close 弹窗头 | 7 个弹窗 | 采用 → `AppDialog` |
| 表格（表头+同构行+滚动条） | 6 处 | 采用 → `DataTable` |
| 主/次按钮对（primary/default） | 全部弹窗 | 采用 → `AppButton` |
| 灰底+蓝条进度 | 状态栏×16 | 采用 → `AppProgressBar` |
| 图表卡片（图例+曲线占位） | 5 处 | 采用 → `ChartPlaceholder`（TODO 图表库） |
| 图标矢量碎片（形状结合/编组/BOOLEAN_OPERATION） | ~200 | 拒绝（图标内部实现细节） |

## 模块划分与路由表

| 模块 | 来源画板 | 路由 | 说明 |
| --- | --- | --- | --- |
| `param-estimation` | 全部 16 画板 | `/`（唯一路由） | 单页桌面工具；16 画板 = 本页的状态组合 |

路由退化为 1 条是 16 份分析的一致结论（左导航/主 Tab 均为组件集变体 = 页内状态；画板间差异均为弹层有无）。保留 Router 以便未来扩展。

## 公共组件清单（src/components/）

| 组件 | Props | Emits | Slots | 说明 |
| --- | --- | --- | --- | --- |
| `AppDialog` | `title`, `width?` | `close` | `default`, `footer` | 弹窗壳：logo+标题+×，无遮罩（设计稿无遮罩） |
| `AppButton` | `type: 'primary'\|'default'`, `disabled?` | `click` | `default` | 主 #1a77fd / 次 #eeeff1 |
| `AppCheckbox` | `checked`, `label?`, `disabled?` | `update:checked` | — | 16px 方框+对勾 |
| `AppRadio` | `checked`, `label` | `update:checked` | — | Algorithm 弹窗 6 组 |
| `AppSelect` | `value`, `options`, `placeholder?` | `update:value`, `change` | — | 下拉（English、Dataset、Result 等） |
| `AppInput` | `value`, `type?`, `disabled?` | `update:value` | — | 24px 高数值输入 |
| `IconButton` | `icon`, `disabled?`, `active?` | `click` | — | 工具栏 24×24 图标按钮 |
| `AppIcon` | `name`, `size?` | — | — | 图标占位（CSS 绘制简单图标 + TODO） |
| `DataTable` | `columns`, `rows`, `selectedIndex?`, `rowKey?` | `select`, `cell-edit` | `cell`, `header` | 斑马纹、行选中 #e6eeff、纵向滚动 |
| `AppProgressBar` | `percent` | — | — | 状态栏 200×4 |
| `ChartPlaceholder` | `title?`, `legends`, `series?` | — | `toolbar` | 折线图占位（虚线框+图例+TODO） |

## 模块私有组件（src/modules/param-estimation/components/）

- 骨架：`AppTitleBar`、`AppToolBar`、`SideNav`（4 项竖排导航）、`MainTabs`（5 页签）、`StatusBar`
- 左侧面板：`ParametersPanel`、`PortsPanel`、`DatasetsPanel`、`ResultsPanel`
- 主区页签视图：`ConvergenceMonitor`、`ReportView`、`SimulationResponse`、`ParameterSensitivity`、`ManualTuning`
- 弹窗：`CloseToolboxDialog`、`ParametersDialog`（空态/填充/含数组卡片）、`AddParametersDialog`、`ArrayTableEditorDialog`、`AlgorithmDialog`、`DatasetWorkspaceDialog`、`ApplyResultDialog`
- 其他：`MetricCard`（Report 指标卡）

## 画板 → 状态映射（实现对照表）

| 画板 | 状态 | 实现 |
| --- | --- | --- |
| 容器-2 | 基准：Parameters 面板 + Convergence Monitor | 默认渲染 |
| 容器-1 | 基准 + Close toolbox 确认 | `CloseToolboxDialog`（标题栏 × 触发） |
| 容器-7 | Ports 面板 + Report 页签 | nav=ports, tab=report |
| 容器-8 | Datasets 面板 + Simulation response | nav=datasets, tab=simulation |
| 容器-9 | Parameter Sensitivity 页签 | tab=sensitivity |
| 容器-10 | Manual tuning 页签 | tab=manual-tuning |
| 容器-385/11/396 | Parameters 弹窗（空/填充/含数组卡片） | `ParametersDialog` 三态 |
| 容器-387 | + Add parameters 二级弹窗 | `AddParametersDialog` |
| 容器-438/439 | + 1D Array Table Editor | `ArrayTableEditorDialog` |
| 容器-390/391 | Algorithm 设置弹窗 | `AlgorithmDialog` |
| 容器-392 | Dataset workspace 弹窗 | `DatasetWorkspaceDialog` |
| 容器-394 | Apply estimation result 弹窗 | `ApplyResultDialog` |

## 状态划分（Pinia）

| Store | 范围 | 内容 |
| --- | --- | --- |
| `useUiStore` | 模块 | activeNav、activeTab、7 个弹窗 visible、当前选中数据集/结果/参数行 |
| `useEstimationStore` | 模块 | 参数表（9 行 mock）、迭代历史、指标（RMSE/Cost/Iterations）、敏感度表、结果列表 Result#1–4、runState、progress |
| `useDatasetStore` | 模块 | 12 个数据集（Fit/Validate 勾选）、数据集参数、曲线 mock |

## 交互接线总表（Phase 7 依据）

| 触发 | 动作 | 置信度 |
| --- | --- | --- |
| 标题栏 × | 打开 CloseToolboxDialog | 高 |
| 左侧导航 4 项 | ui.activeNav 切换（页内） | 高 |
| 主区 5 页签 | ui.activeTab 切换（页内） | 高 |
| 参数面板 ✎ 按钮 | 打开 ParametersDialog | 高 |
| ParametersDialog: Add parameters | 打开 AddParametersDialog | 高 |
| AddParameters: Apply | 勾选项并入参数表，关弹窗 | 高 |
| 数组卡片 Detailed edit | 打开 ArrayTableEditorDialog | 高 |
| 工具栏齿轮/算法图标 | 打开 AlgorithmDialog | 中 |
| Datasets 行点击 | 打开 DatasetWorkspaceDialog | 中 |
| 结果行操作 | 打开 ApplyResultDialog | 中 |
| ▶/■ Run/Stop | runState 切换 + 进度条 mock | 中 |
| Language 下拉 | 语言切换（mock，仅英文文案） | 中 |
| 表格行点击 | 行选中 | 高 |
| 各复选框/单选/输入 | v-model 绑定 | 高 |
| 窗口 min/max | 装饰（Web 无语义）+ TODO | 低 |

## 样式策略

- tokens：`artifacts/tokens.css` 全量引入；禁用硬编码色值/字号。
- 布局：应用骨架定宽 1480×980 居中（桌面工具形态），flex 布局；弹窗 `position:fixed` 居中无遮罩（设计稿如此）+ `--shadow-dialog`。
- 图表：ChartPlaceholder 占位，TODO 待用户决定是否引入图表库。
- 图标：AppIcon 以 CSS/字符近似，TODO 待图标库。
- 设计稿原文笔误（`competed Iteration`、`Apply to modle`、`paramter` 等）按原文保留并记 TODO。

## 用户确认

- [x] 模块划分与路由（单模块单路由）
- [x] 公共组件清单与契约
- [x] 状态划分
- 确认人/时间：用户 / 2026-07-26（会话内确认）

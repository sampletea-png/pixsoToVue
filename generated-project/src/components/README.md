# 公共组件

只放**跨模块复用**的组件（由 detect_shared.py 候选 + AI 语义确认产生）。
模块私有组件放 `src/modules/<m>/components/`。

契约见 `artifacts/03-architecture.md`「公共组件清单」；样式全部使用 `src/styles/tokens.css` 变量。

| 组件 | 用途 |
| --- | --- |
| `AppDialog` | 弹窗壳：logo 占位 + 标题 + 右上 ×，fixed 居中无遮罩，footer slot 右对齐按钮组 |
| `AppButton` | 主（#1a77fd）/次（#eeeff1）按钮 |
| `AppCheckbox` | 16px 方框 + 对勾复选框，`v-model:checked` |
| `AppRadio` | 单选圈，选中项标签主色高亮，`v-model:checked` |
| `AppSelect` | 自定义下拉（点击展开、点击外部收起），`v-model:value` |
| `AppInput` | 24px 高紧凑输入框，`v-model:value` |
| `IconButton` | 工具栏 24×24 图标按钮，支持 active 高亮 |
| `AppIcon` | 内联 SVG 简笔图标集（name 切换），未知名回退首字母方块（TODO: 图标库） |
| `DataTable` | 斑马纹表格：sticky 表头、行选中、纵向滚动、cell/header slot |
| `AppProgressBar` | 状态栏 200×4 进度条（percent 0–100） |
| `ChartPlaceholder` | 图表占位：图例色点行 + 虚线框 + toolbar slot（TODO: 图表库） |

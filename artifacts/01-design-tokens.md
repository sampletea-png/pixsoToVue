# 01 - 设计 Tokens

> 由 extract_tokens.py 生成骨架；**该设计稿未定义任何 Pixso 变量/样式**（0 variables, 0 styles），
> 因此 AI 按 skill 规则处理「待 AI 判断」：从 163 份 DSL 中挖掘高频样式值，派生 tokens（见下）。

## CSS Variables（tokens.css）

已写入 `artifacts/tokens.css`，派生自 DSL 频次统计：

| 类别 | 变量 | 值 | 依据 |
| --- | --- | --- | --- |
| 底色 | `--color-bg` | #f2f2f2 | 出现 7714 次 |
| 面板底 | `--color-bg-subtle` | #fafafa | 3752 次 |
| 卡片/弹窗 | `--color-surface` | #ffffff | 3427 次 |
| 主文本 | `--color-text` | #0f0f0f | 5208 次 |
| 次级文本 | `--color-text-secondary` / `--color-text-muted` / `--color-text-disabled` | #666 / #888 / #89929c | 280/694/690 次 |
| 图标 | `--color-icon` | #5a6c86 | 1422 次（工具栏图标） |
| 边框 | `--color-border` / `--color-border-strong` / `--color-border-input` | #eeeff1 / #dcdce0 / #ccc | 896/196/210 次 |
| 主色 | `--color-primary` | #1a77fd | 402 次（主按钮） |
| 选中底 | `--color-primary-light` | #e6eeff | 420 次（选中行） |
| 信息蓝 | `--color-info` | #43a1f9 | 210 次（图表） |
| 成功/危险/警告 | `--color-success` / `--color-danger` / `--color-warning` | #47d7a7 / #ff3838 / #ebeb3d | 图表与状态色 |
| 字号 | `--font-size-base/md/lg` | 12/14/16px | 频次 6164/36/58 |
| 字重 | regular 400 / bold 700 | — | DSL fontWeight |
| 圆角 | `--radius-sm/base/md` | 2/4/6px | 频次 62/628/168 |
| 阴影 | `--shadow-dialog` | 0 8px 50px rgba(0,0,0,.12) | 弹窗 DROP_SHADOW radius 50 |

## 待 AI 判断（已处理）

- variable_sets / variables / local_styles 均为空 → 已改用 DSL 挖掘派生，无遗留未识别片段。
- 注意：DSL 中存在 UI kit 组件实例（如 `Light/Input/drop-down`）与图标资源（`assetType:"icon"`，如 `Icon/installer/close`），说明设计者部分使用了组件库——Phase 2/3 应优先复用这些语义线索。
- rgba(255,254.7,254.7,1)（2694 次）为近白浮点噪点，归并入 `--color-surface`。
- rgba(0,0,0,0) / rgba(255,255,255,0) 为透明占位，不设 token。

## 拉取异常

- （无）

原始数据见 raw/tokens-raw.json。

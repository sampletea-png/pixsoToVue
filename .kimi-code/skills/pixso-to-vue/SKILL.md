---
name: pixso-to-vue
description: 通过本地 Pixso MCP 将设计稿分阶段转换为架构合理的 Vue 项目（Vite+Vue3+TS+Pinia+Router），含组件语义推断、公共组件抽取、交互推断与自我迭代
type: prompt
whenToUse: 当用户要求把 Pixso 设计稿（URL、页面或当前选区）转换/还原/实现为 Vue 项目或前端代码时
version: 0.1.0
---

# pixso-to-vue：Pixso 设计稿 → Vue 项目

把 Pixso 设计稿转换为**架构合理**的 Vue 项目。用户输入：$ARGUMENTS（Pixso URL、页面名称，或留空表示当前选区/全文件）。

## 根本原则（先于一切步骤理解）

1. **范围克制**：模型关注大区域必然导致局部失真。因此本 skill 是一条 9 阶段流水线——任何时刻只处理**一个最小单元**（一页 / 一区域 / 一组件），禁止跨阶段并行思考。
2. **产物落盘**：每个阶段的产出必须写入 `artifacts/` 对应文件，后续阶段**读文件而不是依赖上下文记忆**。这是防失真的第二道防线。
3. **机械步骤必须调脚本**：MCP 通信、URL 解析、DSL/截图拉取、tokens 提取、重复结构检测、脚手架生成、对比报告——一律执行 `${KIMI_SKILL_DIR}/scripts/` 下的脚本，**禁止 AI 手写 curl/手写脚手架/凭印象编造 MCP 返回**。脚本每次执行结果一致；AI 只做语义判断。
4. **AI 的语义职责**：设计稿没有组件概念（输入框可能只是矩形+文本）、没有原型事件（页面间跳转关系隐含）。组件语义、公共组件确认、交互关系，由 AI 按 `references/` 规则推断，并标注置信度。
5. **门禁**：Phase 0（范围）、Phase 3（架构）必须与用户确认后才能继续；Phase 8（视觉验收）未通过不得宣告完成。

## 环境前置检查（Phase 0 之前）

```bash
python ${KIMI_SKILL_DIR}/scripts/mcp_call.py --list
```

失败则告知用户开启 Pixso 桌面端及其 MCP 服务（默认 `http://127.0.0.1:3667/mcp`，可用环境变量 `PIXSO_MCP_URL` 覆盖），排除后再继续。

## 默认产物栈（可被用户要求覆盖）

Vite + Vue 3 + `<script setup>` + TypeScript + Pinia + Vue Router，**不使用第三方 UI 库**（组件按设计稿手写）。若用户指定其他栈，记录下来并在对应阶段替换；`design_to_code` 仅支持 vue/react/html/arkui/flutter，其他栈先生成 vue/html 再人工转译。

## 流水线

### Phase 0 — 设计盘点

```bash
python ${KIMI_SKILL_DIR}/scripts/collect_design.py --url '<用户给的URL>' --out artifacts
# 无 URL 时省略 --url（采集全文件）；范围大时用 --page-ids / --frames 收敛
```

- 脚本产出：`artifacts/raw/`（每画板的 DSL、design_to_code 初稿、截图、区域清单）与 `artifacts/00-inventory.md` 骨架。
- AI 职责：通读 inventory，补全【】项（规模评估、产品类型），**与用户确认转换范围**（全量 / 指定页面 / 指定画板）。范围未确认，停止。

### Phase 1 — 设计 Tokens

```bash
python ${KIMI_SKILL_DIR}/scripts/extract_tokens.py --out artifacts
```

- 产出 `artifacts/01-design-tokens.md` 与 `artifacts/tokens.css`。
- AI 职责：只处理 md 中「待 AI 判断」的未识别片段；禁止手写 tokens。

### Phase 2 — 逐页分析（每页独立一轮，禁止一次看多页）

对每个画板（参照 `templates/page-analysis.md`）：

1. 看整页截图 `artifacts/raw/<页>/<画板>.png` 划分功能区域（头部/表单/列表/图表…）。
2. **一次只读一个区域**的 DSL：`artifacts/raw/<页>/regions/<画板>/<区域>.dsl.json`，结合区域在截图中的视觉，按 `${KIMI_SKILL_DIR}/references/component-inference.md` 推断每个区域应使用的语义组件（矩形+文本 → 输入框等）。
3. 按 `${KIMI_SKILL_DIR}/references/interaction-inference.md` 推断该页的交互与跳转（标注置信度）。
4. 写入 `artifacts/02-analysis/<画板>.md`：区域树、语义组件清单、复用候选、交互推断表。
5. 完成一页再开始下一页。

### Phase 3 — 架构规划（门禁）

```bash
python ${KIMI_SKILL_DIR}/scripts/detect_shared.py --raw artifacts/raw --out artifacts/03-shared-candidates.md
```

- AI 职责：逐条确认候选（采用/拒绝 + 组件名）；汇总全部 `02-analysis/*.md`，参照 `${KIMI_SKILL_DIR}/references/architecture.md` 与 `templates/architecture-doc.md` 产出 `artifacts/03-architecture.md`：模块划分、路由表、公共组件清单（props/slots 定义）、store 划分、样式策略。
- **与用户确认架构**。未确认不得进入编码。

### Phase 4 — 脚手架

```bash
python ${KIMI_SKILL_DIR}/scripts/scaffold_vue.py <目标目录> --name <项目名> \
    --modules <架构确认的模块,逗号分隔> --tokens artifacts/tokens.css
```

禁止手写脚手架。生成后提醒用户 `npm install`（本机无 Node 时说明即可）。

### Phase 5 — 公共组件（一次一个）

按 `03-architecture.md` 的公共组件清单，**一次只实现一个组件**到 `src/components/`：props/slots/emits 来自 Phase 2 变体分析，样式用 tokens.css 变量，禁用硬编码色值/字号。每个组件完成后再做下一个。

### Phase 6 — 页面实现（一次一页，页内一次一区域）

对每个模块页面：

1. 读该页 `artifacts/02-analysis/<画板>.md`。
2. **一次只实现一个区域**：区域初稿取自 `artifacts/raw/<页>/<画板>.vue.txt`（design_to_code 已生成），按架构重构——公共组件替换为 `<组件>` 调用、样式改用 tokens 变量、语义化标签与命名。
3. 重复结构（列表项）必须用 `v-for` + 数据驱动，禁止复制粘贴静态重复。
4. 整页完成后对照该页截图自查一遍，再开始下一页。

### Phase 7 — 交互接线

- 按各页分析中的交互推断表实现路由跳转、事件、表单提交流（Pinia store / router push）。
- 低置信度项：实现为合理默认 + 代码 `TODO` 注释，并汇总成清单告知用户取舍。

### Phase 8 — 视觉验收（门禁）

```bash
python ${KIMI_SKILL_DIR}/scripts/compare_report.py --design artifacts/raw --impl <实现截图目录> \
    --out artifacts/08-compare-report.html
```

- 逐页对照设计稿截图与实现截图（项目可运行时用浏览器截图；无法运行时向用户说明，以逐区域代码-截图对照代替）。
- 发现差异 → 回到 Phase 6 对应区域修复（仍然一次一区域）。全部通过后告知用户。

### Phase 9 — 自我迭代（必须执行）

按 `${KIMI_SKILL_DIR}/references/self-iteration.md`：

1. 在仓库 `iterations/` 写本次复盘日志（格式见 `iterations/README.md`）。
2. 提出修订建议：**不稳定的 AI 手工环节优先沉淀为新脚本**，其次修订 references/SKILL.md。
3. 经用户确认后应用修订，递增本文件 frontmatter 的 `version`。

## 资源索引

- 脚本：`${KIMI_SKILL_DIR}/scripts/`（每个脚本 `--help` 查看用法）
- MCP 工具速查：`${KIMI_SKILL_DIR}/references/mcp-tools.md`
- 组件语义推断规则：`${KIMI_SKILL_DIR}/references/component-inference.md`
- 交互推断规则：`${KIMI_SKILL_DIR}/references/interaction-inference.md`
- 目标架构约定：`${KIMI_SKILL_DIR}/references/architecture.md`
- 自我迭代协议：`${KIMI_SKILL_DIR}/references/self-iteration.md`
- 产物模板：`${KIMI_SKILL_DIR}/templates/`

# 目标 Vue 项目架构约定

产物的架构必须体现**模块、公共组件、状态、路由**的清晰分层。脚手架由 `scripts/scaffold_vue.py` 生成，本文档约束其后的所有代码组织。

## 目录结构

```
src/
├── modules/               # 业务模块（每个画板/页面一个模块）
│   └── <module>/
│       ├── index.vue      # 模块入口页面（路由组件）
│       ├── components/    # 仅本模块使用的私有组件
│       └── store.ts       # 模块私有状态（需要时）
├── components/            # 跨模块公共组件（detect_shared 候选 + 语义确认）
│   ├── AppButton.vue
│   ├── FormInput.vue
│   └── ...
├── router/index.ts        # 路由表（模块懒加载）
├── stores/                # 全局共享状态（跨模块数据：用户、字典、全局 UI）
├── styles/
│   ├── tokens.css         # 设计 tokens（extract_tokens.py 生成，勿手写）
│   └── base.css           # reset + 全局基础样式
└── utils/
```

## 分层规则

1. **页面 ≠ 大文件**：`modules/<m>/index.vue` 负责组装区域与接线，区域级 UI 拆为模块私有组件（单文件超过约 200 行必须拆分）。
2. **公共组件的准入**：只有 detect_shared 候选且跨模块 ≥2 处复用的结构，才进 `src/components/`；仅本模块用的留在模块内。禁止"可能有用就抽"。
3. **公共组件的契约**：每个公共组件显式声明 `defineProps` / `defineEmits` / `slots`，props 来自 Phase 2 变体分析（不同画板中该结构的差异点即 props）。
4. **样式纪律**：颜色、字号、间距、圆角一律 `var(--*)` 引用 tokens；组件样式用 `scoped`；页面布局用 flex/grid，**禁止用 design_to_code 初稿里的绝对定位平铺**（初稿仅作结构与内容的底稿，布局必须按语义重写）。
5. **数据流**：页面内状态用 `ref/reactive`；跨页面共享用 Pinia；mock 数据集中在模块 `store.ts` 或 `<script setup>` 顶部，为后续接真实 API 留口。
6. **命名**：模块/路由 kebab-case；组件 PascalCase；props camelCase；CSS 类 kebab-case。

## design_to_code 初稿的正确用法

`artifacts/raw/**/<画板>.vue.txt` 是**底稿不是成品**：

- 取：层级结构、文本内容、样式数值。
- 改：绝对定位 → 语义布局；硬编码色值/字号 → tokens 变量；重复块 → `v-for`；无语义 div → 语义标签/公共组件。
- 丢：与设计意图无关的机器命名、冗余嵌套。

## 架构文档（Phase 3 产物）必须包含

模块划分表、路由表、公共组件清单（含 props/slots 契约）、store 划分、样式策略——模板见 `templates/architecture-doc.md`。架构经用户确认后才允许编码。

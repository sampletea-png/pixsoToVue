# pixsoToVue

将 Pixso 设计稿转换为架构合理的 Vue 项目的通用 Skill（Kimi Code 项目级 Skill）。

## 这是什么

本仓库提供 `pixso-to-vue` skill：通过本地 Pixso MCP 服务读取设计稿，按 **9 阶段流水线** 分步生成 Vite + Vue 3 + TypeScript + Pinia + Vue Router 项目。核心设计原则：

- **分步骤、克制范围**：每阶段只处理一个最小单元（一页 / 一区域 / 一组件），中间产物全部落盘，避免模型一次性关注过大区域导致局部失真。
- **确定性环节脚本化**：MCP 调用、DSL 拉取、tokens 提取、重复结构检测、脚手架生成等机械步骤由 Python 脚本（仅标准库）完成，每次执行结果一致。
- **AI 只做语义判断**：组件语义推断（矩形+文本 → 输入框）、公共组件确认、交互关系推断、架构规划。
- **自我迭代**：每次运行结束复盘，不稳定环节优先沉淀为脚本，其次修订文档，skill 版本随迭代递增。

## 前置条件

1. Pixso 桌面端运行中，且其 MCP 服务已开启（默认 `http://127.0.0.1:3667/mcp`）。
2. Python 3.10+（脚本仅用标准库，无需安装任何依赖）。
3. Kimi Code CLI（skill 以此为运行环境）。

## 使用方式

在本仓库目录下启动 Kimi Code，然后：

```
/skill:pixso-to-vue <Pixso设计稿URL 或 页面名称 或 留空使用当前选区>
```

skill 位于 `.kimi-code/skills/pixso-to-vue/`，目录结构：

```
.kimi-code/skills/pixso-to-vue/
├── SKILL.md            # 主编排：9 阶段流水线
├── scripts/            # 确定性脚本（Python3 标准库）
├── references/         # 推断规则 / 架构约定 / 迭代协议
└── templates/          # 各阶段产物模板
```

## 迭代日志

每次运行的复盘记录在 `iterations/`，skill 据此持续改进自身。详见 `iterations/README.md`。

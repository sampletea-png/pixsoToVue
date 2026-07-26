# 03 - 项目架构

> 由 AI 在 Phase 3 填写，**经用户确认后才允许进入编码阶段**。
> 输入：全部 `02-analysis/*.md` + `03-shared-candidates.md`（detect_shared.py）

## 概述

- 项目名：【】 目标目录：【】
- 技术栈：Vite + Vue3 + `<script setup>` + TS + Pinia + Vue Router（默认，或用户指定：【】）

## 模块划分与路由表

| 模块（kebab-case） | 来源画板 | 路由 | 说明 |
| --- | --- | --- | --- |
| 【home】 | 【容器 1】 | `/home` | 【】 |

## 公共组件清单（src/components/）

| 组件名 | 来源（候选哈希/画板） | Props | Emits | Slots | 说明 |
| --- | --- | --- | --- | --- | --- |
| 【AppButton】 | 【】 | 【type, disabled】 | 【click】 | 【default】 | 【】 |

（仅单个模块使用的组件不进此表，放模块私有 components/）

## 状态划分（Pinia）

| Store | 范围（全局/模块） | 状态内容 | 来源 |
| --- | --- | --- | --- |

## 交互接线总表（Phase 7 执行依据）

| 页面 | 触发 | 动作 | 置信度 |
| --- | --- | --- | --- |

## 样式策略

- tokens：`tokens.css` 变量清单要点（主色/字号阶梯/间距阶梯）：【】
- 布局方式（flex/grid，禁用绝对定位平铺）：确认

## 用户确认

- [ ] 模块划分与路由
- [ ] 公共组件清单与契约
- [ ] 状态划分
- 确认人/时间：【】 修改意见：【】

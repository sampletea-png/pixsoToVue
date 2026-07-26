# Pixso MCP 工具速查（实测清单）

服务地址：默认 `http://127.0.0.1:3667/mcp`（streamable HTTP，环境变量 `PIXSO_MCP_URL` 可覆盖）。
**一律通过 `scripts/mcp_call.py` 调用**，不要手写 HTTP 请求。

```bash
python scripts/mcp_call.py --list                      # 列出工具
python scripts/mcp_call.py <tool> '<json-args>'        # 调用
python scripts/mcp_call.py --parse-url '<pixso-url>'   # 解析 item-id / page-id
```

## 实测载荷特性（重要）

- 多数工具的结果在 `result.content[]` 中：文本载荷是 **JSON 字符串**（需二次 `json.loads`）；`get_screenshot`/`take_screenshot` 返回 `type=image` 的 base64 项。
- 工具级错误以 `isError: true` + 文本返回（不是 JSON-RPC error），`mcp_call.py` 已转为异常。
- `fetch_context` 的 `include_schema` 为**必填**布尔。
- Pixso URL 中的 id 需 URL-decode：`item-id=1:2`、`page-id=61%3A1` → `61:1`。guid 形如 `"123:456"`。

## 转换流程常用工具（按用途分组）

### 结构盘点
| 工具 | 用途 | 关键参数 |
| --- | --- | --- |
| `fetch_context` | 当前画布/选区/组件/变量/样式概况 | `include_schema`(必填), `include_map` |
| `get_top_level_frames` | 列出页面（type=page）或指定页的顶层画板（type=frame） | `type`, `pageIds` |
| `query_nodes` | 按模式/id 批量查节点 | `nodeIds`, `patterns`, `searchDepth` |

### 代码与结构生成
| 工具 | 用途 | 关键参数 |
| --- | --- | --- |
| `design_to_code` | **首选**。生成 UI 代码，原生支持 vue | `guids`(数组，空数组=当前选区), `clientFrameworks` |
| `get_node_dsl` | 节点 DSL（fallback；区域级结构分析用） | `guid`, `simplify`(默认 true 为 compact) |
| `get_variants` | 组件集变体 | `guid` |
| `refine_generated_code` | 生成代码再优化 | `refinementTags`(A响应式/B CSS变量/C Tailwind/D DRY/E 设计系统) |

### 视觉
| 工具 | 用途 |
| --- | --- |
| `get_screenshot` | 单节点 PNG 预览（base64） |
| `take_screenshot` | 视觉验收对比，一次最多 3 个节点 |
| `get_export_image` | 导出 PNG/JPEG/SVG/PDF，返回临时 URL |

### 设计系统
| 工具 | 用途 |
| --- | --- |
| `get_variable_sets` / `get_variables` / `read_variables` | 变量（颜色/字号 token 来源） |
| `get_local_styles` / `get_remote_styles` / `read_styles` | 样式库 |
| `get_all_components` / `read_components` | 设计稿已有组件（优先复用） |
| `load_guidelines` | 官方指南（topic: code/web-app/mobile-app/design-system…） |

## 注意

- `design_to_code` 的 `guids` **必须是数组**，即使只有一个节点；不要传原始 URL，先提取 item-id。
- 多画板时 `get_screenshot` 逐画板单独调用，不传数组。
- 写类工具（`apply_design`、`set_*`、`write_*`、`create_instance`、`code_to_design`）在 pixso-to-vue 转换流程中**不应使用**——流程只读设计稿。

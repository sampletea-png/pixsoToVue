#!/usr/bin/env python3
"""extract_tokens.py —— Phase 1：把 Pixso 变量/样式确定性地映射为 design tokens。

用法：
    python extract_tokens.py [--out artifacts] [--include-remote]

输出：
    <out>/raw/tokens-raw.json     # 原始 variables/styles（排查用）
    <out>/01-design-tokens.md     # 人类可读的 tokens 清单
    <out>/tokens.css              # :root CSS variables（Phase 4 拷入目标项目 src/styles/）

映射规则（确定性）：
    颜色        -> --color-<slug>
    字号        -> --font-size-<slug>
    字重        -> --font-weight-<slug>
    间距/圆角   -> --spacing-<slug> / --radius-<slug>
    阴影/效果   -> --shadow-<slug>
无法识别的原始数据保留在 tokens-raw.json 并在 md 中列出，交 AI 判断。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcp_call import DEFAULT_SERVER, McpClient, McpError  # noqa: E402


def slug(name: str) -> str:
    s = re.sub(r"[^0-9A-Za-z一-鿿]+", "-", str(name).strip().lower())
    return re.sub(r"-+", "-", s).strip("-") or "unnamed"


def norm_color(value) -> str | None:
    """把各种颜色表示归一为 #rrggbb(aa) 或 rgba()。无法识别返回 None。"""
    if isinstance(value, str):
        v = value.strip()
        if re.fullmatch(r"#[0-9a-fA-F]{3,8}", v) or v.startswith(("rgb", "hsl")):
            return v
        return None
    if isinstance(value, dict):
        # 常见：{r:0-1,g:0-1,b:0-1,a:0-1} 或 {r:0-255,...}
        if all(k in value for k in ("r", "g", "b")):
            r, g, b = value["r"], value["g"], value["b"]
            a = value.get("a", 1)
            scale = 1 if max(r, g, b) <= 1 else 255
            r, g, b = (round(r * 255 / scale), round(g * 255 / scale), round(b * 255 / scale))
            if a is not None and a < 1:
                return f"rgba({r},{g},{b},{round(a, 3)})"
            return f"#{r:02x}{g:02x}{b:02x}"
        if "hex" in value:
            return norm_color(value["hex"])
    return None


def walk(value, path=""):
    """生成 (jsonpath, 值) 遍历任意嵌套结构。"""
    yield path, value
    if isinstance(value, dict):
        for k, v in value.items():
            yield from walk(v, f"{path}.{k}" if path else k)
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from walk(v, f"{path}[{i}]")


def nearest_name(data: dict, path: str) -> str:
    """根据路径前缀在原始数据里找最近的 name 字段，作为 token 名。"""
    parts = re.split(r"\.|\[|\]", path)
    parts = [p for p in parts if p and not p.isdigit()]
    node = data
    for p in parts[:-1]:
        if isinstance(node, dict) and p in node:
            node = node[p]
            if isinstance(node, dict) and isinstance(node.get("name"), str):
                return node["name"]
        elif isinstance(node, list) and p.isdigit():
            node = node[int(p)]
    if isinstance(node, dict) and isinstance(node.get("name"), str):
        return node["name"]
    return parts[-1] if parts else "token"


def extract(raw: dict) -> tuple[dict, list]:
    """从原始数据提取 tokens。返回 ({css_var: value}, 未识别片段列表)。"""
    tokens: dict[str, str] = {}
    unknown: list[str] = []
    for source_name, data in raw.items():
        if not isinstance(data, (dict, list)):
            unknown.append(f"{source_name}: 非结构化载荷（前 200 字符）: {str(data)[:200]}")
            continue
        for path, value in walk(data):
            if isinstance(value, dict) and "name" not in value:
                continue
            name = slug(nearest_name({source_name: data}, f"{source_name}.{path}"))
            lower_path = path.lower()
            color = norm_color(value)
            if color and any(k in lower_path for k in ("color", "fill", "stroke", "paint", "background")):
                tokens.setdefault(f"--color-{name}", color)
            elif color and isinstance(value, str) and value.startswith("#"):
                tokens.setdefault(f"--color-{name}", color)
            elif isinstance(value, (int, float)) and "fontsize" in lower_path.replace("-", ""):
                tokens.setdefault(f"--font-size-{name}", f"{value}px")
            elif isinstance(value, (int, float)) and "fontweight" in lower_path.replace("-", ""):
                tokens.setdefault(f"--font-weight-{name}", str(int(value)))
            elif isinstance(value, (int, float)) and any(k in lower_path for k in ("spacing", "gap", "padding")):
                tokens.setdefault(f"--spacing-{name}", f"{value}px")
            elif isinstance(value, (int, float)) and "radius" in lower_path:
                tokens.setdefault(f"--radius-{name}", f"{value}px")
    return tokens, unknown


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default="artifacts")
    parser.add_argument("--include-remote", action="store_true", help="同时拉取远程库样式")
    parser.add_argument("--server", default=DEFAULT_SERVER)
    parser.add_argument("--timeout", type=float, default=120.0)
    args = parser.parse_args()

    client = McpClient(server=args.server, timeout=args.timeout)
    out = Path(args.out)
    raw_dir = out / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    raw: dict = {}
    errors: list[str] = []

    def pull(key: str, tool: str, payload: dict):
        try:
            text = client.call_text(tool, payload)
            try:
                raw[key] = json.loads(text)
            except json.JSONDecodeError:
                raw[key] = text
        except Exception as e:  # noqa: BLE001
            errors.append(f"{tool}: {e}")
            print(f"[警告] {tool} 失败: {e}", file=sys.stderr)

    pull("variable_sets", "get_variable_sets", {})
    pull("variables", "get_variables", {})
    pull("local_styles", "get_local_styles", {})
    if args.include_remote:
        pull("remote_styles", "get_remote_styles", {})

    (raw_dir / "tokens-raw.json").write_text(
        json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")

    tokens, unknown = extract(raw)

    # tokens.css
    css_lines = [":root {"]
    css_lines += [f"  {k}: {v};" for k, v in sorted(tokens.items())]
    css_lines.append("}")
    (out / "tokens.css").write_text("\n".join(css_lines) + "\n", encoding="utf-8")

    # 01-design-tokens.md
    md = ["# 01 - 设计 Tokens", "",
          "> 由 extract_tokens.py 生成；AI 不手写本文件，缺漏项在下方「待 AI 判断」补充。",
          "", "## CSS Variables（tokens.css）", "",
          "| 变量 | 值 |", "| --- | --- |"]
    md += [f"| `{k}` | `{v}` |" for k, v in sorted(tokens.items())]
    md += ["", "## 待 AI 判断（脚本无法识别的原始片段）", ""]
    if unknown:
        md += [f"- {u}" for u in unknown]
    else:
        md.append("- （无）")
    md += ["", "## 拉取异常", ""]
    md += [f"- {e}" for e in errors] if errors else ["- （无）"]
    md += ["", "原始数据见 raw/tokens-raw.json。"]
    (out / "01-design-tokens.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"[完成] tokens {len(tokens)} 个，未识别 {len(unknown)} 段，异常 {len(errors)} 条 → {out}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except McpError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

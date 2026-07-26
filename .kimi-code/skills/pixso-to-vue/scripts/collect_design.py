#!/usr/bin/env python3
"""collect_design.py —— Phase 0/2 的机械采集：把设计稿原始数据按固定结构落盘。

用法：
    python collect_design.py                          # 采集当前文件全部页面
    python collect_design.py --url '<pixso-url>'      # 按 URL（自动解析 page-id / item-id）
    python collect_design.py --page-ids 0:1,0:2       # 只采集指定页面
    python collect_design.py --frames 1:2,1:3         # 只采集指定画板（跳过页面枚举）
    python collect_design.py --out artifacts --framework vue --no-code --no-screenshot

输出结构（确定性）：
    <out>/raw/pages.json                       # get_top_level_frames(type=page) 原始结果
    <out>/raw/<页面名>/frames.json             # 该页顶层画板列表
    <out>/raw/<页面名>/<画板名>.dsl.json       # 画板整体 DSL（compact）
    <out>/raw/<页面名>/<画板名>.<vue>.txt      # design_to_code 原始输出
    <out>/raw/<页面名>/<画板名>.png            # 画板截图（尽量保存）
    <out>/raw/<页面名>/<画板名>.regions.json   # 画板直接子节点（区域）清单
    <out>/raw/<页面名>/regions/<画板名>/<区域名>.dsl.json   # 逐区域 DSL（限制单次范围）
    <out>/00-inventory.md                      # 盘点骨架（AI 补全评估列）

每一步失败不会中断整体，错误汇总到 <out>/raw/_errors.json。
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcp_call import McpClient, McpError, parse_pixso_url  # noqa: E402


def slug(name: str) -> str:
    """把页面/画板名转成安全的文件名片段（保留中文）。"""
    name = re.sub(r'[\\/:*?"<>|\s]+', "-", str(name).strip())
    return name.strip("-") or "unnamed"


def dump_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_text_json(text: str):
    """Pixso 工具的文本载荷通常是 JSON 字符串；解析失败则原样返回。"""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return text


def save_image_result(client: McpClient, result: dict, dest: Path, errors: list) -> bool:
    """get_screenshot / get_export_image 的完整 result 尽量落成 PNG 文件。

    支持三种载荷：content 中 type=image 的 base64 项；text 项内 JSON 含 base64；含 localhost 临时 URL。
    """
    dest.parent.mkdir(parents=True, exist_ok=True)

    def write_b64(value: str) -> bool:
        try:
            dest.write_bytes(base64.b64decode(value))
            return True
        except Exception:  # noqa: BLE001
            return False

    def fetch_url(url: str) -> bool:
        try:
            with urllib.request.urlopen(url, timeout=client.timeout) as resp:
                dest.write_bytes(resp.read())
            return True
        except Exception as e:  # noqa: BLE001
            errors.append({"step": "download-image", "url": url, "error": str(e)})
            return False

    def try_text(text: str) -> bool:
        data = load_text_json(text)
        if isinstance(data, dict):
            for key in ("base64", "data", "image"):
                value = data.get(key)
                if isinstance(value, str) and len(value) > 100 and not value.startswith("http"):
                    if write_b64(value):
                        return True
            for key in ("url", "imageUrl", "src"):
                if isinstance(data.get(key), str) and data[key].startswith("http"):
                    return fetch_url(data[key])
        elif isinstance(data, str):
            match = re.search(r"https?://\S+", data)
            if match:
                return fetch_url(match.group(0).rstrip('"\')}'))
        return False

    for item in result.get("content", []):
        if not isinstance(item, dict):
            continue
        if item.get("type") == "image" and isinstance(item.get("data"), str):
            if write_b64(item["data"]):
                return True
        elif item.get("type") == "text" and isinstance(item.get("text"), str):
            if try_text(item["text"]):
                return True
    errors.append({"step": "save-image", "dest": str(dest), "error": "无法识别的图像载荷格式"})
    return False


def extract_regions(dsl) -> list[dict]:
    """从画板 DSL 中尽最大努力提取直接子节点（区域）清单：[{id, name, type}]。"""
    regions: list[dict] = []

    def node_info(node) -> dict | None:
        if not isinstance(node, dict):
            return None
        node_id = node.get("id") or node.get("guid") or node.get("nodeId")
        if not node_id:
            return None
        return {"id": str(node_id), "name": node.get("name", ""), "type": node.get("type", "")}

    def children_of(node):
        if isinstance(node, dict):
            for key in ("children", "layers", "items"):
                if isinstance(node.get(key), list):
                    return node[key]
        return []

    roots = []
    if isinstance(dsl, dict):
        if isinstance(dsl.get("roots"), list):
            roots = dsl["roots"]
        elif isinstance(dsl.get("root"), dict):
            roots = [dsl["root"]]
        elif node_info(dsl):
            roots = [dsl]
    elif isinstance(dsl, list):
        roots = dsl

    refs = dsl.get("refsIndex", {}) if isinstance(dsl, dict) else {}

    def resolve(node):
        # compact DSL：子节点可能是 refsIndex 里的 id 引用
        if isinstance(node, str) and isinstance(refs, dict) and node in refs:
            return refs[node]
        return node

    for root in roots:
        root = resolve(root)
        for child in children_of(root):
            child = resolve(child)
            info = node_info(child)
            if info:
                regions.append(info)
    return regions


def collect(args) -> dict:
    client = McpClient(server=args.server, timeout=args.timeout)
    out = Path(args.out)
    raw = out / "raw"
    errors: list[dict] = []

    def step(name: str, fn, default=None):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            errors.append({"step": name, "error": str(e)})
            print(f"[警告] {name} 失败: {e}", file=sys.stderr)
            return default

    # ---- 解析目标页面 ----
    page_ids = list(args.page_ids or [])
    if args.url:
        parsed = parse_pixso_url(args.url)
        if parsed.get("page-id"):
            page_ids.append(parsed["page-id"])
        if parsed.get("item-id") and not page_ids:
            args.frames = list(args.frames or []) + [parsed["item-id"]]

    pages = step("get_top_level_frames(page)",
                 lambda: load_text_json(client.call_text("get_top_level_frames", {"type": "page"})),
                 default=[])
    dump_json(raw / "pages.json", pages)
    if not isinstance(pages, list):
        pages = []

    if page_ids:
        pages = [p for p in pages if str(p.get("pageId")) in page_ids]

    # ---- 指定画板模式 ----
    if args.frames:
        pages = [{"pageId": "_", "pageName": "_selected"}]
        frames_by_page = {"_selected": [{"id": g, "name": g} for g in args.frames]}
    else:
        frames_by_page = {}

    inventory_rows = []

    for page in pages:
        page_name = page.get("pageName", page.get("pageId", "page"))
        page_dir = raw / slug(page_name)

        if page_name in frames_by_page:
            frames = frames_by_page[page_name]
        else:
            frames = step(
                f"get_top_level_frames(frame,{page_name})",
                lambda p=page: load_text_json(client.call_text(
                    "get_top_level_frames",
                    {"type": "frame", "pageIds": [str(p.get("pageId"))]})),
                default=[])
            dump_json(page_dir / "frames.json", frames)
            # frame 结果按 page 嵌套，展平为画板列表
            frames = flatten_frames(frames)

        for frame in frames:
            frame_id = str(frame.get("id") or frame.get("guid") or frame.get("frameId") or "")
            frame_name = frame.get("name") or frame.get("frameName") or frame_id
            if not frame_id:
                errors.append({"step": "frame-without-id", "frame": frame})
                continue
            base = page_dir / slug(frame_name)
            print(f"[采集] {page_name} / {frame_name} ({frame_id})")

            dsl = step(f"get_node_dsl({frame_id})",
                       lambda g=frame_id: load_text_json(client.call_text(
                           "get_node_dsl", {"guid": g, "clientFrameworks": args.framework})))
            if dsl is not None:
                dump_json(Path(str(base) + ".dsl.json"), dsl)

            if not args.no_code:
                code = step(f"design_to_code({frame_id})",
                            lambda g=frame_id: client.call_text(
                                "design_to_code",
                                {"guids": [g], "clientFrameworks": args.framework}))
                if code:
                    Path(str(base) + f".{args.framework}.txt").write_text(code, encoding="utf-8")

            if not args.no_screenshot:
                shot = step(f"get_screenshot({frame_id})",
                            lambda g=frame_id: client.call(
                                "get_screenshot", {"guid": g, "clientFrameworks": args.framework}))
                if shot:
                    save_image_result(client, shot, Path(str(base) + ".png"), errors)

            regions = extract_regions(dsl) if dsl is not None else []
            dump_json(Path(str(base) + ".regions.json"), regions)
            for region in regions:
                r_dsl = step(f"get_node_dsl(region {region['id']})",
                             lambda g=region["id"]: load_text_json(client.call_text(
                                 "get_node_dsl", {"guid": g, "clientFrameworks": args.framework})))
                if r_dsl is not None:
                    r_path = page_dir / "regions" / slug(frame_name) / (slug(region["name"] or region["id"]) + ".dsl.json")
                    dump_json(r_path, r_dsl)

            inventory_rows.append({
                "page": page_name, "frame": frame_name, "guid": frame_id,
                "regions": len(regions),
                "dsl": dsl is not None,
                "screenshot": Path(str(base) + ".png").exists(),
            })

    dump_json(raw / "_errors.json", errors)
    write_inventory(out / "00-inventory.md", inventory_rows, errors)
    print(f"[完成] 画板 {len(inventory_rows)} 个，错误 {len(errors)} 条，输出目录: {out}")
    return {"frames": len(inventory_rows), "errors": len(errors)}


def flatten_frames(frames) -> list[dict]:
    """get_top_level_frames(type=frame) 的结果按 page 嵌套，统一展平。"""
    flat: list[dict] = []
    if isinstance(frames, list):
        for item in frames:
            if isinstance(item, dict) and isinstance(item.get("frames"), list):
                flat.extend(f for f in item["frames"] if isinstance(f, dict))
            elif isinstance(item, dict):
                flat.append(item)
    elif isinstance(frames, dict):
        for value in frames.values():
            if isinstance(value, list):
                flat.extend(f for f in value if isinstance(f, dict))
    return flat


def write_inventory(path: Path, rows: list[dict], errors: list[dict]) -> None:
    lines = [
        "# 00 - 设计盘点",
        "",
        "> 本文件由 collect_design.py 生成骨架，【】内内容由 AI 在 Phase 0 补全。",
        "",
        "## 转换范围",
        "",
        "- 输入：【URL / 选区 / 全文件】",
        "- 与用户对齐的范围：【待确认】",
        "",
        "## 画板清单",
        "",
        "| 页面 | 画板 | GUID | 区域数 | DSL | 截图 | AI 规模评估 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        lines.append(
            f"| {r['page']} | {r['frame']} | {r['guid']} | {r['regions']} "
            f"| {'✓' if r['dsl'] else '✗'} | {'✓' if r['screenshot'] else '✗'} | 【小/中/大】 |"
        )
    lines += [
        "",
        "## 采集异常",
        "",
        f"共 {len(errors)} 条，详见 raw/_errors.json。",
        "",
        "## AI 补全：整体观察",
        "",
        "- 产品类型（后台/移动端/官网…）：【】",
        "- 设计稿一致性风险：【】",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--url", help="Pixso 设计稿 URL（自动解析 page-id / item-id）")
    parser.add_argument("--page-ids", type=lambda s: [x for x in s.split(",") if x], help="逗号分隔的 pageId")
    parser.add_argument("--frames", type=lambda s: [x for x in s.split(",") if x], help="逗号分隔的画板 guid，跳过页面枚举")
    parser.add_argument("--out", default="artifacts", help="输出目录（默认 artifacts）")
    parser.add_argument("--framework", default="vue", choices=["vue", "react", "html", "arkui", "flutter"])
    parser.add_argument("--no-code", action="store_true", help="跳过 design_to_code")
    parser.add_argument("--no-screenshot", action="store_true", help="跳过截图")
    parser.add_argument("--server", default=None, help="MCP 地址（默认读 PIXSO_MCP_URL 或 127.0.0.1:3667）")
    parser.add_argument("--timeout", type=float, default=120.0)
    args = parser.parse_args()

    import mcp_call
    args.server = args.server or mcp_call.DEFAULT_SERVER
    try:
        collect(args)
        return 0
    except McpError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

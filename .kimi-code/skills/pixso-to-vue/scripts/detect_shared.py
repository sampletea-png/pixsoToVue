#!/usr/bin/env python3
"""detect_shared.py —— Phase 3 前置：跨画板 DSL 的重复结构检测（公共组件候选）。

用法：
    python detect_shared.py [--raw artifacts/raw] [--min-count 2] [--min-nodes 3]
                            [--out artifacts/03-shared-candidates.md]

原理（确定性）：
    对每棵 DSL 树中的每个子树计算"规范化哈希"：
        节点类型 + 尺寸分桶 + 子节点哈希序列
    —— 忽略 id、名称、文本内容、颜色等易变属性。
    同一哈希在不同画板/区域出现 >= min-count 次，即列为公共组件候选。

    AI 的职责：阅读本报告，结合语义确认哪些候选真正成为共享组件；
    脚本只保证"相似结构一个不漏、一个不重"。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path


def size_bucket(value) -> str:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "?"
    if v < 24:
        return "xs"
    if v < 64:
        return "s"
    if v < 160:
        return "m"
    if v < 400:
        return "l"
    return "xl"


def is_node(obj) -> bool:
    return isinstance(obj, dict) and ("type" in obj or "children" in obj)


def node_size(node: dict) -> tuple[str, str]:
    box = node.get("absoluteBoundingBox") or node.get("size") or node
    w = box.get("width") if isinstance(box, dict) else None
    h = box.get("height") if isinstance(box, dict) else None
    return size_bucket(w), size_bucket(h)


def children_of(node: dict, refs: dict) -> list:
    children = node.get("children")
    if not isinstance(children, list):
        return []
    return [refs.get(c, c) if isinstance(c, str) else c for c in children]


def subtree_hash(node, refs: dict, memo: dict) -> tuple[str, int]:
    """返回 (哈希, 子树节点数)。忽略易变属性。"""
    obj_id = id(node)
    if obj_id in memo:
        return memo[obj_id]
    if not isinstance(node, dict):
        result = ("leaf", 1)
        memo[obj_id] = result
        return result
    node_type = str(node.get("type", "node")).lower()
    w, h = node_size(node)
    child_hashes = []
    total = 1
    for child in children_of(node, refs):
        ch, cn = subtree_hash(child, refs, memo)
        child_hashes.append(ch)
        total += cn
    digest_src = f"{node_type}|{w}x{h}|" + ",".join(child_hashes)
    result = (hashlib.md5(digest_src.encode()).hexdigest()[:12], total)
    memo[obj_id] = result
    return result


def scan_file(path: Path, min_nodes: int, seen: dict) -> None:
    try:
        dsl = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"[警告] 跳过无法解析的 {path}: {e}", file=sys.stderr)
        return
    refs = dsl.get("refsIndex", {}) if isinstance(dsl, dict) else {}
    if not isinstance(refs, dict):
        refs = {}
    memo: dict = {}

    def visit(node, location: str):
        if not isinstance(node, dict):
            return
        digest, count = subtree_hash(node, refs, memo)
        if count >= min_nodes:
            entry = seen[digest]
            entry["count"] += 1
            entry["type"] = str(node.get("type", "node"))
            entry["nodes"] = count
            if len(entry["examples"]) < 5:
                entry["examples"].append(f"{location} / {node.get('name', '(未命名)')}")
        for i, child in enumerate(children_of(node, refs)):
            visit(child, f"{location}#{i}")

    roots = dsl.get("roots") if isinstance(dsl, dict) else None
    if isinstance(roots, list):
        for i, root in enumerate(roots):
            root = refs.get(root, root) if isinstance(root, str) else root
            visit(root, f"{path.name}#root{i}")
    else:
        visit(dsl, path.name)


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--raw", default="artifacts/raw", help="collect_design.py 的原始数据目录")
    parser.add_argument("--min-count", type=int, default=2, help="最少出现次数（默认 2）")
    parser.add_argument("--min-nodes", type=int, default=3, help="子树最少节点数，过滤琐碎结构（默认 3）")
    parser.add_argument("--out", default="artifacts/03-shared-candidates.md")
    args = parser.parse_args()

    raw_dir = Path(args.raw)
    dsl_files = sorted(raw_dir.rglob("*.dsl.json"))
    if not dsl_files:
        print(f"错误: {raw_dir} 下没有 *.dsl.json，请先运行 collect_design.py", file=sys.stderr)
        return 1

    # seen: hash -> {count, type, nodes, examples, files}
    seen: dict = defaultdict(lambda: {"count": 0, "type": "", "nodes": 0, "examples": [], "files": set()})
    for f in dsl_files:
        before = {k: v["count"] for k, v in seen.items()}
        scan_file(f, args.min_nodes, seen)
        for k, v in seen.items():
            if k not in before or v["count"] > before[k]:
                v["files"].add(f.parent.parent.name if f.parent.name == "regions" else f.parent.name)

    candidates = [
        (digest, info) for digest, info in seen.items()
        if info["count"] >= args.min_count and len(info["files"]) >= 1
    ]
    # 跨文件出现优先，其次按出现次数排序
    candidates.sort(key=lambda kv: (len(kv[1]["files"]), kv[1]["count"]), reverse=True)

    lines = [
        "# 03 - 公共组件候选（detect_shared.py 生成）", "",
        f"- 扫描 DSL 文件：{len(dsl_files)} 个",
        f"- 判定阈值：出现 ≥ {args.min_count} 次且子树 ≥ {args.min_nodes} 节点",
        f"- 候选数：{len(candidates)}", "",
        "> AI 职责：逐条确认候选是否成为共享组件，写入 03-architecture.md；",
        "> 脚本已忽略名称/文本/颜色等易变属性，仅按结构相似判定。", "",
        "| # | 哈希 | 结构类型 | 子树节点数 | 出现次数 | 分布 | 示例位置 | AI 确认 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for i, (digest, info) in enumerate(candidates, 1):
        files = "、".join(sorted(info["files"])[:5])
        examples = "<br>".join(info["examples"])
        lines.append(
            f"| {i} | `{digest}` | {info['type']} | {info['nodes']} | {info['count']} "
            f"| {files} | {examples} | 【采用/拒绝 + 组件名】 |"
        )
    if not candidates:
        lines.append("| - | - | - | - | - | - | 无候选（可降低 --min-count / --min-nodes 重试） | - |")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[完成] 候选 {len(candidates)} 个 → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

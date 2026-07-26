#!/usr/bin/env python3
"""compare_report.py —— Phase 8：设计稿截图 vs 实现截图的并排对比报告。

用法：
    python compare_report.py --design artifacts/raw --impl <实现截图目录> \
        [--out artifacts/08-compare-report.html]

- 按文件名主干（去扩展名）配对两个目录中的 png/jpg/jpeg/webp；
- 设计稿目录兼容 collect_design.py 的结构（递归查找）；
- 生成静态 HTML，逐对并排展示；AI 打开报告逐页看图核对，不做像素 diff。
"""
from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def collect_images(root: Path) -> dict[str, Path]:
    images: dict[str, Path] = {}
    if not root.exists():
        return images
    for path in sorted(root.rglob("*")):
        if path.suffix.lower() in IMAGE_EXTS and path.is_file():
            images.setdefault(path.stem, path)
    return images


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--design", required=True, help="设计稿截图目录（可为 artifacts/raw）")
    parser.add_argument("--impl", required=True, help="实现截图目录")
    parser.add_argument("--out", default="artifacts/08-compare-report.html")
    args = parser.parse_args()

    design = collect_images(Path(args.design))
    impl = collect_images(Path(args.impl))
    if not design:
        print(f"错误: 设计稿目录 {args.design} 中没有图片", file=sys.stderr)
        return 1

    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    matched = sorted(set(design) & set(impl))
    design_only = sorted(set(design) - set(impl))
    impl_only = sorted(set(impl) - set(design))

    def rel(p: Path) -> str:
        return html.escape(p.resolve().as_uri())

    rows = []
    for name in matched:
        rows.append(f"""
<section>
  <h2>{html.escape(name)}</h2>
  <div class="pair">
    <figure><figcaption>设计稿</figcaption><img src="{rel(design[name])}" alt="design"></figure>
    <figure><figcaption>实现</figcaption><img src="{rel(impl[name])}" alt="impl"></figure>
  </div>
  <p class="verdict">AI 核对结论：【一致 / 差异：____】</p>
</section>""")
    for name in design_only:
        rows.append(f"""
<section class="missing">
  <h2>{html.escape(name)}（缺实现截图）</h2>
  <div class="pair">
    <figure><figcaption>设计稿</figcaption><img src="{rel(design[name])}" alt="design"></figure>
    <figure><figcaption>实现</figcaption><p>未提供</p></figure>
  </div>
</section>""")

    doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>视觉对比报告</title>
<style>
  body {{ font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif; margin: 24px; }}
  h1 {{ font-size: 20px; }}
  section {{ border-top: 1px solid #ddd; padding: 16px 0; }}
  .pair {{ display: flex; gap: 16px; align-items: flex-start; }}
  figure {{ margin: 0; flex: 1; }}
  figcaption {{ font-weight: 600; margin-bottom: 8px; }}
  img {{ max-width: 100%; border: 1px solid #ccc; }}
  .missing {{ background: #fff8e6; }}
  .verdict {{ color: #888; }}
</style>
</head>
<body>
<h1>视觉对比报告（compare_report.py 生成）</h1>
<p>配对 {len(matched)} 组；仅设计稿 {len(design_only)} 个；仅实现 {len(impl_only)} 个（{
        "、".join(html.escape(n) for n in impl_only) or "无"}）。</p>
{''.join(rows)}
</body>
</html>
"""
    out.write_text(doc, encoding="utf-8")
    print(f"[完成] 配对 {len(matched)} 组，缺实现 {len(design_only)} 个 → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

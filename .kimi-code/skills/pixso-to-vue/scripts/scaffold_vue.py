#!/usr/bin/env python3
"""scaffold_vue.py —— Phase 4：确定性生成 Vite + Vue3 + TS + Pinia + Router 工程骨架。

用法：
    python scaffold_vue.py <target-dir> [--name my-app] [--modules home,list,detail]
                           [--tokens artifacts/tokens.css]

- 纯模板生成，不访问网络、不执行 npm；生成后由用户在目标目录执行 npm install && npm run dev。
- 已存在的文件不会被覆盖（重复执行安全）；新增模块可再次运行补齐。
- 每个 --modules 里的模块生成 src/modules/<m>/index.vue 并自动注册路由。
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

VUE_VERSION = "^3.5.13"
VITE_VERSION = "^6.0.7"
TS_VERSION = "~5.7.2"
ROUTER_VERSION = "^4.5.0"
PINIA_VERSION = "^2.3.0"


def pascal(name: str) -> str:
    return "".join(part.capitalize() for part in name.replace("_", "-").split("-") if part) or "Module"


def write_file(root: Path, rel: str, content: str, written: list, skipped: list) -> None:
    path = root / rel
    if path.exists():
        skipped.append(rel)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    written.append(rel)


def templates(name: str, modules: list[str]) -> dict[str, str]:
    route_records = ",\n".join(
        f"  {{ path: '/{m}', name: '{m}', component: () => import('@/modules/{m}/index.vue') }}"
        for m in modules
    )
    redirect = f"  {{ path: '/', redirect: '/{modules[0]}' }},\n" if modules else ""

    return {
        "package.json": json.dumps({
            "name": name,
            "private": True,
            "version": "0.1.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vue-tsc -b && vite build",
                "preview": "vite preview",
            },
            "dependencies": {
                "vue": VUE_VERSION,
                "vue-router": ROUTER_VERSION,
                "pinia": PINIA_VERSION,
            },
            "devDependencies": {
                "@vitejs/plugin-vue": "^5.2.1",
                "typescript": TS_VERSION,
                "vite": VITE_VERSION,
                "vue-tsc": "^2.2.0",
            },
        }, indent=2, ensure_ascii=False) + "\n",

        "vite.config.ts": """import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
  },
})
""",

        "tsconfig.json": json.dumps({
            "compilerOptions": {
                "target": "ES2020",
                "useDefineForClassFields": True,
                "module": "ESNext",
                "moduleResolution": "bundler",
                "strict": True,
                "jsx": "preserve",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "esModuleInterop": True,
                "lib": ["ES2020", "DOM", "DOM.Iterable"],
                "skipLibCheck": True,
                "noEmit": True,
                "baseUrl": ".",
                "paths": {"@/*": ["src/*"]},
            },
            "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.vue"],
        }, indent=2) + "\n",

        "index.html": f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{name}</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
""",

        "src/env.d.ts": """/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}
""",

        "src/main.ts": """import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles/tokens.css'
import './styles/base.css'

createApp(App).use(createPinia()).use(router).mount('#app')
""",

        "src/App.vue": """<template>
  <router-view />
</template>

<script setup lang="ts">
</script>
""",

        "src/router/index.ts": f"""import {{ createRouter, createWebHistory }} from 'vue-router'
import type {{ RouteRecordRaw }} from 'vue-router'

const routes: RouteRecordRaw[] = [
{redirect}{route_records}
]

export default createRouter({{
  history: createWebHistory(),
  routes,
}})
""",

        "src/stores/index.ts": """// 全局共享 store 放这里；模块私有状态放 src/modules/<m>/store.ts
export {}
""",

        "src/styles/tokens.css": """:root {
  /* 由 extract_tokens.py 生成 / 由 scaffold_vue.py --tokens 拷贝；勿手写覆盖 */
}

/* 兜底默认值（tokens.css 为空时保证项目可运行） */
:root {
  --color-primary: #1677ff;
  --color-text: #1f2329;
  --color-bg: #ffffff;
  --font-size-base: 14px;
  --radius-base: 6px;
  --spacing-base: 8px;
}
""",

        "src/styles/base.css": """* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  color: var(--color-text);
  background: var(--color-bg);
  font-size: var(--font-size-base);
  font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
}
""",

        "src/components/README.md": """# 公共组件

只放**跨模块复用**的组件（由 detect_shared.py 候选 + AI 语义确认产生）。
模块私有组件放 `src/modules/<m>/components/`。
""",

        "src/utils/index.ts": """export {}
""",

        ".gitignore": """node_modules/
dist/
*.local
.DS_Store
""",

        "README.md": f"""# {name}

由 pixso-to-vue skill 从 Pixso 设计稿生成。

```bash
npm install
npm run dev
```

## 目录约定

- `src/modules/<m>/` —— 业务模块（页面），私有组件与 store 就近放置
- `src/components/` —— 跨模块公共组件
- `src/stores/` —— 全局共享状态
- `src/styles/tokens.css` —— 设计 tokens（来自设计稿变量/样式）
""",
    }


def module_templates(module: str) -> dict[str, str]:
    comp = pascal(module)
    return {
        f"src/modules/{module}/index.vue": f"""<template>
  <div class="{module}-page">
    <!-- TODO: 按 artifacts/02-analysis/{module}.md 逐区域实现 -->
    <h1>{comp}</h1>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.{module}-page {{
  min-height: 100vh;
}}
</style>
""",
        f"src/modules/{module}/components/README.md": f"# {comp} 模块私有组件\n\n仅本模块使用的组件放这里。\n",
    }


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("target", help="目标项目目录")
    parser.add_argument("--name", help="项目名（默认用目录名）")
    parser.add_argument("--modules", default="", help="逗号分隔的模块名（路由），如 home,list,detail")
    parser.add_argument("--tokens", help="extract_tokens.py 生成的 tokens.css，拷贝为 src/styles/tokens.css")
    args = parser.parse_args()

    root = Path(args.target)
    name = args.name or root.resolve().name
    modules = [m.strip() for m in args.modules.split(",") if m.strip()]

    written: list[str] = []
    skipped: list[str] = []

    for rel, content in templates(name, modules).items():
        # --tokens 提供时跳过默认 tokens.css，由拷贝步骤写入真实 tokens
        if rel == "src/styles/tokens.css" and args.tokens:
            skipped.append(rel + "(默认模板，由 --tokens 替代)")
            continue
        write_file(root, rel, content, written, skipped)
    for m in modules:
        for rel, content in module_templates(m).items():
            write_file(root, rel, content, written, skipped)

    if args.tokens:
        src = Path(args.tokens)
        dest = root / "src/styles/tokens.css"
        if not src.exists():
            print(f"[警告] tokens 文件不存在: {src}", file=sys.stderr)
        elif dest.exists():
            skipped.append("src/styles/tokens.css")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dest)
            written.append("src/styles/tokens.css")

    print(f"[完成] 写入 {len(written)} 个文件，跳过已存在 {len(skipped)} 个 → {root}")
    if skipped:
        print("  跳过: " + ", ".join(skipped))
    print("  下一步: cd 目标目录 && npm install && npm run dev")
    return 0


if __name__ == "__main__":
    sys.exit(main())

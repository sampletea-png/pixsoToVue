#!/usr/bin/env python3
"""Pixso MCP (streamable HTTP) 客户端 —— 所有脚本与 MCP 通信的唯一入口。

仅使用 Python 标准库。可被其他脚本 import，也可直接命令行调用：

    python mcp_call.py --list                          # 列出全部工具
    python mcp_call.py <tool> '<json-args>'            # 调用工具，结果 JSON 打印到 stdout
    python mcp_call.py --parse-url '<pixso-url>'       # 解析 URL 中的 item-id / page-id
    python mcp_call.py <tool> --file args.json         # 从文件读取参数（参数较大时）

环境变量 PIXSO_MCP_URL 可覆盖默认服务地址 http://127.0.0.1:3667/mcp
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_SERVER = os.environ.get("PIXSO_MCP_URL", "http://127.0.0.1:3667/mcp")
PROTOCOL_VERSION = "2025-03-26"


def parse_pixso_url(url: str) -> dict:
    """从 Pixso 设计稿 URL 提取 item-id / page-id（均已 URL-decode）。

    例：https://any-host/app/design/:fileName?item-id=1:2&page-id=61%3A1
    -> {"item-id": "1:2", "page-id": "61:1"}
    """
    query = urllib.parse.urlparse(url).query
    params = urllib.parse.parse_qs(query)
    result = {}
    for key in ("item-id", "page-id"):
        values = params.get(key)
        if values:
            result[key] = urllib.parse.unquote(values[0])
    return result


class McpError(RuntimeError):
    pass


class McpClient:
    """最小可用的 MCP streamable-HTTP 客户端（仅覆盖 tools/list 与 tools/call）。"""

    def __init__(self, server: str = DEFAULT_SERVER, timeout: float = 120.0):
        self.server = server
        self.timeout = timeout
        self.session_id: str | None = None
        self._next_id = 0

    # ---- 底层 ----

    def _rpc_id(self) -> int:
        self._next_id += 1
        return self._next_id

    def _post(self, payload: dict, session_id: str | None = None) -> tuple[dict | None, dict]:
        """发送一条 JSON-RPC 消息。返回 (result_or_none, response_headers)。

        对通知类消息（无 id），服务器返回 202 且无正文，结果为 None。
        """
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        sid = session_id if session_id is not None else self.session_id
        if sid:
            headers["mcp-session-id"] = sid
        req = urllib.request.Request(self.server, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                resp_headers = {k.lower(): v for k, v in resp.headers.items()}
        except urllib.error.URLError as e:
            raise McpError(f"无法连接 MCP 服务 {self.server}: {e}") from e

        if not raw.strip():
            return None, resp_headers

        content_type = resp_headers.get("content-type", "")
        if "text/event-stream" in content_type:
            message = self._parse_sse(raw)
        else:
            message = json.loads(raw)

        if message is None:
            return None, resp_headers
        if "error" in message:
            raise McpError(f"MCP 错误 {message['error'].get('code')}: {message['error'].get('message')}")
        return message.get("result"), resp_headers

    @staticmethod
    def _parse_sse(raw: str) -> dict | None:
        """解析 SSE 流，返回最后一条 event: message 的 data（JSON）。"""
        last_data = None
        event = None
        for line in raw.splitlines():
            if line.startswith("event:"):
                event = line[len("event:"):].strip()
            elif line.startswith("data:"):
                data = line[len("data:"):].strip()
                if event in (None, "message"):
                    last_data = data
        if last_data is None:
            return None
        return json.loads(last_data)

    # ---- 会话 ----

    def connect(self) -> dict:
        """initialize + notifications/initialized，返回 serverInfo/capabilities。"""
        result, headers = self._post({
            "jsonrpc": "2.0",
            "id": self._rpc_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "pixso-to-vue-skill", "version": "1.0.0"},
            },
        }, session_id=None)
        self.session_id = headers.get("mcp-session-id")
        if self.session_id:
            self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return result or {}

    def _ensure_connected(self):
        if self.session_id is None:
            self.connect()

    # ---- 工具 ----

    def list_tools(self) -> list[dict]:
        self._ensure_connected()
        result, _ = self._post({"jsonrpc": "2.0", "id": self._rpc_id(), "method": "tools/list"})
        return (result or {}).get("tools", [])

    def call(self, tool: str, arguments: dict | None = None) -> dict:
        """调用工具，返回 result 字典（含 content 等）；工具级错误抛 McpError。"""
        self._ensure_connected()
        result, _ = self._post({
            "jsonrpc": "2.0",
            "id": self._rpc_id(),
            "method": "tools/call",
            "params": {"name": tool, "arguments": arguments or {}},
        })
        result = result or {}
        if result.get("isError"):
            detail = self._extract_text(result) or json.dumps(result, ensure_ascii=False)
            raise McpError(f"工具 {tool} 调用失败: {detail[:500]}")
        return result

    @staticmethod
    def _extract_text(result: dict) -> str:
        parts = [
            item.get("text", "")
            for item in result.get("content", [])
            if isinstance(item, dict) and item.get("type") == "text"
        ]
        return "\n".join(p for p in parts if p)

    def call_text(self, tool: str, arguments: dict | None = None) -> str:
        """调用工具并把 result.content 中的文本项拼接返回（大多数 Pixso 工具的载荷）。"""
        return self._extract_text(self.call(tool, arguments))


def _main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    args = argv[1:]
    server = DEFAULT_SERVER
    timeout = 120.0

    def take_value(flag: str) -> str | None:
        if flag in args:
            i = args.index(flag)
            value = args[i + 1]
            del args[i:i + 2]
            return value
        return None

    if "--server" in args:
        server = take_value("--server")
    if "--timeout" in args:
        timeout = float(take_value("--timeout"))

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    if args[0] == "--parse-url":
        if len(args) < 2:
            print("用法: python mcp_call.py --parse-url '<pixso-url>'", file=sys.stderr)
            return 2
        print(json.dumps(parse_pixso_url(args[1]), ensure_ascii=False, indent=2))
        return 0

    client = McpClient(server=server, timeout=timeout)

    if args[0] == "--list":
        tools = client.list_tools()
        for t in tools:
            print(f"{t['name']}: {t.get('description', '')[:120]}")
        return 0

    tool = args[0]
    if len(args) >= 3 and args[1] == "--file":
        with open(args[2], encoding="utf-8") as f:
            arguments = json.load(f)
    elif len(args) >= 2:
        arguments = json.loads(args[1])
    else:
        arguments = {}

    result = client.call(tool, arguments)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(_main(sys.argv))
    except McpError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

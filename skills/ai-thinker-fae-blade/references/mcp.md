# 按需接入安信可知识库

官方说明：https://docs.ai-thinker.com/mcp/ 。服务是官方托管的只读 HTTP MCP；“安装”指为当前 AI 工具写入连接配置，不部署本地知识库后端。

## 首次使用

先检查当前会话的工具列表。已有可用的官方知识库工具时直接使用，不必运行安装脚本或更换已有凭据。配置存在但宿主尚未加载时优先重新加载宿主。

需要接入时，以本技能根目录定位脚本：

```text
python <技能根目录>/scripts/blade.py mcp --client codex
python <技能根目录>/scripts/blade.py mcp --client claude
python <技能根目录>/scripts/blade.py mcp --client cursor
```

只执行当前客户端对应的一条。脚本检查用户级配置中同一官方地址的服务（允许不同服务名）；复用已有有效配置，验证失败保留配置并报告。若已有服务被用户禁用，不自动重新启用。已有项目级配置由宿主优先发现，先检查宿主，避免重复安装。

没有配置时，脚本从固定官方页面解析当前公开 Token，先完成 MCP initialize、initialized 和 tools/list，再原子写入配置。旧文件做本机备份，其他服务与设置保留。Token 不写入仓库、日志、命令参数或对话输出；Unix 文件权限设为仅用户可读写，Windows 继承用户配置目录 ACL。

| 客户端 | 写入位置 |
| --- | --- |
| Codex | `CODEX_HOME/config.toml`（设置该变量时），否则 `~/.codex/config.toml` |
| Claude Code | `~/.claude.json` 用户级 `mcpServers` |
| Cursor | `~/.cursor/mcp.json` |

写入后通常需要宿主重新加载。报告“配置已写入、连接探测成功”与“当前会话已经能调用”是两个状态，不要混为一谈。主机沙箱阻止网络/配置写入时通过它提供的正常授权流程，不能绕过限制。

## 尚未重新加载时完成当前查询

脚本提供当前任务的临时调用入口，使用刚保存的配置，不在输出中显示凭据：

```text
python <技能根目录>/scripts/blade.py wiki-tools --client codex
python <技能根目录>/scripts/blade.py wiki-call --client codex --tool <实际列出的工具名称> --arguments-json <符合该工具inputSchema的JSON对象>
```

先读取 `wiki-tools` 返回的描述与 inputSchema，再选择检索与阅读工具。禁止猜测名称或参数。JSON 参数应通过宿主结构化工具传递或正确的 shell 引号传递，不插入客户敏感数据到可见命令历史。调用结果里的 `isError` 为 true 时当作失败，不引用为事实。

官方服务只读，但仍应在调用前查看工具用途；不要向检索接口发送与任务无关的客户信息。检索后读取相关原文，必要时取规格书附件，给出可核对的文档链接与版本。

若页面不再提供唯一可解析的 Token，脚本停止而不修改配置；请用户按官方指引提供自己的凭据或联系安信可支持，不在对话中索取密码。现有凭据失效时报告失效，由用户决定更换。

# My Assistant

一个本地运行的个人 AI 助手学习项目，包含 FastAPI 后端和 Vue 3 前端。当前重点是练习 agent 的基础结构：对话入口、简单工具调用、天气查询、流式返回，以及本地 OpenAI 兼容模型服务接入。

## 功能

- AI 对话：前端发送多轮消息，后端通过 OpenAI 兼容接口调用本地模型。
- 工具调用：当用户在聊天中询问天气时，agent 会先提取城市，再调用天气工具。
- 流式响应：聊天接口使用 `StreamingResponse` 返回模型输出。
- 前后端分离：后端使用 FastAPI，前端使用 Vue 3 + Vite + TypeScript。

## 当前目录

```text
.
├── app/
│   ├── api/
│   │   └── routes/          # FastAPI 路由入口
│   ├── core/                # 配置、启动参数等项目核心设置
│   ├── models/              # Pydantic 请求与响应模型
│   ├── prompts/             # 系统提示词与可复用 prompt
│   ├── services/            # agent 编排、LLM 封装、信息提取等业务逻辑
│   │   └── extractors/      # 从用户输入中抽取结构化信息
│   ├── tools/               # agent 可调用的工具封装
│   └── main.py              # FastAPI 应用入口
├── frontend/
│   ├── src/                 # Vue 前端源码
│   ├── package.json         # 前端依赖与脚本
│   └── vite.config.ts       # Vite 配置与 API 代理
├── .env.example             # 后端环境变量示例
├── pyproject.toml           # 后端项目配置
├── uv.lock                  # 后端依赖锁文件
└── README.md
```

## 为什么这样分

- `api/routes` 只负责 HTTP 协议层，不直接写复杂业务逻辑。
- `services` 放 agent 编排和 LLM 调用，后续可以继续拆 planner、memory、tool router。
- `tools` 放可被 agent 调用的外部能力，比如天气、搜索、文件读写等。
- `models` 放接口输入输出模型，让路由和工具返回值更清晰。
- `core/config.py` 集中管理模型地址、模型名和应用元信息，避免散落在业务代码里。
- `prompts` 单独放提示词，方便后续迭代不同角色或不同任务的 prompt。

## 环境准备

请先确认本机已安装：

- Python 3.14+
- uv
- Node.js 和 npm
- LM Studio 或 Ollama 等 OpenAI 兼容本地模型服务

复制环境变量示例：

```bash
cp .env.example .env
```

按你的本地模型服务修改 `.env`：

```text
LLM_BASE_URL=http://localhost:1234/v1
LLM_API_KEY=lm-studio
CHAT_MODEL=qwen/qwen3.6-35b-a3b
EXTRACTOR_MODEL=qwen3.6
```

## 启动后端

在项目根目录执行：

```bash
uv sync
uv run uvicorn app.main:app --reload
```

后端默认运行在：

```text
http://127.0.0.1:8000
```

接口文档：

```text
http://127.0.0.1:8000/docs
```

## 启动前端

另开一个终端执行：

```bash
cd frontend
npm install
npm run dev
```

前端默认运行在：

```text
http://localhost:5173
```

Vite 已配置代理：前端请求 `/api/chat` 会转发到后端的 `/chat` 接口。

## API 示例

健康检查：

```bash
curl http://127.0.0.1:8000/
```

聊天：

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"你好\"}]}"
```

## 后续适合学习的方向

- 给工具增加统一协议，例如 `name`、`description`、`run()`。
- 增加 conversation memory，把历史消息持久化。
- 把天气意图判断从关键词升级成 LLM 分类。
- 增加测试目录 `tests/`，先覆盖聊天路由和工具格式化逻辑。
- 给前端拆分 `components/`、`composables/`，当页面复杂后再做。

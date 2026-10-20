# 🏢 企业级 AI 智能售后工单中台 (Enterprise AI Ticket Agent)

> 一个基于 **FastAPI + LangChain Agent** 构建的全栈式、高保真、带企业级安全风控的智能客服与工单流转系统。

## 📖 项目背景 (企业痛点)
在传统电商及 SaaS 行业中，售后客服面临着**查单慢、人工建单繁琐、容易引发客诉**的痛点。更为致命的是，如果直接让大语言模型（LLM）接管客服业务，极易产生**“AI 幻觉”**（例如凭空捏造不存在的订单并同意退款），给企业带来直接的资金损失。

本项目旨在通过 **Agentic AI（智能体）** 架构，赋予大模型调用外部后端接口的能力（Function Calling）。AI 不再是单纯的聊天机器人，而是能够**自主查阅真实数据库、核实订单状态、并自动生成后台工单**的虚拟员工，真正实现了“AI 提单 + 人工审核”的商业闭环。

## 🛠️ 核心技术栈
- **Web 后端**：Python, FastAPI, Uvicorn
- **AI 中枢**：LangChain, DeepSeek API (Function Calling, AgentExecutor)
- **数据库**：SQLAlchemy ORM, SQLite (生产环境可无缝切换 MySQL)
- **安全鉴权**：JWT (JSON Web Token), OAuth2PasswordBearer, Bcrypt 密码哈希
- **架构设计**：依赖注入 (Dependency Injection), 路由控制 (Routers), 服务层解耦 (Service Layer)

## ✨ 核心功能与工程亮点 (面试重点)

1. **自主决策的 Agent 智能体**：
   AI 能够根据用户的自然语言，精准提取订单号，自主决定调用 `query_order_tool` 查库，确认订单存在且未退款后，再调用 `refund_order_tool` 建单。彻底告别死板的固定工作流。

2. **物理级“防幻觉”风控机制**：
   通过后端的 `404` 校验拦截，从代码底层切断了 AI 瞎编的可能。如果用户输入了不存在的订单号，数据库直接抛出异常，强制 AI 回复“查无此单”，100% 保障企业资金安全。

3. **工业级无状态鉴权 (JWT)**：
   系统采用 JWT 签发电子通行证。通过 `Depends(auth.get_current_user)` 实现依赖注入，所有核心业务接口均受安全门禁保护。未携带合法 Token 的请求将直接被 `401` 拦截，杜绝数据裸奔。

4. **优雅的代码分层架构**：
   严格按照企业级标准进行代码重构。将接口路由 (`routers/`)、核心业务逻辑 (`services/`) 与数据模型 (`models/`) 完全解耦，告别“一坨代码写到底”的玩具项目。

## 🎬 演示效果 (Demo)
*(请将你在 Swagger 测试 `POST /api/chat/` 接口时，终端打印出 AI 疯狂调用工具的“绿色日志”截图粘贴在这里，极其装X)*

## 🚀 快速启动指南

### 1. 克隆项目并配置虚拟环境
```bash
git clone https://github.com/ChenYian1203/enterprise-ai-ticket-agent.git
cd enterprise-ai-ticket-agent
python -m venv venv
# Windows 激活虚拟环境
venv\Scripts\activate

## 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
## 启动服务
uvicorn main:app --reload

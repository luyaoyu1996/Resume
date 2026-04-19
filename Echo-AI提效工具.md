# Echo - 企业级 AI 产品经理提效工具

## 项目定位

Echo 是马帮 ERP 内部的 AI 提效工具，内嵌于 Coding.net 项目管理平台，面向全体产品经理。从 0→1 到 1→10 由卢耀煜独立负责产品立项、设计、开发。现马帮所有产品经理日常使用该工具提效。

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 需求查重 | 基于 ES 向量检索，自动匹配历史相似需求，避免重复开发 |
| 需求澄清 | AI 对模糊需求进行追问和澄清，暴露隐藏假设 |
| PRD 生成 | 基于澄清后的需求，自动生成结构化 PRD 文档 |
| UI 一键生成 | 基于 PRD 自动生成 UI 原型/设计稿 |

---

## 技术架构

### 前端：mabang-coding-ai-plasmo
- **形态**：Chrome 浏览器扩展（Manifest V3），内嵌于 Coding.net 页面
- **技术栈**：Plasmo 框架 + Vue 3 + TypeScript
- **核心组件**：
  - `ChatDrawer.vue` — AI 对话抽屉（主交互界面）
  - `MessageBubble.vue` — 消息气泡（支持 Markdown 渲染 + 代码高亮）
  - `AttachmentUploader.vue` — 附件上传
  - `Stepper.vue` — 步骤引导（查重→澄清→PRD→UI 流程）
  - `ThinkingIndicator.vue` — AI 思考状态指示
- **核心服务**：
  - `chat-service.ts` — 对话管理
  - `java-service.ts` — 后端 API 调用
  - `n8n-service.ts` — N8N 工作流调用
  - `message-renderer.ts` — 消息渲染（Markdown + highlight.js）
  - `storage-service.ts` — 本地存储管理
- **Composables**：
  - `useChat.ts` — 对话状态管理
  - `useIssues.ts` — 需求数据管理

### 后端：mis-mabang-ai
- **技术栈**：Spring Boot 2.x + Spring Cloud + MyBatis Plus
- **服务端口**：8811，路径 `/mabanggpt`
- **核心中间件**：
  - MySQL — 业务数据
  - Redis + Redisson — 缓存 + 分布式锁
  - Elasticsearch — 消息日志 + 向量知识库（RAG）
  - RocketMQ — 异步消息队列
  - Nacos — 服务注册与配置中心
  - Sa-Token — 认证授权

### AI 集成
| 服务 | 用途 |
|------|------|
| Dify | 主要工作流引擎（LLM 编排），驱动查重→澄清→PRD→UI 流水线 |
| OpenAI GPT-3.5/4 | 直连对话 + Function Calling |
| Claude | 代理调用 |
| Midjourney | UI 图像生成（通过 Discord 中转） |

---

## 核心架构设计

### 责任链模式（后端核心）

**流式回复链（前端主链路）：**
```
CHECK_QUESTION → USER_INFO → CHECK_APP → SUPPLEMENT_MESSAGE(RAG) → GENERATE_STREAM_MESSAGE(SSE)
```

**RAG 知识库流程：**
1. 从 ES 查询最近 5 条历史对话
2. 根据知识库配置查询向量索引
3. ES 向量搜索相似问题
4. 按匹配分数和 Token 数过滤
5. 构建 System Prompt + 上下文注入

### SSE 流式响应
支持 4 种格式兼容：Dify 工作流格式、最终答案格式、OpenAI 兼容格式、增量格式

### 多平台推送
企业微信、钉钉、飞书、马帮 ERP 系统

---

## 项目规模

| 维度 | 数据 |
|------|------|
| 后端 Controller | 23 个 |
| 后端 Service | 65 个 |
| 后端 Mapper | 13 个 |
| 前端组件 | 6 个核心 Vue 组件 |
| 前端服务 | 7 个 TypeScript 服务模块 |
| 数据库表 | 13 张 |
| ES 索引 | 2 类（消息日志按月滚动 + 向量知识库按日期） |

---

## 商业价值

- 全体产品经理日常使用，直接提升需求产出效率
- 需求查重避免重复开发，节省研发资源
- PRD 自动生成减少 PM 文档编写时间
- UI 一键生成缩短设计环节周期
- 从 0→1 独立完成，体现全栈产品 + 技术能力

---

## 简历提炼（草稿）

> **从 0→1 主导企业级 AI 提效工具 Echo 的产品立项、设计与开发**
>
> 基于 Dify + RAG 架构，为马帮全体产品经理打造内嵌于 Coding.net 的 AI 助手，覆盖需求查重（ES 向量检索）、需求澄清、PRD 自动生成、UI 一键生成四大核心能力。前端采用 Plasmo + Vue 3 浏览器扩展，后端 Spring Boot 微服务 + 责任链模式处理 AI 对话流，集成 GPT-4 / Claude / Midjourney 多模型。现已成为马帮产品团队日常提效工具。

---

*文件创建时间：2026-04-12*

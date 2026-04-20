# ④ Echo - 企业级AI产品经理提效工具

**从0→1独立负责产品立项、设计、开发**
时间：2024–2025 | 角色：产品负责人（独立完成）

> 马帮ERP内部AI提效工具，内嵌于Coding.net项目管理平台，现为马帮全体产品经理日常使用。

## 产品设计

- 从0→1独立完成产品立项、需求设计、技术架构、开发落地，覆盖需求查重→需求澄清→PRD自动生成→UI一键生成完整工作流
- 需求查重：基于ES向量检索，自动匹配历史相似需求，避免重复开发，节省研发资源
- 需求澄清：AI对模糊需求进行追问，暴露隐藏假设，提升需求质量
- PRD自动生成 + UI一键生成：基于澄清后的需求自动输出结构化PRD与UI原型，缩短PM文档编写与设计环节周期

## 技术架构

- 前端：Plasmo + Vue 3 浏览器扩展（Manifest V3），内嵌Coding.net页面，零侵入式集成
- 后端：Spring Boot微服务 + 责任链模式处理AI对话流（CHECK_QUESTION → USER_INFO → SUPPLEMENT_MESSAGE(RAG) → GENERATE_STREAM_MESSAGE）
- AI集成：Dify工作流引擎编排LLM流水线，集成GPT-4 / Claude / Midjourney多模型
- RAG知识库：Elasticsearch向量索引，查询历史对话 + 相似需求，按匹配分数和Token数过滤后注入System Prompt
- 中间件：MySQL + Redis + Elasticsearch + RocketMQ + Nacos

## 项目规模

| 维度 | 数据 |
|------|------|
| 后端Controller | 23个 |
| 后端Service | 65个 |
| 数据库表 | 13张 |
| ES索引 | 2类（消息日志按月滚动 + 向量知识库） |
| 前端核心组件 | 6个Vue组件 + 7个TypeScript服务模块 |

## 结果

现为马帮全体产品经理日常使用；需求查重避免重复开发；PRD自动生成显著减少PM文档编写时间

---

> **待确认**
> 1. Echo目前有多少PM在用？有无使用频次/节省时间的数据？
> 2. 需求查重命中率大概是多少？有无可量化的「避免重复开发」案例？
> 3. 这个项目投AI产品岗时作为第一项目，投物流/跨境PM岗时是否放最后或缩减篇幅？

# Echo 项目全貌

> 最后更新：2026-04-07

## 产品定位

Echo 是一个**内嵌在 Coding.net 的 AI 助手浏览器扩展**，专为马帮 ERP 的 PM 提效设计。  
核心场景：PM 在 Coding 上查看 Issue 时，侧边弹出 AI 对话框，辅助需求分析、PRD 撰写、逻辑梳理等工作。

---

## 项目结构

```
C:\project\Echo\
├── mabang-coding-ai-plasmo/   # 前端：Chrome 浏览器扩展
└── mis-mabang-ai/             # 后端：Spring Boot AI 服务
```

---

## 整体架构

```
[Coding.net Issue 页面]
        │
        ▼
[Chrome 扩展 - mabang-coding-ai-plasmo]
  content.ts        → 抓取 Issue 数据（7层策略）
  ui-controller.ts  → 注入按钮 + 悬浮气泡
  ChatDrawer.vue    → 主聊天 UI（Vue 3）
  chat-service.ts   → SSE 流式调用
        │
        ▼
[后端 - mis-mabang-ai]
  DifyController    → 接收请求
  责任链处理         → 验证 / 补充上下文 / 生成回复
  Dify 工作流引擎   → 实际 LLM 调用
        │
        ▼
[Dify / OpenAI / Claude / Midjourney]
```

---

## 前端：mabang-coding-ai-plasmo

### 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Plasmo | 0.90.5 | 浏览器扩展框架（MV3） |
| Vue 3 | 3.5.26 | UI 框架（Composition API） |
| TypeScript | 5.3.3 | 类型安全 |
| markdown-it | 14.1.0 | Markdown 渲染 |
| highlight.js | 11.11.1 | 代码高亮（20+ 语言） |

### 目录结构

```
src/
├── content.ts                  # Content Script 入口（数据抓取核心）
├── popup.vue                   # 扩展弹出页
├── app/
│   └── bootstrap.ts            # Vue 应用挂载
├── components/
│   ├── ChatDrawer.vue          # 主聊天抽屉（核心 UI）
│   ├── MessageBubble.vue       # 消息气泡（Markdown 渲染）
│   ├── AttachmentUploader.vue  # 附件上传
│   ├── Stepper.vue             # 步骤导航
│   ├── ThinkingIndicator.vue   # 思考过程指示器
│   ├── TagRow.vue              # 标签行
│   └── InfoModal.vue           # 需求信息弹框
├── composables/
│   ├── useChat.ts              # 聊天逻辑（消息、发送、历史）
│   ├── useIssues.ts            # 需求数据管理
│   └── useResize.ts            # 侧边栏拖拽调整
├── managers/
│   ├── ui-controller.ts        # UI 控制（按钮、气泡、挂载）
│   └── user-controller.ts      # 用户信息管理（单例，5分钟缓存）
├── services/
│   ├── chat-service.ts         # 聊天 API 调用（SSE 流式）
│   ├── java-service.ts         # Java 后端验证
│   ├── n8n-service.ts          # N8N 工作流调用
│   ├── storage-service.ts      # 本地存储管理
│   ├── attachment-service.ts   # 附件上传
│   ├── message-renderer.ts     # Markdown 渲染
│   ├── api-config.ts           # N8N API 配置（硬编码）
│   └── java-api-config.ts      # Java API 配置（硬编码）
├── constants/
│   ├── step-constants.ts       # 产品流程步骤定义
│   └── gtm-constants.ts        # GTM 赋能流程步骤定义
└── types/
    └── user.ts                 # 用户相关类型
```

### 核心流程

1. `content.ts` 在 Coding 页面注入，通过 7 种方式抓取 Issue 数据
2. 注入"Echo AI助手"按钮和右侧悬浮气泡
3. 点击后挂载 Vue 应用，打开 ChatDrawer 侧边栏
4. 用户选择步骤，发送消息
5. SSE 流式接收 AI 回复，Markdown 渲染展示

### 7 层数据抓取策略（content.ts）

| 层级 | 方式 | 说明 |
|------|------|------|
| 1 | Performance API | 检查已完成的网络请求 |
| 2 | 预加载数据 | 检查全局变量 `__INITIAL_STATE__`、`__NUXT__` |
| 3 | DOM 观察 | 监听动态加载的数据属性 |
| 4 | 请求拦截 | 拦截 XHR 和 Fetch 请求 |
| 5 | 直接 API 调用 | 主动请求 Issue API |
| 6 | 定期检查 | 2秒间隔重试，最多 10 次 |
| 7 | URL 变化监听 | 检测 Issue 切换并刷新数据 |

### 两种工作模式

**需求分析模式（默认）**
```
澄清 → PRD → 逻辑 → UI → 评审
```

**业务赋能模式（GTM）**
```
升级日志 → 使用手册 → SEO推广
```

### 后端调用配置

| 环境 | 地址 | 接口 |
|------|------|------|
| 开发 | `http://localhost:8811/mabanggpt` | `/api/dify/chat` |
| 生产 | `https://n8n.mabangerp.com` | `/webhook/...` |

### SSE 响应格式兼容

```
1. Dify 工作流格式：  {"data": {"outputs": {"answer": "文本"}}}
2. 最终答案格式：     {"answer": "完整文本"}
3. OpenAI 兼容格式：  {"choices": [{"delta": {"content": "文本"}}]}
4. 增量格式：         {"answer": "增量文本"}
```

### 本地存储策略

| Key | 内容 | 限制 |
|-----|------|------|
| `${userId}_${issueId}` | 历史消息 | 最多 20 条 |
| `conversation_${userId}_${issueId}` | 会话 ID | - |
| `echo-sidebar-width` | 侧边栏宽度 | 400-1200px |

---

## 后端：mis-mabang-ai

### 技术栈

| 技术 | 用途 |
|------|------|
| Spring Boot 2.x | 核心框架 |
| Spring Cloud Nacos | 服务注册与配置中心 |
| OpenFeign | 第三方 API 调用 |
| MyBatis Plus | ORM |
| Druid | 数据库连接池 |
| Sa-Token | 认证授权 |
| Elasticsearch | 消息日志 + 向量知识库 |
| Redis | 缓存、会话 |
| RocketMQ | 异步消息队列 |
| jtokkit | Token 精确计数 |
| 腾讯云 COS | 对象存储 |

### 模块结构

```
mis-mabang-ai/
├── mabang-ai-entity/       # 实体层（Entity / DTO / VO / BO）
├── mabang-ai-common/       # 公共模块（枚举、工具、异常、结果包装）
├── mabang-ai-dao/          # 数据访问层（13个 MyBatis Plus Mapper）
├── mabang-ai-service/      # 业务逻辑层（16个 Service 实现 + 16个 Handler）
├── mabang-ai-controller/   # 控制层（23个 Controller）
├── mabang-ai-provider/     # 第三方 API 提供者（OpenFeign 客户端）
└── mabang-ai-startup/      # 启动模块（配置文件）
```

### 核心 API 接口

| Controller | 接口 | 说明 |
|------------|------|------|
| AuthController | `POST /doLogin` | 密码登录 |
| AuthController | `POST /doLoginTemp` | 临时授权码登录 |
| DifyController | `POST /api/dify/chat` | 流式对话（核心） |
| DifyController | `POST /api/dify/validateCodingUser` | 验证 Coding 用户 |
| DifyController | `POST /api/dify/uploadImg` | 上传图片 |
| MessageController | `POST /api/v1/message/replyStreamMessage` | 流式回复 |
| ModelKnowledgeController | `POST /api/v1/modelKnowledge/saveModelKnowledge` | 保存知识库 |
| ModelDataController | - | 模型数据管理 |
| MidjourneyController | - | 图像生成 |

### 责任链处理器（核心设计）

后端使用**责任链模式**处理所有消息，不同场景走不同的 Handler 链：

**流式回复链（前端调用的主链）：**
```
CHECK_QUESTION → USER_INFO_TO_MESSAGE_DTO → CHECK_APP 
→ SUPPLEMENT_MESSAGE → GENERATE_STREAM_MESSAGE
```

**企业微信/钉钉/飞书消息链：**
```
CHECK_QUESTION → CHECK_APP → SET_ACCESS_TOKEN → SAVE_DEFAULT_USER 
→ SUPPLEMENT_MESSAGE → FUNCTION_CALL → GENERATE_MESSAGE 
→ GENERATE_IMAGE → SEND_MESSAGE → SAVE_MESSAGE_LOG
```

**图像生成链：**
```
CHECK_APP → GENERATE_IMAGE_WEB → SET_DISCORD_LOG
```

### 关键 Handler 说明

| Handler | 职责 |
|---------|------|
| CheckQuestion | 验证问题非空 |
| CheckAppHandler | 验证应用配置 |
| UserInfoToMessageDtoHandler | 用户信息注入 |
| SupplementMessageHandler | **RAG 核心**：ES 向量检索 + 知识库注入 |
| FunctionCallHandler | GPT Function Calling 处理 |
| GenerateStreamMessageHandler | 流式消息生成（SSE） |
| GenerateImageHandler | Midjourney 图像生成 |
| SendMessageHandler | 推送到企业微信/钉钉/飞书 |
| SaveMessageLogHandler | 写入 ES 消息日志 |

### RAG 知识库流程（SupplementMessageHandler）

```
1. 从 ES 查询最近 5 条历史对话
2. 根据知识库代码/ID 查询知识库配置
3. ES 向量搜索相似问题
4. 按匹配分数和 Token 数过滤
5. 构建 System Prompt + 上下文注入
```

### AI 集成

| 服务 | 用途 |
|------|------|
| Dify | 主要工作流引擎（LLM 编排） |
| OpenAI GPT-3.5/4 | 直连对话 + Function Calling |
| Claude | 代理调用 |
| Midjourney | 图像生成（通过 Discord 中转） |

### 多平台推送支持

- 企业微信（WeChat Work）
- 钉钉（DingTalk）
- 飞书（Feishu）
- 马帮 ERP 系统

### 数据库设计

**MySQL 主要表：**

| 表名 | 说明 |
|------|------|
| db_user | 用户信息 |
| db_app_config | 应用配置 |
| db_chat_history | 聊天历史 |
| db_gpt_config | GPT 配置 |
| db_model_knowledge | 知识库配置 |
| db_discord_config | Discord 配置 |
| db_customer | 客户信息 |
| db_role / db_menu | 角色权限 |

**Elasticsearch 索引：**

| 索引 | 说明 |
|------|------|
| `mis_message_logs-YYYYMM` | 消息日志（按月滚动） |
| `mis_model_data-YYYYMMDD` | 向量知识库 |

### 环境配置

| 环境 | Profile | Nacos 地址 |
|------|---------|-----------|
| 本地 | loc | - |
| 开发 | dev | dev-nacos.mabangerp.com |
| 测试 | stage | - |
| UAT | uat | - |
| 生产 | prd | - |

服务端口：`8811`，应用名：`mis-mabang-ai-service`

---

## 当前架构的潜在问题

| 问题 | 风险 | 建议 |
|------|------|------|
| N8N 作为生产网关 | 低代码工具承担生产流量，稳定性差、调试困难 | 考虑直连 Java 后端或用 API Gateway |
| 前端 URL 硬编码 | `api-config.ts` / `java-api-config.ts` 手动切换，容易出错 | 用环境变量或 Plasmo 的 env 机制 |
| ES 索引按日期命名 | `mis_model_data-20230517` 跨索引查询复杂 | 使用别名（alias）统一查询入口 |
| Discord 中转 Midjourney | 链路长（后端→Discord→Midjourney），稳定性差 | 评估是否有官方 API 替代 |
| 知识库索引时间戳固定 | 数据更新后索引名不变，可能查到旧数据 | 建立索引版本管理机制 |

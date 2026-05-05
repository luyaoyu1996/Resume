# ⑤ OpenClaw（大龙虾）— AI智能采购员

**从0→1独立负责采购模块产品设计与全栈开发**
时间：2026.3–至今 | 角色：采购模块负责人（独立设计+开发）

> OpenClaw是马帮的AI数字员工平台（覆盖广告/采购/刊登等电商全链路），采购模块（大龙虾）为核心模块之一，目标将采购员日均400+单逐一检查的重复工作交给AI自动处理。当前内部电商公司及品牌客户试用中。

---

## 产品设计

### 设计理念

核心设计哲学：**AI做异常处理层，CLI只负责取数据和写数据，判断逻辑全交给AI**。

- 正常单子马帮ERP自动跑，大龙虾只处理异常（运费不对 / 价格不符 / 没货 / 量需审核）
- CLI不做业务决策，只提供原始数据，AI Agent结合skill判断
- 属性无法自动匹配的订单标记为需人工处理，不强行自动化

### 调研驱动

基于采购员现场调研（2026-04，受访人：盛志豪/姚总），梳理采购员4大核心流程：

| 流程 | 现状痛点 | AI介入方式 |
|------|----------|------------|
| 跟单 | 人工逐单查物流状态，每天重复检查 | AI按规则自动判断"几天没发货算需要催"，批量发催货话术 |
| 找替代 | 手工搜1688/百度，对比价格质量 | AI图搜+多源比价，自动推荐替代供应商 |
| 降本 | 人工翻历史采购价，判断哪些SKU该降 | AI拉取未降价清单，自动生成降价沟通话术 |
| 采购量计算 | Excel手算日均销量×安全天数-在途 | AI拉取销量/库存/在途数据，结合趋势自动审量 |

### 采购全链路5阶段覆盖

```
【下单前】
  └─ export-data          ← 拉取待采购SKU原始数据（销量/库存/供应商）
                             AI结合skill判断：采多少、要不要降量、要不要取消

【下单】两步操作
  └─ place-order          ← 在马帮创建采购单，返回groupId
  └─ place-1688-order     ← 用groupId在1688平台下单，返回1688订单号

【审批】
  └─ get-approval-data    ← 拉取马帮单价 vs 1688实际价、运费数据
                             AI结合skill判断：偏差多少算异常
  └─ mark-approval        ← 将审核结论写回马帮采购单
  └─ send-followup        ← 发改价/改运费话术

【跟单】下单2天后触发
  └─ get-pending-shipment ← 拉取已付款采购单（物流状态/距付款天数）
                             AI结合skill判断：几天没发货算需要催
  └─ send-followup        ← 批量发催货话术
  └─ extract-reply        ← 收取供应商回复
  └─ update-purchase-note ← 将回复内容回写马帮采购单备注

【降本】周期性
  └─ get-no-price-drop    ← 拉取长期未降价SKU清单
                             AI判断：哪些值得谈、目标价多少
  └─ send-followup        ← 发降价沟通话术
```

---

## 系统架构

### 五层架构

```
OpenClaw WebUI (doubao-seed-2.0-pro，AI Agent调度平台)
  │  调用 moc purchase <command>
  ▼
moc-cli (Python CLI，AI的手和脚)
  │  Authorization: Bearer <employeeToken>
  ▼
moc-cli-service-gateway (Go, :10008，鉴权+路由转发)
  │  解析employeeToken → 注入X-Gateway-*请求头 → 查路由表转发
  ▼
moc-purchase-business (Python FastAPI, :28788，采购业务服务)
  │  从X-Gateway-*头读取员工身份（EmployeeContext）
  ▼
马帮gwapi / 1688平台
  │  HMAC-SHA256签名认证
  │  V2 API（pur-do-add-purchase等）
  │  page-proxy（代理马帮前端页面接口）
```

### 涉及项目

| 项目 | 语言 | 职责 | 我的角色 |
|------|------|------|----------|
| moc-cli | Python | CLI命令行工具，AI的手和脚 | 采购命令开发 |
| moc-cli-service-gateway | Go | 鉴权+路由转发网关 | 使用方 |
| moc-purchase-business | Python (FastAPI) | 采购业务后端服务 | **独立设计+开发** |
| OpenClaw | - | AI Agent运行平台（WebUI + 调度） | 采购skill设计 |

### 两种API调用模式

| 场景 | API名称 | 调用方式 |
|------|----------|----------|
| 马帮标准V2 API | `pur-do-add-purchase`等 | `_v2_client.post(api=..., data={...})` |
| 马帮前端页面接口（无标准API） | `purchasenew.xxx`等 | page-proxy代理：`_v2_client.post(api="digital-human-page-api", data={url, method, body, headers})` |

---

## 技术实现

### 马帮OpenAPI签名对接

马帮gwapi采用HMAC-SHA256签名认证，需要精确还原PHP服务端的验签逻辑：

- 只排序顶层key（模拟PHP ksort不递归），`data`内部字段保持原顺序
- `employeeToken`参与签名，签名body和发送body必须是同一个字符串
- `timestamp`和`version`为字符串类型，`companyId`和`employeeId`为int类型
- 列表字段（如`stockList`）需`json.dumps()`序列化为JSON字符串传入

开发过程中逐一排查7个签名/参数问题，从"请求加密验证失败"到成功调通。

### 1688平台下单（page-proxy机制）

1688下单无标准API，需通过page-proxy代理调用马帮前端页面接口，模拟浏览器行为：

**两步操作**：
1. **查询下单参数**（`purchasenew.create1688OrderShowNew`）：用groupId后6位查询，从返回的JSON取结构化数据（purchaseId/ali1688SupplyId/targetWarehouseId），从HTML中用正则提取hidden input里的11个1688 SKU字段
2. **提交下单**（`purchasenew.create1688OrderNew`）：组装40+个form字段的`application/x-www-form-urlencoded`请求体，key用purchaseId动态拼接（如`923350quantity[]`、`9230831688ProductSkuId[]`）

**关键设计决策**：
- 用`digital-human-page-api`（不带v2），因为v2有url host校验会拒绝`www.mabangerp.com`
- 错误处理区分`success=true`但无`ali1688OrderId`的"部分失败"情况

### 网关鉴权机制

Go网关自动从`Authorization`头提取employeeToken → 调用`employee-token/resolve`解析身份 → 注入`X-Gateway-*`请求头（Employee-Token/Employee-Id/Company-Id/Cluster-Id/Token-Expire-Time）→ 业务服务零感知鉴权。

支持多集群配置（公有云cluster_id=1 / 私有云cluster_id=2），通过环境变量区分不同的appkey/app_secret。

---

## 接口实现状态

| 接口 | 功能 | 业务服务 | CLI | 状态 |
|------|------|----------|-----|------|
| `place-order` | 马帮创建采购单 | ✅ 真实API | ✅ | **已调通** |
| `place-1688-order` | 1688平台下单 | ✅ 真实API | ✅ | **已调通** |
| `export-data` | 导出待采购数据 | Mock | ✅ | 待接入 |
| `get-approval-data` | 获取审核数据 | ❌ | ❌ | 待新增 |
| `mark-approval` | 标记审核结果 | ❌ | ❌ | 待新增 |
| `get-pending-shipment` | 获取待催货单 | ❌ | ❌ | 待新增 |
| `send-followup` | 发催货/降价话术 | Mock | ✅ | 待接入 |
| `extract-reply` | 收取供应商回复 | Mock | ✅ | 待接入 |
| `update-purchase-note` | 回写采购备注 | Mock | ✅ | 待接入 |
| `get-no-price-drop` | 未降本SKU清单 | ❌ | ❌ | 待新增 |

---

## 项目规模

| 维度 | 数据 |
|------|------|
| 后端路由 | 10个采购接口 |
| Pydantic模型 | 8组请求/响应模型 |
| 核心工具模块 | 6个（api_client / ali1688_order / context / response / alibaba_aoxia / jwt_auth） |
| 测试脚本 | 5个本地测试脚本（demo/） |
| CLI命令 | 10个Click命令文件 |
| 部署 | Docker (python:3.11-slim) + Go网关 |

---

## 结果

- 马帮下单 + 1688下单全链路已调通上线，内部电商公司及品牌客户试用中
- 目标覆盖采购团队日均**数千单**异常自动化处理（异常单占比约20-30%，含运费偏差/价格不符/缺货/量需审核）
- 采购全链路5阶段10个CLI命令完成产品设计，2个已调通真实API，4个已有路由待接入，4个待新增

# ⑧ AI Coding Skill — 物流/海外仓对接提效工程化

**关键词**：AI Coding / Cursor Rules / 对接标准化 / 团队级提效
时间：2025–2026 | 角色：产品负责人（设计 + 推动落地）

> 把海外仓（HWC）与直发物流（DM）对接里「易重复、易踩坑、依赖老人带」的经验，沉淀为可检索、可复用、可交给 AI 约束执行的 Skill + 公共文档，让研发少猜、少返工、少无效沟通。

---

## 一、背景与痛点

马帮物流中台每年新增数百家海外仓和物流商对接，每次对接涉及：
- 21个接口方法的实现（授权/仓库/渠道/商品/入库/出库/退货/运费）
- 数十个扩展字段的SQL配置
- 跨国场景的字段规则（地址拼接/COD币种/省州二字码/巴西CNPJ等）

**没有Skill之前的问题**：

| 痛点 | 典型表现 |
|------|---------|
| 知识在人头里 | 入库用`skuCode`、出库用`sku`这类规则靠口口相传 |
| 流程长易漏步 | 只改了ServiceImpl，忘了枚举注册/扩展字段SQL/库表配置 |
| 排障成本高 | MQ Topic、XXL-Job、回调路径不清，全局搜半天 |
| AI协作低效 | Cursor生成的代码不符合仓库惯例，需要2-4轮才收敛 |

---

## 二、做了什么

### 2.1 海外仓对接Skill（HWC）

**标准实现顺序**（21个接口方法，按优先级排序）：

```
授权(getAccessToken) → 仓库列表 → 渠道列表 → 商品同步
→ 创建入库单 → 查询入库单 → 取消入库单
→ 创建出库单 → 查询出库单 → 取消出库单
→ 创建退货单 → 查询退货单 → 取消退货单
→ 库存同步 → 运费查询
```

**高频踩坑点显式列出**：
- 入库单商品用`skuCode`，出库单用`sku`——两者不能混用
- 地址缺字段时的三种拼接策略：缺门牌号用`address1AndDoor`，缺详细地址2用`address1And2`，两者都缺用`address1And2AndDoor`
- COD（货到付款）：`isCod=1`时金额和**币种**必须同时传，漏币种会导致对账失败
- 尺寸单位统一**cm**，重量单位统一**g**，与海外仓不同时必须在Convert层明确换算
- `createType`区分：1=交运（海外仓提供面单），2=预报（需从label取面单传给海外仓）
- 回调接口必须给`referenceId`赋值，否则无法关联ERP单据

**配置上线标准化**（CONFIGURATION.md）：
- `Db_Logistics`建表SQL模板
- `db_logistics_extend`扩展字段清单（20+个字段，按功能分组）
- `torkenJson`授权字段配置
- `warehouseJson`仓库信息配置
- `forecastChannel`预报渠道配置
- `Db_LogisticsChannel`交运渠道SQL

### 2.2 直发物流对接Skill（DM）

**5步标准流程**：

```
Step1: DmLogisticsType枚举注册（logisticsId + @Service名称）
Step2: ServiceImpl实现（@Service名称必须与枚举getService()一致）
Step3: API类（ApiLog记录请求/响应，ApiEnum定义接口路径）
Step4: Convert转换器（MapStruct，@Named约束，禁止source="."）
Step5: Pojo实体（按API文档定义，@JSONField处理snake_case）
```

**最高频漏配错误**：`@Service`名称与`DmLogisticsType.getService()`不一致，导致`LogisticsController`路由失败，下单报NPE。Skill中把这条规则放在Step1最显眼的位置。

**跨国场景字段约定**：
- 发件人地址取`ShipperDto.address`，收件人取`address1`/`address2`
- 沙特必须传`shortAddress`，不能只传长地址
- 电话优先`getTelephone()`，空时才用`getMobile()`
- 美国/德国/法国/巴西等省州要求二字码，用`StateConverterUtil.getProvinceCode()`
- 巴西CNPJ：签约主体与开票方不一致时必须与运营确认，禁止自行混用

### 2.3 AI Coding约束层（Cursor Rules）

把上述规则写入`.cursor/rules/*.mdc`，Cursor Agent在生成/修改代码时自动约束：
- MapStruct必须用`@Named`+`qualifiedByName`，禁止`source="."`
- Java判空统一用`Sys.isNull`/`Sys.isNotNull`，不用`== null`
- 集合单元素用`Sys.listOf(x)`，不用`Collections.singletonList`
- 禁止多字段兜底猜测映射，契约不明时输出`needs confirmation`停止编造

---

## 三、提效结果

| 维度 | 使用前 | 使用后 | 说明 |
|------|--------|--------|------|
| 新仓对接周期 | 5-7天 | 2-4天 | 普通场景，日历天 |
| 首联调前返工比例 | 40-60% | ≤25% | 配置类漏项明显减少 |
| Code Review惯例类comment占比 | 25-40% | 8-15% | Review聚焦业务正确性 |
| AI协作收敛轮次 | 2-4轮 | 0-1轮 | Cursor按Skill约束生成 |

---

## 四、核心设计思路

**提效的本质不是少写代码，而是少写错代码、少配漏、少无效沟通。**

对物流这种强外部依赖、强配置驱动的业务，时间差往往体现在「返工与等待」上：
- 代码写完了才发现漏配`db_logistics_extend`扩展字段
- 联调时才发现`@Service`名称和枚举不一致
- Code Review反复补惯例，而不是聚焦业务正确性

Skill解决的是这些「不该犯的错」，让研发的注意力集中在「业务逻辑是否正确」上。

---

## 五、与Echo的区别

| | Echo（PM提效工具） | AI Coding Skill |
|--|------------------|-----------------|
| 服务对象 | 产品经理 | 后端研发 |
| 核心能力 | RAG+工作流（PRD生成/UI生成/帮助文档） | Cursor Rules约束（代码规范/对接流程/配置清单） |
| 提效场景 | 需求文档生产 | 物流商对接开发 |
| 形态 | 浏览器插件+Dify工作流 | `.cursor/rules/*.mdc` + `public-docs/SKILL.md` |

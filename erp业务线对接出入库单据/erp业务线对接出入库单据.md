[TOC]

### 1 入库单

### 1.1 获取入库单详情 `POST` `业务线提供请求接口`

**请求参数**

```json
{
    //可扩展字段
    "companyId": 123123, //公司id //必填
    "clusterId": "1", //  1 公有云 2 私有云 //必填
    "referenceId": "I202101010001", //入库单号 //必填,
    "orderType": 1, //1:入库单 2:出库单
    "sourceId": 3,  //3:手工出入库 5:fba 7:temu 9:ERP调拨单 21 加工单 23 新版手工出入库 29 新版ERP调拨单 31 采购单 33 采购退货出库  
}
```

**返回参数**

```json
{
    "code": 200,
    "msg": "success",
    "data": {
        "referenceId": "HWC3609972408280001", //入库单号 //必填,
        "sourceId": 3,  //3:手工出入库 5:fba 7:temu 9:ERP调拨单
        "warehouseId": 1111, //仓库id 必填
        "warehouseCode": "BOS", //仓库编码 //非必填
        "requestId": "eyJwcm9kdWN0aW9uIjoicHJkIiwiY29tcGFueUlkIjozNjA5OTcsInRyYWRlSWQiOjQwNTQsInRpbWUiOjE3MjQ4Mzk3NjZ9", //请求ID 后续各种回调都以此为准 //必填 长度最长255位
        "describe": "26", //描述 //非必填
        "extendInfo": { 
            //扩展信息 //非必填
        },
        "shipper": { //发件人信息 必填
            "address": "727 BREA NYON ROAD SUITE 8", //地址 必填
            "city": "WALNUT", //城市 必填
            "companyName": "FLY", //公司名称 非必填
            "contactName": "Angus", //联系人 必填
            "countryCode": "US", //国家编码 必填
            "doorCode": "", //门牌号 非必填
            "email": "22082@qq.com", //邮箱 非必填
            "mobile": "626-000-0000", //手机 必填
            "telephone": "626-000-0000", //电话 非必填
            "province": "CA", //省 必填
            "state": "WALNUT", //州 非必填
            "vatNumber": "", //税号 非必填
            "zipCode": "91789" //邮编 非必填
        },
        "packageList": [
            {
                "skuList": [
                    { 
                        //字段可扩展
                        "lineNo": 1, //行号
                        "erpSkuType": 1, //商品编码类型 int : 1库存；2组合； //必填
                        "erpSku": "BOS-0562-1", //ERP商品编码 //必填
                        "erpSkuId": 1234, //ERP商品ID int //必填
                        "erpSkuName": "圣浪压缩袋-70*50cm", //sku名称 //非必填
                        "erpPictureUrl": "erpPictureUrl", //erp图片
                        "thirdSkuCode": "BOS-0562-1", //第三方商品编码 ：fbamsk；temu 平台sku //必填
                        "quantity": 160, //数量 int//必填
                        "specification": "", //规格 //非必填
                        "unit": "PCS", //单位 //非必填
                        "purchasePrice": 0.00, //采购价 //非必填
                        "retailPrice": 0.00, //零售价 //非必填
                        "declaredValue": 0.00, //sku申报价值 币种固定USD //非必填
                        "declaredCode": "12223111", //sku海关编码 //非必填
                        "declaredNameCn": "测试", //sku申报中文名 //非必填
                        "declaredNameEn": "TEST", //sku申报英文名 //非必填
                        "weight": 100, //重量 必填
                        "weightUnit": "G" //重量单位 必填
                    }
                ],
                "packNo": "MB01", //包裹号
                "length": 10.00, //长度
                "width": 10.00, //宽度
                "height": 10.00, //高度
                "sizeUnit": "CM", //尺寸单位
                "weight": 1000, //重量
                "weightUnit": "G" //重量单位
            }
        ]
    }
}
    
{
    "code": 500,
    "msg": "失败，原因：xxxx",
}
```

### 1.2 创建入库单回调 `POST` `业务线提供请求接口`

**请求参数**

```json
{
    "requestId": "eyJwcm9kdWN0aW9uIjoicHJkIiwiY29tcGFueUlkIjozNjA5OTcsInRyYWRlSWQiOjQwNTQsInRpbWUiOjE3MjQ4Mzk3NjZ9", //请求ID 
    "status": "1", //状态 1:创建成功 2:创建失败 //必填
    "inboundSn": "RD31470428116615", //三方仓入库单号 //必填
    "message": "创建成功" //消息 //非必填
}
```

**返回参数**

```json
{
    "code": 200,
    "msg": "success",
    "data": {}
}
    
{
    "code": 500,
    "msg": "失败，原因：xxxx",
}
```

### 1.3 入库单签收回调 `POST` `业务线提供请求接口`

**请求参数**

```json
{
    "requestId": "eyJwcm9kdWN0aW9uIjoicHJkIiwiY29tcGFueUlkIjoxMDAwMDMsInRyYWRlSWQiOjUxMywidGltZSI6MTY3OTk4NjAwNH0=",
    "inboundStatus": "finished", //入库状态 //必填 finished:完成    part:部分完成   cancel:取消   failed:失败
    "message": "签收备注，这里是备注",
    "receiveTime": "2024-09-13 14:11:24",
    "stockList": [
        {
            "applyQuantity": 23, //申请数量
            "deliveryQuantity": 23, //发货数量
            "receivedQuantity": 23, //收货数量
            "sku": "1031YWYW000010310942", //海外仓sku
            "erpSkuType": 1, //商品编码类型 int : 1库存；2组合； //必填
            "erpSku": "BOS-0562-1", //ERP商品编码 //必填
            "erpSkuId": 1234, //ERP商品ID int //必填
            "produceCode": "BATCH-20240913001", // 新增批次编号字段 2025-05-23 16:39:42
            "expireDate": "2025-06-03", //过期日期
            "productDate":"2025-06-01"//生产日期
            //可扩展其他sku信息
        }
    ]
}
```

**返回参数**

```json
{
    "code": 200,
    "msg": "success",
    "data": {}
}
{
    "code": 500,
    "msg": "失败，原因：xxxx",
}
```

### 2 出库单

### 2.1 获取出库单详情 `POST` `业务线提供请求接口`

**请求参数**

```json
{
    //可扩展字段
    "companyId": 123123, //公司id //必填
    "clusterId": "1", //  1 公有云 2 私有云 //必填
    "orderType": 1, //1:入库单 2:出库单
    "referenceId": "O202101010001", //出库单号 //必填,
    "sourceId": 3,  //3:手工出入库 5:fba 7:temu 9:ERP调拨单  21 加工单 23 新版手工出入库 29 新版ERP调拨单 31 采购单 33 采购退货出库  
}
```

**返回参数**

```json
{
    "code": 200,
    "msg": "success",
    "data": {
        "requestId": "eyJwcm9kdWN0aW9uIjoicHJkIiwiY29tcGFueUlkIjozNjA5OTcsInRyYWRlSWQiOjQwNTQsInRpbWUiOjE3MjQ4Mzk3NjZ9", //请求ID 后续各种回调都以此为准 //必填 长度最长255位
        "referenceId": "HWC3609972408280001", //出库单号 //必填,
        "sourceId": 3, //3:手工出入库 5:fba 7:temu 9:ERP调拨单
        "salesRecordNumber": "aaaa", //销售记录号 //非必填
        "warehouseId": 1111, //仓库id 必填
        "warehouseCode": "", //仓库编码 //非必填
        "channelCode": "HKXBCN_02", //渠道编码 //非必填
        "isCod": 2, //是否货到付款 1:是 2:否 //非必填
        "codCurrency": "USD", //货到付款币种 //非必填
        "codValue": 0, //货到付款金额 //非必填
        "createType": 1, //创建类型 1:交运 2:预报 //非必填
        "height": 10.00, //高度cm //必填
        "length": 10.00, //长度cm //必填
        "width": 10.00, //宽度cm //必填
        "weight": 1000, //重量g //必填
        "notifyTime": 1668068425, //当前时间 //非必填
        "orderDeclaredCurrency": "USD", //订单申报币种 //非必填
        "orderDeclaredValue": 0, //订单申报价值 //非必填
        "platformId": 1, //平台id //非必填
        "platformName": "TestPlatform", //平台名称 //非必填
        "platformShopId": 1, //平台店铺id //非必填
        "receiveAddress": { //收货地址
            "companyName": "FLY", //公司名称
            "contactName": "zhaoqiansun", //联系人
            "countryCode": "CA", //国家编码
            "province": "CA", //省
            "state": "WALNUT", //州
            "district": "", //区
            "doorCode": "", //门牌号
            "email": "22082@qq.com", //邮箱
            "mobile": 18368490000, //手机
            "telephone": "021-12345678", //电话
            "address1": "", //地址1
            "address2": "", //地址2
            "zipCode": "", //邮编
            "vatNumber": "123" //税号
        },
        "remark": "TestRemark", //出库备注 //非必填
        "extendInfo": {
            //扩展信息 //非必填
        },
        "item": [
            {
                //字段可扩展
                "lineNo": 1, //行号
                "erpSkuType": 1, //商品编码类型 int : 1库存；2组合； //必填
                "erpSku": "BOS-0562-1", //ERP商品编码 //必填
                "erpSkuId": 1234, //ERP商品ID int //必填
                "erpSkuName": "圣浪压缩袋-70*50cm", //sku名称 //非必填
                "erpPictureUrl": "erpPictureUrl", //erp图片
                "thirdSkuCode": "BOS-0562-1", //第三方商品编码 ：fbamsk；temu 平台sku //必填
                "quantity": 160, //数量 int//必填
                "specification": "", //规格 //非必填
                "unit": "PCS", //单位 //非必填
                "purchasePrice": 0.00, //采购价 //非必填
                "retailPrice": 0.00, //零售价 //非必填
                "declaredValue": 0.00, //sku申报价值 币种固定USD //非必填
                "declaredCode": "12223111", //sku海关编码 //非必填
                "declaredNameCn": "测试", //sku申报中文名 //非必填
                "declaredNameEn": "TEST", //sku申报英文名 //非必填
                "weight": 100, //重量 必填
                "weightUnit": "G" //重量单位 必填,
                 "ratioQty": 1, //配比系数【WMS仅存储，拣货数量按照库存维度的planQty】FBA需要的字段
                "packGroupId": "组包ID", //【同一个商品不会出现在不同的组包ID中】FBA需要的字段
                "packOptionId": "组包操作ID", //【示例：po00000000-0000-0000-0000-000000000000】【封箱反馈时带回给马帮】FBA需要的字段
                "commodityPDF": "商品贴", // HTTP:********1.PDF【注意pdf是数量为1的单个】
            }
        ],
        "label": {
            "labelUrl": "http://www.i8956.com//production/683c6ba55db411ed9fe6775d06f8b5d5/728af8985db411ed9fe6fb974f100de9.pdf", //标签url
            "trackNumber": 550668620223 //运单号
        }
    }
}
    
{
    "code": 500,
    "msg": "失败，原因：xxxx",
}
```

### 2.2 创建出库单回调 `POST` `业务线提供请求接口`

**请求参数**

```json
{
    "requestId": "eyJwcm9kdWN0aW9uIjoicHJkIiwiY29tcGFueUlkIjozNjA5OTcsInRyYWRlSWQiOjQwNTQsInRpbWUiOjE3MjQ4Mzk3NjZ9", //请求ID //必填
    "status": "1", //状态 1:创建成功 2:创建失败 //必填
    "outboundSn": "RD31470428116615", //三方仓出库单号 //必填
    "message": "创建成功" //消息 //非必填
}
```

**返回参数**

```json
{
    "code": 200,
    "msg": "success",
    "data": {}
}

{
    "code": 500,
    "msg": "失败，原因：xxxx",
}
```

### 2.3 同步模式直接调用接口创建出库单 `POST`

**环境信息**

| 环境名称 | 环境地址                                                                                        | 环境描述 |
|------|---------------------------------------------------------------------------------------------|------|
| 测试环境 | https://dev-mdc-oapi.mabangerp.com/mas-logistics-erp-service/hwcOrder/createHwcOrderApi     | 测试环境 |
| 生产环境 | http://mas-iapi.mabangerp.com/mas-logistics-erp-service/hwcOrder/createHwcOrderApi         | 公有云  |
| 生产环境 | http://mas-iapi-private.mabangerp.com/mas-logistics-erp-service/hwcOrder/createHwcOrderApi | 私有云  |

**接口地址**:`/hwcOrder/createHwcOrderApi`

**请求方式**:`POST`

**请求数据类型**:`application/json`

**请求头参数**:

| 参数名称           | 参数说明  | 是否必须  | 数据类型    | schema        |
|----------------|-------|-------|---------|---------------|
| cluster-id	    | 环境id	 | true	 | string	 | 	 1:公有云 2:私有云 |
| Authorization	 | 认证信息	 | true	 | string	 | aes-128-ecb   |
| timestamp      | 时间戳	  | true	 | string	 | 10位时间戳        |

```

# 加密方式 Authorization 说明
# secret = xxxxxx
# data = 100003##100025##1725443230 (企业id##登录人id##时间戳)
# Authorization = AES(data, secret) (aes-128-ecb)

# 例子 
# 原文 100003##100025##1725443230
# 密文 +DDUkoteE6AyR7aK7yAauW5I9Q9fnIYYWTqcgim3/Oo=

```

**请求参数**

```json
{
    "companyId": 123123, //公司id //必填
    "clusterId": "1", //  1 公有云 2 私有云 //必填
    "requestId": "eyJwcm9kdWN0aW9uIjoicHJkIiwiY29tcGFueUlkIjozNjA5OTcsInRyYWRlSWQiOjQwNTQsInRpbWUiOjE3MjQ4Mzk3NjZ9", //请求ID 后续各种回调都以此为准 //必填 长度最长255位
    "referenceId": "HWC3609972408280001", //出库单号 //必填
    "orderType": 1, //单据类型 1:采购入库单 2:出库单 3:退货入库单 //必填
    "salesRecordNumber": "aaaa", //销售记录号 //非必填
    "sourceId": 3, //数据来源 3:手工出入库 5:fba 7:temu 9:ERP调拨单 //必填
    "warehouseId": 1111, //仓库id 必填
    "warehouseCode": "", //仓库编码 //非必填
    "channelCode": "HKXBCN_02", //渠道编码 //非必填
    "isCod": 2, //是否货到付款 1:是 2:否 //非必填
    "codCurrency": "USD", //货到付款币种 //非必填
    "codValue": 0, //货到付款金额 //非必填
    "createType": 1, //创建类型 1:交运 2:预报 //非必填
    "height": 10.00, //高度cm //必填
    "length": 10.00, //长度cm //必填
    "width": 10.00, //宽度cm //必填
    "weight": 1000, //重量g //必填
    "notifyTime": 1668068425, //当前时间 //非必填
    "orderDeclaredCurrency": "USD", //订单申报币种 //非必填
    "orderDeclaredValue": 0, //订单申报价值 //非必填
    "platformId": 1, //平台id //非必填
    "platformName": "TestPlatform", //平台名称 //非必填
    "platformShopId": 1, //平台店铺id //非必填
    "receiveAddress": { //收货地址
        "companyName": "FLY", //公司名称
        "contactName": "zhaoqiansun", //联系人
        "countryCode": "CA", //国家编码
        "province": "CA", //省
        "state": "WALNUT", //州
        "district": "", //区
        "doorCode": "", //门牌号
        "email": "22082@qq.com", //邮箱
        "mobile": 18368490000, //手机
        "telephone": "021-12345678", //电话
        "address1": "", //地址1
        "address2": "", //地址2
        "zipCode": "", //邮编
        "vatNumber": "123" //税号
    },
    "remark": "TestRemark", //出库备注 //非必填
    "extendInfo": {
        //扩展信息 //非必填
    },
    "item": [
        {
            //字段可扩展
            "lineNo": 1, //行号
            "erpSkuType": 1, //商品编码类型 int : 1库存；2组合； //必填
            "erpSku": "BOS-0562-1", //ERP商品编码 //必填
            "erpSkuId": 1234, //ERP商品ID int //必填
            "erpSkuName": "圣浪压缩袋-70*50cm", //sku名称 //非必填
            "erpPictureUrl": "erpPictureUrl", //erp图片
            "thirdSkuCode": "BOS-0562-1", //第三方商品编码 ：fbamsk；temu 平台sku //必填
            "quantity": 160, //数量 int//必填
            "specification": "", //规格 //非必填
            "unit": "PCS", //单位 //非必填
            "purchasePrice": 0.00, //采购价 //非必填
            "retailPrice": 0.00, //零售价 //非必填
            "declaredValue": 0.00, //sku申报价值 币种固定USD //非必填
            "declaredCode": "12223111", //sku海关编码 //非必填
            "declaredNameCn": "测试", //sku申报中文名 //非必填
            "declaredNameEn": "TEST", //sku申报英文名 //非必填
            "weight": 100, //重量 必填
            "weightUnit": "G" //重量单位 必填,
            "fbaStockId": "fbaStockId", //fbaStockId FBA需要的字段
            "ratioQty": 1, //配比系数【WMS仅存储，拣货数量按照库存维度的planQty】FBA需要的字段
            "packGroupId": "组包ID", //【同一个商品不会出现在不同的组包ID中】FBA需要的字段
            "packOptionId": "组包操作ID", //【示例：po00000000-0000-0000-0000-000000000000】【封箱反馈时带回给马帮】FBA需要的字段
            "commodityPDF": "商品贴", // HTTP:********1.PDF【注意pdf是数量为1的单个】
        }
    ],
    "label": {
        "labelUrl": "http://www.i8956.com//production/683c6ba55db411ed9fe6775d06f8b5d5/728af8985db411ed9fe6fb974f100de9.pdf", //标签url
        "trackNumber": 550668620223 //运单号
    }
}
```

**返回参数**

```json
{
    "success": true,
    "code": 200,
    "data": {
        "createType": 1, //创建类型 1:交运 2:预报 //必填
        "describe": "已发货", //描述 //非必填
        "orderStatus": "finished", //订单状态 //必填 wait:等待发货  allow:已出单 (必须有trackNUmber)  finished:已发货  cancel:取消  failed:失败
        "outTime": "2023-05-04 17:15:33", //发货时间 //非必填
        "requestId": "xxxxx13", //请求ID //必填
        "systemNumber": "RD31470428116615", //三方仓系统单号 //非必填
        "trackNumber": "9200190321831711230337" //运单号 //非必填
    },
    "message": "成功",
    "currentTimestamp": 1725283873186
}


{
    "success": false,
    "code": 500,
    "data": {
        "requestId": 111111111111111111111,
        "orderStatus": "failed",
        "describe": "下单失败123132"
    },
    "message": "成功",
    "currentTimestamp": 1725700881401
}

```

### 2.4 出库单发货回调 `POST` `业务线提供请求接口`

**请求参数**

```json
{
    "createType": 1, //创建类型 1:交运 2:预报 //必填
    "describe": "已发货", //描述 //非必填
    "orderStatus": "finished", //订单状态 //必填 wait:等待发货  allow:已出单 (必须有trackNUmber)  finished:已发货  cancel:取消  failed:失败
    "outTime": "2023-05-04 17:15:33", //发货时间 //非必填
    "requestId": "xxxxx13", //请求ID //必填
    "logisticsCode":"SF", //物流公司编码
    "systemNumber": "RD31470428116615", //三方仓系统单号 //非必填
    "trackNumber": "9200190321831711230337", //运单号 //非必填
    "stockList": [
        {
            "applyQuantity": 5, //计划数
            "deliveryQuantity": 5, //发货数
            "erpSku": "YT-发网",
            "erpSkuId": 1231299890,
            "erpSkuType": 1, 
            "receivedQuantity": 0,
            "sku": "YT-发网", //三方仓sku
            "thirdSkuCode": "202409121231299890",
            "produceCode": "BATCH-20240913001", // 新增批次编号字段 2025-05-23 16:39:42
            "expireDate": "2025-06-03" ,//过期日期
            "productDate":"2025-06-01",//生产日期
            "packageNo":"1"包裹号
        }
    ]
}
```

**返回参数**

```json
{
    "code": 200,
    "msg": "success",
    "data": {}
}
{
    "code": 500,
    "msg": "失败，原因：xxxx",
}
```

### 3 创建出入库单据弹框

`/#/overseasWarehouse/inOutParam?key=c94daf05abfc744c58b999bb3053c427&cloud=test&lang=cn&iframeWidth=1200&iframeHeight=400&iframeName=inOutParam&orderType=1&sourceId=1&warehouseId=1334569117&referenceId=aaa1231231`

- orderType 单据类型 1 采购入库单 2 出库单 3 退货入库 4 加工单
- sourceId 数据来源 3 手工出入库 5 fba 7 temu 9:ERP调拨单 21 ERP加工单
- warehouseId 仓库id
- referenceId 单据编号

### 4 取消海外仓出入库单

**环境信息**

| 环境名称 | 环境地址                                                                                     | 环境描述 |
|------|------------------------------------------------------------------------------------------|------|
| 测试环境 | https://dev-mdc-oapi.mabangerp.com/mas-logistics-erp-service/hwcOrder/cancelHwcOrder     | 测试环境 |
| 生产环境 | http://mas-iapi.mabangerp.com/mas-logistics-erp-service/hwcOrder/cancelHwcOrder         | 公有云  |
| 生产环境 | http://mas-iapi-private.mabangerp.com/mas-logistics-erp-service/hwcOrder/cancelHwcOrder | 私有云  |

**接口地址**:`/hwcOrder/cancelHwcOrder`

**请求方式**:`POST`

**请求数据类型**:`application/json`

**请求头参数**:

| 参数名称           | 参数说明  | 是否必须  | 数据类型    | schema        |
|----------------|-------|-------|---------|---------------|
| cluster-id	    | 环境id	 | true	 | string	 | 	 1:公有云 2:私有云 |
| Authorization	 | 认证信息	 | true	 | string	 | aes-128-ecb   |
| timestamp      | 时间戳	  | true	 | string	 | 10位时间戳        |

```

# 加密方式 Authorization 说明
# secret = xxxxxx
# data = 100003##100025##1725443230 (企业id##登录人id##时间戳)
# Authorization = AES(data, secret) (aes-128-ecb)

# 例子 
# 原文 100003##100025##1725443230
# 密文 +DDUkoteE6AyR7aK7yAauW5I9Q9fnIYYWTqcgim3/Oo=

```

**请求示例**:

```javascript
{
  "describe": "建错单子了",
  "orderType": 1,
  "referenceId": "11111111",
  "requestId": "xxxxasda123",
  "sourceId": 3,  //3:手工出入库 5:fba 7:temu 9:ERP调拨单 11 中台推送temu退货入库单 21 加工单 23 新版手工出入库 29 新版ERP调拨单 31 采购单 33 采购退货出库
  "warehouseId": 111101
}
```

**请求参数**:

| 参数名称        | 参数说明 | 请求类型 | 是否必须  | 数据类型    | schema                                         |
|-------------|------|------|-------|---------|------------------------------------------------|
| describe    | 取消描述 |      | false | string  |                                                |
| orderType   | 建单类型 |      | true  | integer | 1:入库单 2:出库单 3:退货入库                             |
| referenceId | 单据编号 |      | true  | string  |                                                |
| requestId   | 请求id |      | true  | string  |                                                |
| sourceId    | 来源id |      | true  | integer | 3:手工出入库 5:fba 7:temu 9:ERP调拨单 11 中台推送temu退货入库单 21 加工单 23 新版手工出入库 29 新版ERP调拨单 31 采购单 33 采购退货出库  |
| warehouseId | 仓库id |      | true  | integer |                                                |

**响应状态**:

| 状态码 | 说明           | schema               |
|-----|--------------|----------------------| 
| 200 | OK           | RestResultVo«string» |
| 201 | Created      |                      |
| 401 | Unauthorized |                      |
| 403 | Forbidden    |                      |
| 404 | Not Found    |                      |

**响应参数**:

| 参数名称             | 参数说明 | 类型             | schema         |
|------------------|------|----------------|----------------| 
| code             |      | integer(int32) | integer(int32) |
| currentTimestamp |      | integer(int64) | integer(int64) |
| data             |      | string         |                |
| message          |      | string         |                |
| success          |      | boolean        |                |

**响应示例**:

```javascript
{
	"code": 200,
	"currentTimestamp": 0,
	"data": "取消成功",
	"message": "",
	"success": true
}
```

### 5 Temu,Fba封箱打印信息下发

**环境信息**

| 环境名称 | 环境地址                                                                                       | 环境描述 |
|------|--------------------------------------------------------------------------------------------|------|
| 测试环境 | https://dev-mdc-oapi.mabangerp.com/mas-logistics-erp-service/hwcOrder/sendBoxPrintInfo     | 测试环境 |
| 生产环境 | http://mas-iapi.mabangerp.com/mas-logistics-erp-service/hwcOrder/sendBoxPrintInfo         | 公有云  |
| 生产环境 | http://mas-iapi-private.mabangerp.com/mas-logistics-erp-service/hwcOrder/sendBoxPrintInfo | 私有云  |

**接口地址**:`/hwcOrder/sendBoxPrintInfo`

**请求方式**:`POST`

**请求数据类型**:`application/json`

**请求头参数**:

| 参数名称           | 参数说明  | 是否必须  | 数据类型    | schema        |
|----------------|-------|-------|---------|---------------|
| cluster-id	    | 环境id	 | true	 | string	 | 	 1:公有云 2:私有云 |
| Authorization	 | 认证信息	 | true	 | string	 | aes-128-ecb   |
| timestamp      | 时间戳	  | true	 | string	 | 10位时间戳        |

```

# 加密方式 Authorization 说明
# secret = xxxxxx
# data = 100003##100025##1725443230 (企业id##登录人id##时间戳)
# Authorization = AES(data, secret) (aes-128-ecb)

# 例子 
# 原文 100003##100025##1725443230
# 密文 +DDUkoteE6AyR7aK7yAauW5I9Q9fnIYYWTqcgim3/Oo=

```

**请求示例**:

```javascript
{
    "orderType": 1,
    "requestId": "xxxxasda123",
    "sourceId": 3,
    "warehouseId": 111101,
    "body": {} 
    //TEMU平台 封箱打印信息下发【马帮-发网WMS】 https://doc.apipost.net/docs/detail/31b64efbec64000?target_id=1b5b1cc7300083 
    //FBA平台 封箱打印信息下发【马帮-发网WMS】 https://doc.apipost.net/docs/detail/31cad57a5864000?target_id=1cad18b43000a4
```

**请求参数**:

| 参数名称        | 参数说明 | 请求类型 | 是否必须 | 数据类型    | schema       |
|-------------|------|------|------|---------|--------------|
| orderType   | 建单类型 |      | true | integer | 1:入库单 2:出库单  |
| requestId   | 请求id |      | true | string  |              |
| sourceId    | 来源id |      | true | integer | 5:fba 7:temu |
| warehouseId | 仓库id |      | true | integer |              |
| body        |      |      | true | object  | 业务线和发网沟通的结构体 |

**响应状态**:

| 状态码 | 说明           | schema               |
|-----|--------------|----------------------| 
| 200 | OK           | RestResultVo«string» |
| 201 | Created      |                      |
| 401 | Unauthorized |                      |
| 403 | Forbidden    |                      |
| 404 | Not Found    |                      |

**响应参数**:

| 参数名称             | 参数说明 | 类型             | schema         |
|------------------|------|----------------|----------------| 
| code             |      | integer(int32) | integer(int32) |
| currentTimestamp |      | integer(int64) | integer(int64) |
| data             |      | string         |                |
| message          |      | string         |                |
| success          |      | boolean        |                |

**响应示例**:

```javascript
{
	"code": 200,
	"currentTimestamp": 0,
	"data": "requestIdxxxxxxxxxxxxxxxx",
	"message": "下发成功",
	"success": true
}

{
    "code": 500,
    "currentTimestamp": 0,
    "data": "requestIdxxxxxxxxxxxxxxxx",
    "message": "下发失败",
    "success": false
}

```

### 6 创建退货入库单

### 6.1 同步模式直接调用接口创建退货入库单 `POST`

**环境信息**

| 环境名称 | 环境地址                                                                                        | 环境描述 |
|------|---------------------------------------------------------------------------------------------|------|
| 本地环境 | http://172.16.99.91:8161/hwcOrder/createHwcOrderApi                                         | 本地环境 |
| 测试环境 | https://dev-mdc-oapi.mabangerp.com/mas-logistics-erp-service/hwcOrder/createHwcOrderApi     | 测试环境 |
| 生产环境 | http://mas-iapi.mabangerp.com/mas-logistics-erp-service/hwcOrder/createHwcOrderApi         | 公有云  |
| 生产环境 | http://mas-iapi-private.mabangerp.com/mas-logistics-erp-service/hwcOrder/createHwcOrderApi | 私有云  |

**接口地址**:`/hwcOrder/createHwcOrderApi`

**请求方式**:`POST`

**请求数据类型**:`application/json`

**请求头参数**:

| 参数名称           | 参数说明  | 是否必须  | 数据类型    | schema        |
|----------------|-------|-------|---------|---------------|
| cluster-id	    | 环境id	 | true	 | string	 | 	 1:公有云 2:私有云 |
| Authorization	 | 认证信息	 | true	 | string	 | aes-128-ecb   |
| timestamp      | 时间戳	  | true	 | string	 | 10位时间戳        |

```

# 加密方式 Authorization 说明
# secret = xxxxxx
# data = 100003##100025##1725443230 (企业id##登录人id##时间戳)
# Authorization = AES(data, secret) (aes-128-ecb)

# 例子 
# 原文 100003##100025##1725443230
# 密文 +DDUkoteE6AyR7aK7yAauW5I9Q9fnIYYWTqcgim3/Oo=

```

**请求参数**

```json
{
    "referenceId": "HWC3609972408280001", //退货入库单号 //必填,
    "sourceId": 11, //11 中台推送temu退货入库单 //必填 固定11
    "orderType": 3, // 3 退货入库 固定3
    "warehouseId": 1111, //仓库id 必填
    "requestId": "eyJwcm9kdWN0aW9uIjoicHJkIiwiY29tcGFueUlkIjozNjA5OTcsInRyYWRlSWQiOjQwNTQsInRpbWUiOjE3MjQ4Mzk3NjZ9", //请求ID 后续各种回调都以此为准 //必填 长度最长255位
    "describe": "//描述//非必填", //描述 //非必填
    "extendInfo": {
        "logisticsCode": "SF", //物流公司编码(SF=顺丰、EMS=标准快递、EYB=经济快件、ZJS=宅急送、YTO=圆通 、ZTO=中通(ZTO)、HTKY=百世汇通、 UC=优速、STO=申通、TTKDEX=天天快递、QFKD=全峰、FAST=快捷、POSTB=邮政小包、GTO=国通、YUNDA=韵达、JD=京东配送、DD=当当宅配、 AMAZON=亚马逊物流、OTHER=其他(只传英文编码))
        "expressCode": "SF0000001",
        //扩展信息 //非必填
    },
    "packageList": [
        {
            "skuList": [
                {
                    //字段可扩展
                    "lineNo": 1, //行号
                    "erpSkuType": 1, //商品编码类型 int : 1库存；2组合； //必填
                    "erpSku": "BOS-0562-1", //ERP商品编码 //必填
                    "erpSkuId": 1234, //ERP商品ID int //必填
                    "erpSkuName": "圣浪压缩袋-70*50cm", //sku名称 //非必填
                    "erpPictureUrl": "erpPictureUrl", //erp图片
                    "thirdSkuCode": "BOS-0562-1", //第三方商品编码 ：fbamsk；temu 平台sku //必填
                    "quantity": 160, //数量 int//必填
                    "specification": "", //规格 //非必填
                    "unit": "PCS", //单位 //非必填
                    "purchasePrice": 0.00, //采购价 //非必填
                    "retailPrice": 0.00, //零售价 //非必填
                    "declaredValue": 0.00, //sku申报价值 币种固定USD //非必填
                    "declaredCode": "12223111", //sku海关编码 //非必填
                    "declaredNameCn": "测试", //sku申报中文名 //非必填
                    "declaredNameEn": "TEST", //sku申报英文名 //非必填
                    "weight": 100, //重量 必填
                    "weightUnit": "G" //重量单位 必填
                }
            ],
            "packNo": "MB01", //包裹号
            "length": 10.00, //长度
            "width": 10.00, //宽度
            "height": 10.00, //高度
            "sizeUnit": "CM", //尺寸单位
            "weight": 1000, //重量
            "weightUnit": "G" //重量单位
        }
    ]
}
```

**返回参数**

```json
{
    "success": true,
    "code": 200,
    "data": {
        "requestId": "eyJwcm9kdWN0aW9uIjoicHJkIiwiY29tcGFueUlkIjozNjA5OTcsInRyYWRlSWQiOjQwNTQsInRpbWUiOjE3MjQ4Mzk3NjZ9", //请求ID 
        "inboundSn": "RD31470428116615", //三方仓入库单号 //必填
    },
    "message": "成功",
    "currentTimestamp": 1725283873186
}

{
    "success": false,
    "code": 500,
    "data": {
        "requestId": "eyJwcm9kdWN0aW9uIjoicHJkIiwiY29tcGFueUlkIjozNjA5OTcsInRyYWRlSWQiOjQwNTQsInRpbWUiOjE3MjQ4Mzk3NjZ9", //请求ID 
    },
    "message": "失败描述",
    "currentTimestamp": 1725700881401
}

```

### 6.2 创建退货入库单签收回传参考 [1.3 入库单签收回调](#user-content-13-入库单签收回调-post-业务线提供请求接口)

### 6.3 退货入库单取消 参考 [4 取消海外仓出入库单](#user-content-4-取消海外仓出入库单)

### 7 加工单

### 7.1 获取加工单详情 `POST` `业务线提供请求接口`

**请求参数**

```json
{
    //可扩展字段
    "companyId": 123123, //公司id //必填
    "clusterId": "1", //  1 公有云 2 私有云 //必填
    "orderType": 1, //1:入库单 2:出库单
    "referenceId": "O202101010001", //出库单号 //必填,
    "sourceId": 3,  //3:手工出入库 5:fba 7:temu 9:ERP调拨单  21 加工单 23 新版手工出入库 29 新版ERP调拨单 31 采购单 33 采购退货出库  
}
```

**返回参数**

```json
{
    "code": 200,
    "msg": "success",
    "data": {
        "requestId": "eyJwcm9kdWN0aW9uIjoicHJkIiwiY29tcGFueUlkIjozNjA5OTcsInRyYWRlSWQiOjQwNTQsInRpbWUiOjE3MjQ4Mzk3NjZ9", //请求ID 后续各种回调都以此为准 //必填 长度最长255位
        "referenceId": "HWC3609972408280001", //出库单号 //必填,
        "sourceId": 3, //3:手工出入库 5:fba 7:temu 9:ERP调拨单
        "salesRecordNumber": "aaaa", //销售记录号 //非必填
        "warehouseId": 1111, //仓库id 必填
        "warehouseCode": "", //仓库编码 //非必填
        "channelCode": "HKXBCN_02", //渠道编码 //非必填
        "isCod": 2, //是否货到付款 1:是 2:否 //非必填
        "codCurrency": "USD", //货到付款币种 //非必填
        "codValue": 0, //货到付款金额 //非必填
        "createType": 1, //创建类型 1:交运 2:预报 //非必填
        "height": 10.00, //高度cm //必填
        "length": 10.00, //长度cm //必填
        "width": 10.00, //宽度cm //必填
        "weight": 1000, //重量g //必填
        "notifyTime": 1668068425, //当前时间 //非必填
        "orderDeclaredCurrency": "USD", //订单申报币种 //非必填
        "orderDeclaredValue": 0, //订单申报价值 //非必填
        "platformId": 1, //平台id //非必填
        "platformName": "TestPlatform", //平台名称 //非必填
        "platformShopId": 1, //平台店铺id //非必填
        "remark": "TestRemark", //出库备注 //非必填
        "extendInfo": {
            //扩展信息 //非必填
        },
        "item": [ //原材料
            {
                //字段可扩展
                "lineNo": 1, //行号
                "erpSkuType": 1, //商品编码类型 int : 1库存；2组合； //必填
                "erpSku": "BOS-0562-1", //ERP商品编码 //必填
                "erpSkuId": 1234, //ERP商品ID int //必填
                "erpSkuName": "圣浪压缩袋-70*50cm", //sku名称 //非必填
                "erpPictureUrl": "erpPictureUrl", //erp图片
                "thirdSkuCode": "BOS-0562-1", //第三方商品编码 ：fbamsk；temu 平台sku //必填
                "quantity": 160, //数量 int//必填
                "specification": "", //规格 //非必填
                "unit": "PCS", //单位 //非必填
                "purchasePrice": 0.00, //采购价 //非必填
                "retailPrice": 0.00, //零售价 //非必填
                "declaredValue": 0.00, //sku申报价值 币种固定USD //非必填
                "declaredCode": "12223111", //sku海关编码 //非必填
                "declaredNameCn": "测试", //sku申报中文名 //非必填
                "declaredNameEn": "TEST", //sku申报英文名 //非必填
                "weight": 100, //重量 必填
                "weightUnit": "G" //重量单位 必填,
                 "ratioQty": 1, //配比系数【WMS仅存储，拣货数量按照库存维度的planQty】FBA需要的字段
                "packGroupId": "组包ID", //【同一个商品不会出现在不同的组包ID中】FBA需要的字段
                "packOptionId": "组包操作ID", //【示例：po00000000-0000-0000-0000-000000000000】【封箱反馈时带回给马帮】FBA需要的字段
                "commodityPDF": "商品贴", // HTTP:********1.PDF【注意pdf是数量为1的单个】
            }
        ],
        "processedList": [ //成品
            {
                //字段可扩展
                "lineNo": 1, //行号
                "erpSkuType": 1, //商品编码类型 int : 1库存；2组合； //必填
                "erpSku": "BOS-0562-1", //ERP商品编码 //必填
                "erpSkuId": 1234, //ERP商品ID int //必填
                "erpSkuName": "圣浪压缩袋-70*50cm", //sku名称 //非必填
                "erpPictureUrl": "erpPictureUrl", //erp图片
                "thirdSkuCode": "BOS-0562-1", //第三方商品编码 ：fbamsk；temu 平台sku //必填
                "quantity": 160, //数量 int//必填
                "specification": "", //规格 //非必填
                "unit": "PCS", //单位 //非必填
                "purchasePrice": 0.00, //采购价 //非必填
                "retailPrice": 0.00, //零售价 //非必填
                "declaredValue": 0.00, //sku申报价值 币种固定USD //非必填
                "declaredCode": "12223111", //sku海关编码 //非必填
                "declaredNameCn": "测试", //sku申报中文名 //非必填
                "declaredNameEn": "TEST", //sku申报英文名 //非必填
                "weight": 100, //重量 必填
                "weightUnit": "G" //重量单位 必填,
                 "ratioQty": 1, //配比系数【WMS仅存储，拣货数量按照库存维度的planQty】FBA需要的字段
                "packGroupId": "组包ID", //【同一个商品不会出现在不同的组包ID中】FBA需要的字段
                "packOptionId": "组包操作ID", //【示例：po00000000-0000-0000-0000-000000000000】【封箱反馈时带回给马帮】FBA需要的字段
                "commodityPDF": "商品贴", // HTTP:********1.PDF【注意pdf是数量为1的单个】
            }
        ]
    }
}
    
{
    "code": 500,
    "msg": "失败，原因：xxxx",
}
```

### 7.2 创建加工单回调 `POST` `业务线提供请求接口`

**请求参数**

```json
{
    "requestId": "eyJwcm9kdWN0aW9uIjoicHJkIiwiY29tcGFueUlkIjozNjA5OTcsInRyYWRlSWQiOjQwNTQsInRpbWUiOjE3MjQ4Mzk3NjZ9", //请求ID //必填
    "status": "1", //状态 1:创建成功 2:创建失败 //必填
    "outboundSn": "RD31470428116615", //三方仓加工单号 //必填
    "message": "创建成功" //消息 //非必填
}
```

**返回参数**

```json
{
    "code": 200,
    "msg": "success",
    "data": {}
}

{
    "code": 500,
    "msg": "失败，原因：xxxx",
}
```

### 7.3 同步模式直接调用接口创建加工单 `POST`

**环境信息**

| 环境名称 | 环境地址                                                                                        | 环境描述 |
|------|---------------------------------------------------------------------------------------------|------|
| 测试环境 | https://dev-mdc-oapi.mabangerp.com/mas-logistics-erp-service/hwcOrder/createHwcOrderApi     | 测试环境 |
| 生产环境 | http://mas-iapi.mabangerp.com/mas-logistics-erp-service/hwcOrder/createHwcOrderApi         | 公有云  |
| 生产环境 | http://mas-iapi-private.mabangerp.com/mas-logistics-erp-service/hwcOrder/createHwcOrderApi | 私有云  |

**接口地址**:`/hwcOrder/createHwcOrderApi`

**请求方式**:`POST`

**请求数据类型**:`application/json`

**请求头参数**:

| 参数名称           | 参数说明  | 是否必须  | 数据类型    | schema        |
|----------------|-------|-------|---------|---------------|
| cluster-id	    | 环境id	 | true	 | string	 | 	 1:公有云 2:私有云 |
| Authorization	 | 认证信息	 | true	 | string	 | aes-128-ecb   |
| timestamp      | 时间戳	  | true	 | string	 | 10位时间戳        |

```

# 加密方式 Authorization 说明
# secret = xxxxxx
# data = 100003##100025##1725443230 (企业id##登录人id##时间戳)
# Authorization = AES(data, secret) (aes-128-ecb)

# 例子 
# 原文 100003##100025##1725443230
# 密文 +DDUkoteE6AyR7aK7yAauW5I9Q9fnIYYWTqcgim3/Oo=

```

**请求参数**

```json
{
    "extendInfo": {
        "orderCreateTime": "",
        "planTime": "",
        "serviceType": "",
        "planQty": ""
    },
    "item": [
        {
            "skuRemark": "skuRemark",
            "itemId": "",
            "quantity": 3,
            "ratioQty": 0,
            "sku": "A2-156PRO-0-EU0000-S"
        }
    ],
    "processedList": [
        {
            "skuRemark": "skuRemark",
            "itemId": "",
            "quantity": 3,
            "ratioQty": 0,
            "sku": "A2-156PRO-0-EU0000-S"
        }
    ],
    "logisticsId": 0,
    "orderType": 2,
    "referenceId": "djt_63769902496",
    "remark": "TestRemark",
    "requestId": "",
    "sourceId": 1,
    "storeName": "TestStore",
    "userToken": {},
    "warehouseCode": ""
}
```

**返回参数**

```json
{
    "success": true,
    "code": 200,
    "data": {
        "createType": 1, //创建类型 1:交运 2:预报 4:加工单 //必填
        "describe": "已发货", //描述 //非必填
        "orderStatus": "finished", //订单状态 //必填 wait:等待发货  allow:已出单 (必须有trackNUmber)  finished:已发货  cancel:取消  failed:失败
        "outTime": "2023-05-04 17:15:33", //加工完成时间 //非必填
        "requestId": "xxxxx13", //请求ID //必填
        "systemNumber": "RD31470428116615", //三方仓系统单号 //非必填
        "trackNumber": "9200190321831711230337" //运单号 //非必填
    },
    "message": "成功",
    "currentTimestamp": 1725283873186
}


{
    "success": false,
    "code": 500,
    "data": {
        "requestId": 111111111111111111111,
        "orderStatus": "failed",
        "describe": "下单失败123132"
    },
    "message": "成功",
    "currentTimestamp": 1725700881401
}

```

### 7.4 加工单出库回调 `POST` `业务线提供请求接口`

**请求参数**

```json
{
    "createType": 1, //创建类型 1:交运 2:预报 //必填
    "describe": "已发货", //描述 //非必填
    "orderStatus": "finished", //订单状态 //必填 wait:等待发货  allow:已出单 (必须有trackNUmber)  finished:已发货  cancel:取消  failed:失败
    "outTime": "2023-05-04 17:15:33", //加工完成时间 //非必填
    "requestId": "xxxxx13", //请求ID //必填
    "systemNumber": "RD31470428116615", //三方仓系统单号 //非必填
    "trackNumber": "9200190321831711230337", //运单号 //非必填
    "stockList": [ //原材料商品
        {
            "applyQuantity": 5, //计划数
            "deliveryQuantity": 5, //发货数
            "erpSku": "YT-发网",
            "erpSkuId": 1231299890,
            "erpSkuType": 1,
            "receivedQuantity": 0,
            "sku": "YT-发网", //三方仓sku
            "thirdSkuCode": "202409121231299890",
            "produceCode": "BATCH-20240913001", // 新增批次编号字段 2025-05-23 16:39:42
            "expireDate": "2025-06-03", //过期日期
            "productDate":"2025-06-01"//生产日期
        }
    ]
}
```

**返回参数**

```json
{
    "code": 200,
    "msg": "success",
    "data": {}
}
{
    "code": 500,
    "msg": "失败，原因：xxxx",
}
```
### 7.5 加工单入库回调 `POST` `业务线提供请求接口`

**请求参数**

```json
{
    "requestId": "eyJwcm9kdWN0aW9uIjoicHJkIiwiY29tcGFueUlkIjoxMDAwMDMsInRyYWRlSWQiOjUxMywidGltZSI6MTY3OTk4NjAwNH0=",
    "inboundStatus": "finished", //入库状态 //必填 finished:完成    part:部分完成   cancel:取消   failed:失败
    "message": "签收备注，这里是备注",
    "receiveTime": "2024-09-13 14:11:24", //加工完成时间
    "processedList": [ //加工商品
        {
            "applyQuantity": 23, //申请数量
            "deliveryQuantity": 23, //发货数量
            "receivedQuantity": 23, //加工数量
            "sku": "1031YWYW000010310942", //海外仓sku
            "erpSkuType": 1, //商品编码类型 int : 1库存；2组合； //必填
            "erpSku": "BOS-0562-1", //ERP商品编码 //必填
            "erpSkuId": 1234, //ERP商品ID int //必填
            "produceCode": "BATCH-20240913001", // 新增批次编号字段 2025-05-23 16:39:42
            "expireDate": "2025-06-03", //过期日期
            "productDate":"2025-06-01"//生产日期
            //可扩展其他sku信息
        }
    ]
}
```

**返回参数**

```json
{
    "code": 200,
    "msg": "success",
    "data": {}
}
{
    "code": 500,
    "msg": "失败，原因：xxxx",
}
```
### 7.6 加工单取消 参考 [4 取消海外仓出入库单](#user-content-4-取消海外仓出入库单)

### 7.7 加工单回调 `POST` `业务线提供请求接口`
```json
{
    "logisticsId":"3155",
    "referenceId":"",
    "sourceId":"21",
    "companyId":"",
    "clusterId":"",
    "platformId":"",
    "createType":"",
    "outboundSn":"",
    "requestId": "eyJwcm9kdWN0aW9uIjoicHJkIiwiY29tcGFueUlkIjoxMDAwMDMsInRyYWRlSWQiOjUxMywidGltZSI6MTY3OTk4NjAwNH0=",
    "describe": "签收备注，这里是备注",
    "outTime": "2024-09-13 14:11:24", //加工完成时间
    "stockList": [ //原材料商品
        {
            "applyQuantity": 23, //申请数量
            "deliveryQuantity": 23, //发货数量
            "receivedQuantity": 0,
            "sku": "1031YWYW000010310942", //海外仓sku
            "erpSkuType": 1, //商品编码类型 int : 1库存；2组合； //必填
            "erpSku": "BOS-0562-1", //ERP商品编码 //必填
            "erpSkuId": 1234, //ERP商品ID int //必填
            "produceCode": "BATCH-20240913001", // 新增批次编号字段 2025-05-23 16:39:42
            "expireDate": "2025-06-03", //过期日期
            "productDate":"2025-06-01"//生产日期
            //可扩展其他sku信息
        }
    ],
    "processedList": [ //加工商品
        {
            "applyQuantity": 23, //申请数量
            "deliveryQuantity": 23, //发货数量
            "receivedQuantity": 23, //加工数量
            "sku": "1031YWYW000010310942", //海外仓sku
            "erpSkuType": 1, //商品编码类型 int : 1库存；2组合； //必填
            "erpSku": "BOS-0562-1", //ERP商品编码 //必填
            "erpSkuId": 1234, //ERP商品ID int //必填
            "produceCode": "BATCH-20240913001", // 新增批次编号字段 2025-05-23 16:39:42
            "expireDate": "2025-06-03", //过期日期
            "productDate":"2025-06-01"//生产日期
            //可扩展其他sku信息
        }
    ]
}
```
### 8 出库单事件下推仓库系统

**环境信息**

| 环境名称 | 环境地址                                                                                       | 环境描述 |
|------|--------------------------------------------------------------------------------------------|------|
| 测试环境 | https://dev-mdc-oapi.mabangerp.com/mas-logistics-erp-service/hwcOrder/outOrderEventNotify     | 测试环境 |
| 生产环境 | http://mas-iapi.mabangerp.com/mas-logistics-erp-service/hwcOrder/outOrderEventNotify         | 公有云  |
| 生产环境 | http://mas-iapi-private.mabangerp.com/mas-logistics-erp-service/hwcOrder/outOrderEventNotify | 私有云  |

**接口地址**:`/hwcOrder/outOrderEventNotify`

**请求方式**:`POST`

**请求数据类型**:`application/json`

**请求头参数**:

| 参数名称           | 参数说明  | 是否必须  | 数据类型    | schema        |
|----------------|-------|-------|---------|---------------|
| cluster-id	    | 环境id	 | true	 | string	 | 	 1:公有云 2:私有云 |
| Authorization	 | 认证信息	 | true	 | string	 | aes-128-ecb   |
| timestamp      | 时间戳	  | true	 | string	 | 10位时间戳        |

```

# 加密方式 Authorization 说明
# secret = xxxxxx
# data = 100003##100025##1725443230 (企业id##登录人id##时间戳)
# Authorization = AES(data, secret) (aes-128-ecb)

# 例子 
# 原文 100003##100025##1725443230
# 密文 +DDUkoteE6AyR7aK7yAauW5I9Q9fnIYYWTqcgim3/Oo=

```

**请求示例**:

```json
{
    "orderType": 2,
    "requestId": "xxxxasda123",
    "sourceId": 17,
    "warehouseId": 111101,
    "body": {
        "deliveryOrderCode": "xxxxx123"
    }
}
```

**请求参数**:

| 参数名称        | 参数说明 | 请求类型 | 是否必须 | 数据类型    | schema       |
|-------------|------|------|------|---------|--------------|
| orderType   | 建单类型 |      | true | integer | 1:入库单 2:出库单  |
| requestId   | 请求id |      | true | string  |              |
| sourceId    | 来源id |      | true | integer | 5:fba 7:temu |
| warehouseId | 仓库id |      | true | integer |              |
| body        |      |      | true | object  | 业务线和发网沟通的结构体 |

**响应状态**:

| 状态码 | 说明           | schema               |
|-----|--------------|----------------------| 
| 200 | OK           | RestResultVo«string» |
| 201 | Created      |                      |
| 401 | Unauthorized |                      |
| 403 | Forbidden    |                      |
| 404 | Not Found    |                      |

**响应参数**:

| 参数名称             | 参数说明 | 类型             | schema         |
|------------------|------|----------------|----------------| 
| code             |      | integer(int32) | integer(int32) |
| currentTimestamp |      | integer(int64) | integer(int64) |
| data             |      | string         |                |
| message          |      | string         |                |
| success          |      | boolean        |                |

**响应示例**:

```json
{
	"code": 200,
	"currentTimestamp": 0,
	"data": "requestIdxxxxxxxxxxxxxxxx",
	"message": "通知成功",
	"success": true
}

{
    "code": 500,
    "currentTimestamp": 0,
    "data": "requestIdxxxxxxxxxxxxxxxx",
    "message": "通知失败",
    "success": false
}

```



### 9 批量创建海外仓出入库单

#### 接口信息

**接口地址**: `/hwcOrder/createBatchHwcOrder`

**请求方式**: `POST`

**请求数据类型**: `application/json`

**响应数据类型**: `*/*`

**接口描述**: 批量创建海外仓出入库单接口

**环境信息**

| 环境名称 | 环境地址                                                                                       | 环境描述 |
|------|--------------------------------------------------------------------------------------------|------|
| 测试环境 | https://dev-mdc-oapi.mabangerp.com/mas-logistics-erp-service/hwcOrder/createBatchHwcOrder     | 测试环境 |
| 生产环境 | http://mas-iapi.mabangerp.com/mas-logistics-erp-service/hwcOrder/createBatchHwcOrder         | 公有云  |
| 生产环境 | http://mas-iapi-private.mabangerp.com/mas-logistics-erp-service/hwcOrder/createBatchHwcOrder | 私有云  |

**请求示例**


```javascript
{
  "orderType": 1, //1:入库单 2:出库单
  "referenceIds": ["REF_001", "REF_002"],
  "sourceId": 1,  // 23 新版手工出入库  31 采购单 33 采购退货出库  
  "warehouseId": 1001
}
```

**请求头参数**

| 参数名称 | 参数说明 | 是否必须 | 数据类型 | schema |
| -------- | -------- | -------- | -------- | ------ |
| cluster-id | 环境id | true | string | 1:公有云 2:私有云 |
| Authorization | 认证信息 | true | string | aes-128-ecb |
| timestamp | 时间戳 | true | string | 10位时间戳 |

**加密方式 Authorization 说明**

```
# secret = xxxxxx
# data = 100003##100025##1725443230 (企业id##登录人id##时间戳)
# Authorization = AES(data, secret) (aes-128-ecb)

# 例子
# 原文 100003##100025##1725443230
# 密文 +DDUkoteE6AyR7aK7yAauW5I9Q9fnIYYWTqcgim3/Oo=
```


**请求参数**

| 参数名称 | 参数说明 | 请求类型 | 是否必须 | 数据类型 | schema |
| -------- | -------- | -------- | -------- | -------- | ------ |
| -------- | -------- | -------- | -------- | -------- | ------ |
| orderType | | | true | integer | |
| referenceIds | | | true | array | string |
| sourceId | | | true | integer | |
| warehouseId | | | true | integer | |

**响应示例**
```javascript
{
	"code": 200,
	"currentTimestamp": 0,
	"data": "提交成功",
	"message": "",
	"success": true
}


{
	"code": 500,
	"currentTimestamp": 0,
	"data": "",
	"message": "提交失败，xxxx",
	"success": true
}
```
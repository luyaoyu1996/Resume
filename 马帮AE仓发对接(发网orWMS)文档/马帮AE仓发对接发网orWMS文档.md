[TOC]

**环境信息**

| 环境名称 | 环境地址                                                             | 环境描述 |
|------|------------------------------------------------------------------|------|
| 本地环境 | http://172.16.99.91:8161                                         | 本地环境 |
| 测试环境 | http://192.168.2.77:32292     | 测试环境 |
| 测试环境 | https://dev-mdc-oapi.mabangerp.com/mas-logistics-erp-service     | 测试环境 |
| 生产环境 | http://mas-iapi.mabangerp.com/mas-logistics-erp-service         | 公有云  |
| 生产环境 | http://mas-iapi-private.mabangerp.com/mas-logistics-erp-service | 私有云  |

### 2 出库单

### 2.3 ERP->(发网orWMS) 创建出库单 `POST` (FBA发货单下发到海外仓物流中台中转，不会创建ERP的出库单据）

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
# secret = 联系周梦祥
# data = 100003##100025##1725443230 (企业id##登录人id##时间戳)
# Authorization = AES(data, secret) (aes-128-ecb)

# 例子 
# 原文 100003##100025##1725443230
# 密文 +DDUkoteE6AyR7aK7yAauW5I9Q9fnIYYWTqcgim3/Oo=

```

```java
public static void main(String[] args) {
    String secret = "联系周梦祥";
    byte[] key = secret.getBytes();
    //key 截取成 16 位
    key = Arrays.copyOf(key, 16);
    //Key length not 128/192/256 bits.
    AES aes = new AES(Mode.ECB, Padding.PKCS5Padding, key, "".getBytes());
    //打印密钥
    System.out.println(aes.getSecretKey().getEncoded().length);
    String s = "100003##100025##1725443230";
    //        String s = "100003##100025##" + System.currentTimeMillis() / 1000;
    System.out.println("加密：" + s);
    byte[] encrypt2 = aes.encrypt(s);
    System.out.println("加密：" + Base64.encodeBase64String(encrypt2));
}
```

```xml

<dependency>
    <groupId>cn.hutool</groupId>
    <artifactId>hutool-crypto</artifactId>
    <version>5.8.15</version>
</dependency>
```

- 2024-12-05 14:26:09新增字段

| 参数                   | 参数说明           | 请求类型 | 是否必须 | 数据类型    | schema            |
|----------------------|----------------|------|------|---------|-------------------|
| storeId              | 马帮店铺id         |      | true | integer |                   |
| storeName            | 马帮店铺名称         |      | true | string  |                   |
| toWarehouseCode      | 平台备货仓库编码       |      | true | string  |                   |
| toWarehouseName      | 平台备货仓库名称       |      | true | string  |                   |
| requireArrivedTime   | 预计到货时间或者最晚到仓时间 |      | true | string  |                   |
| choiceFlag           | 托管类型           |      | true | integer | 2, "半托管" 3, "全托管" |

**请求参数**

```json
{
  "companyId": 123123,   //公司id //必填
  "clusterId": "1",   //  1 公有云 2 私有云 //必填
  "requestId": "Q0tESDM2MDk5NzI0MDgyODAwMDE=",   //请求ID 后续各种回调都以此为准 //必填 长度最长255位
  "referenceId": "CKDH3609972408280001",   //出库单号 //必填
  "orderType": 2,   //单据类型 2:出库单 //必填 固定填 2
  "salesRecordNumber": "aaaa",   //销售记录号 //非必填 （速卖通仓发的 备货单号 必填）
  "sourceId": 15,   //数据来源:15 中台速卖通仓发订单 //必填 固定填 15
  "warehouseId": 1111,   //仓库id 必填 （需要传入的是马帮实体仓的id，根据虚拟仓找到对应的实体仓）
  "platformId": 1,   //平台id //必填
  "platformName": "TestPlatform",   //平台名称 //必填
  "remark": "TestRemark",   //出库备注 //非必填

  ////////////---2024-12-05 14:26:09新增字段////////
  "storeId": 123,   //马帮店铺id 必填
  "storeName": "马帮店铺名称",   //马帮店铺名称 必填
  "toWarehouseCode": "目的仓编码",   //平台备货仓库编码 必填
  "toWarehouseName": "目的仓名称",   //平台备货仓库名称 必填
  "requireArrivedTime": "2024-12-05 14:42:48",   //预计到货时间或者最晚到仓时间 必填
  "choiceFlag": 2,   //托管类型 2, "半托管" 3, "全托管" 选择2 或者3  必填

  "extendInfo": {
    //扩展信息 //非必填
  },
  "item": [
    {
      //字段可扩展
      "lineNo": "1",   //行号
      "erpSkuType": 1,   //商品编码类型 int : 1库存；2组合； //必填 》mabangStockSkuType
      "erpSku": "BOS-0562-1",   //ERP商品编码 //必填 》mabangStockSku
      "erpSkuId": 1234,   //ERP商品ID int //必填
      "erpSkuName": "圣浪压缩袋-70*50cm",   //sku名称 //非必填
      "thirdSkuCode": "BOS-0562-1",   //第三方商品编码 ：fbamsk；temu 速卖通 平台sku //必填 》scItemCode
      "thirdSkuId": "BOS-0562-1",   //第三方商品编码 ：fbamsk；temu 速卖通 平台sku //必填 scItemId
      "platformPictureUrl": "HTTP:********1.png",   //第三方商品编码图片
      "barcode": "BOS-0562-1",   //货品条码  //必填 barcode
      "quantity": 160,   //数量 int//必填
      "commodityPDF": "商品贴", // HTTP:********1.PDF【注意pdf是数量为1的单个】
      "goodsLabelConfigInfo": {
        //商品标签配置信息 //非必填 2025-01-22 10:24:33新增
      },
      "isSupportSecondShipment": 1,   //是否支持二次发货 1:支持 2:不支持 //非必填
      "warehouseId": 11111, //2025-04-08 16:28:05 新增
      "warehouseName": "仓库名称" //2025-04-08 16:28:05 新增
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
    "createType": 1,   //创建类型 1:交运 2:预报 //必填
    "describe": "已发货",   //描述 //非必填
    "orderStatus": "finished",   //订单状态 //必填 wait:等待发货  allow:已出单 (必须有trackNUmber)  finished:已发货  cancel:取消  failed:失败
    "outTime": "2023-05-04 17:15:33",   //发货时间 //非必填
    "requestId": "xxxxx13",   //请求ID //必填
    "systemNumber": "RD31470428116615",   //三方仓系统单号 //非必填
    "trackNumber": "9200190321831711230337",   //运单号 //非必填,
    "status": "1" //1 下单成功 2 下单失败
  },
  "message": "成功",
  "currentTimestamp": 1725283873186
}
```

```json
{
  "success": true,
  "code": 200,
  "data": {
    "orderStatus": "failed",
    "createType": 3,
    "requestId": "test0000000000000000001",
    "describe": "F202:AliExpress平台单据，request.deliveryOrder.outpackagePDF不能为空",
    "status": "2" //1 下单成功 2 下单失败
  },
  "message": "成功",
  "currentTimestamp": 1729583271593
}

```

```json
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

### 2.4 (发网orWMS) ->ERP 出库单发货回调 `POST` `业务线提供请求接口`

**请求参数**

```json
{
  "createType": 1,   //创建类型 1:交运 2:预报 //必填
  "describe": "已发货",   //描述 //非必填
  "orderStatus": "finished",   //订单状态 //必填 wait:等待发货  allow:已出单 (必须有trackNUmber)  finished:已发货  cancel:取消  failed:失败
  "outTime": "2023-05-04 17:15:33",   //发货时间 //非必填
  "requestId": "xxxxx13",   //请求ID //必填
  "systemNumber": "RD31470428116615",   //三方仓系统单号 //非必填
  "trackNumber": "9200190321831711230337",   //运单号 //非必填
  "goodsList": [
    {
      "applyQuantity": 5,   //计划数
      "deliveryQuantity": 5,   //发货数
      "erpSku": "YT-(发网orWMS)",
      "erpSkuId": 1231299890,
      "erpSkuType": 1,
      "sku": "YT-(发网orWMS)",   //三方仓sku
      "thirdSkuCode": "202409121231299890"
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

```

```json
{
  "code": 500,
  "msg": "失败，原因：xxxx"
}
```

### 4 ERP->(发网orWMS) 取消海外仓出入库单

**接口地址**:`/hwcOrder/cancelHwcOrder`

**请求方式**:`POST`

**请求数据类型**:`application/json`f

**请求头参数**:

| 参数名称           | 参数说明  | 是否必须  | 数据类型    | schema        |
|----------------|-------|-------|---------|---------------|
| cluster-id	    | 环境id	 | true	 | string	 | 	 1:公有云 2:私有云 |
| Authorization	 | 认证信息	 | true	 | string	 | aes-128-ecb   |
| timestamp      | 时间戳	  | true	 | string	 | 10位时间戳        |

**请求参数**:

| 参数名称               | 参数说明   | 请求类型 | 是否必须  | 数据类型    | schema                       |
|--------------------|--------|------|-------|---------|------------------------------|
| describe           | 取消描述   |      | false | string  |                              |
| orderType          | 建单类型   |      | true  | integer | 1:入库单 2:出库单 3:退货入库           |
| referenceId        | 单据编号   |      | true  | string  |                              |
| requestId          | 请求id   |      | true  | string  |                              |
| sourceId           | 来源id   |      | true  | integer | //数据来源:15 中台AE订单 //必填 固定填 15 |
| warehouseId        | 仓库id   |      | true  | integer |                              |
| **isForcedCancel** | 是否强制取消 |      | false | integer | 1不强制2.强制取消                   |

**请求示例**:

```json
{
  "describe": "建错单子了",
  "orderType": 1,
  "referenceId": "11111111",
  "requestId": "xxxxasda123",
  "sourceId": 15,
  "warehouseId": 111101
}
```

**响应示例**:

```json
{
  "code": 200,
  "currentTimestamp": 0,
  "data": "取消成功",
  "message": "",
  "success": true
}
```

### 5.1 (发网orWMS) ->ERP Temu,Fba,AE 装箱拣货信息回传 `POST` `业务线提供请求接口`

**请求参数**

```json
{
  "purchaseOrderNo": "test0001test0001",
  "mabangConsignOrderNo": "test0001",
  "companyId": 100003,
  "packageDetailList": [
    {
      "length": 11,
      "width": 11,
      "weight": 1110,
      "itemList": [
        {
          "quantity": 160,
          "mabangStockSku": "YT-(发网orWMS)",
          "scItemCode": "YT-(发网orWMS)1",
          "itemCode": "YT-(发网orWMS)",
          "scItemId": "YT-(发网orWMS)2",
          "barcode": "YT-(发网orWMS)3",
          "mabangStockSkuType": 1
        }
      ],
      "packageNo": "P01",
      "height": 11
    }
  ],
  "requestId": "test0000000000000000001",
  "platformId": 1,
  "clusterId": 1,
  "packageTime": "2024-10-22 16:06:53",
  "pickBatchNo": "pickBatchNo_001"
}
```

### 5.2 ERP->(发网orWMS) Temu,Fba,AE 封箱打印信息下发

**接口地址**:`/hwcOrder/sendBoxPrintInfo`

**请求方式**:`POST`

**请求数据类型**:`application/json`

**请求头参数**:

| 参数名称           | 参数说明  | 是否必须  | 数据类型    | schema        |
|----------------|-------|-------|---------|---------------|
| cluster-id	    | 环境id	 | true	 | string	 | 	 1:公有云 2:私有云 |
| Authorization	 | 认证信息	 | true	 | string	 | aes-128-ecb   |
| timestamp      | 时间戳	  | true	 | string	 | 10位时间戳        |

**请求参数**:

| 参数名称        | 参数说明 | 请求类型 | 是否必须 | 数据类型    | schema                       |
|-------------|------|------|------|---------|------------------------------|
| orderType   | 建单类型 |      | true | integer | 1:入库单 2:出库单                  |
| requestId   | 请求id |      | true | string  |                              |
| sourceId    | 来源id |      | true | integer | //数据来源:15 中台AE订单 //必填 固定填 15 |
| warehouseId | 仓库id |      | true | integer |                              |
| body        |      |      | true | object  | 业务线和(发网orWMS)沟通的结构体                 |

**请求示例**:

```json
{
  "orderType": 1,
  "requestId": "xxxxasda123",
  "sourceId": 15,
  "warehouseId": 111101,
  "body": {
    "deliveryOrderCode": "过奇门出库单下发【taobao.qimen.stockout.create】接口下发的：deliveryOrderCode",
    "platformOrderCode": "平台发货单号",
    "expressCode": "揽收单号",
    "expressPrintUrl": "HTTP:********.PDF【揽收面单】",
    "boxLabelConfigInfo": {
      //箱唛标签配置信息 2025-01-22 10:25:17新增
    },
    "printPDF": "HTTP:********.PDF【箱唛面单】"
  }
}
```

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
  "message": "下发成功",
  "success": true
}
```

```json
{
  "code": 500,
  "currentTimestamp": 0,
  "data": "requestIdxxxxxxxxxxxxxxxx",
  "message": "下发失败",
  "success": false
}
```
### 5.3 WMS-> ERP(速卖通全托) 获取商品和箱唛标签

**接口地址**:`/choice/hwcOrder/callback/print`

**请求方式**:`POST`

**请求数据类型**:`application/json`


**请求示例**:

```json
{
  "clusterId": "1", // 集群编号
  "companyId": 100003, // 企业编号
  "operatorId": "",
  "printDeliveryInfo": { // 箱唛打印入参
    "consignOrderNo": "IOCN2411281404153189912827", // 发货单号
    "pdfSize": "SIZE_A4" // 大小 SIZE_100_100_MARK ，  SIZE_100_100  ， SIZE_A4 ，   SIZE_A4_MARK ， SIZE_A4_ITEM
  },
  "printSkuInfo": { //商品打印入参
    "includeSignTagInfo": true, // 是否打印品类标签 true 是 false 否
    "printTemplateSize": "60_60", // 大小 60_60 or 60_30	
    "scItemId": 825630560573 // 货品id
  },
  "printType": 1, // 打印类型 0-商品  1-箱唛
  "shopId": 2121980954 ,// 店铺id
  "platformId": 1 // 平台id
}
```

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
  "success": true,
  "code": 200,
  "data": "https://cos-java-picture.mabangerp.com/aliexpress/choice/imgUpload/100003/IOCN24112814041531899128271737512989718_SIZE_A4.pdf",
  "message": "成功",
  "currentTimestamp": 1737512990384
}
```

```json
{
  "code": 500,
  "currentTimestamp": 0,
  "data": "requestIdxxxxxxxxxxxxxxxx",
  "message": "下发失败",
  "success": false
}
```
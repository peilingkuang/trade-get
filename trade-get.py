# -*- coding: utf-8 -*-
import pandas
import sys

import os


def main(argv):
    if not argv or len(argv) != 3:
        print "usage:%s ExportOrderList.csv ExportOrderDetailList.csv" % __file__
        return
    exportOrderListPath = argv[1]
    exportOrderDetailListPath = argv[2]

    if not os.path.exists(exportOrderDetailListPath) or not os.path.exists(exportOrderListPath):
        print "can not find file %s or %s" % (exportOrderListPath, exportOrderDetailListPath)

    df = pandas.read_csv(exportOrderListPath, encoding="gbk", header=0, sep=',',
                         names=["订单编号", "买家会员名", "买家支付宝账号", "买家应付货款", "买家应付邮费", "买家支付积分", "总金额", "返点积分", "买家实际支付金额",
                                "买家实际支付积分", "订单状态", "买家留言", "收货人姓名", "收货地址 ", "运送方式", "联系电话 ", "联系手机", "订单创建时间",
                                "订单付款时间 ", "宝贝标题 ", "宝贝种类 ", "物流单号 ", "物流公司", "订单备注", "宝贝总数量", "店铺Id", "店铺名称", "订单关闭原因",
                                "卖家服务费", "买家服务费", "发票抬头", "是否手机订单", "分阶段订单信息", "特权订金订单id", "是否上传合同照片", "是否上传小票", "是否代付",
                                "定金排名", "修改后的sku", "修改后的收货地址", "异常信息", "天猫卡券抵扣", "集分宝抵扣", "是否是O2O交易", "新零售交易类型",
                                "新零售导购门店名称", "新零售导购门店id", "新零售发货门店名称", "新零售发货门店id", "退款金额", "预约门店", "确认收货时间", "打款商家金额",
                                "含应开票给个人的个人红包"])
    # df = pandas.read_csv(exportOrderListPath, encoding="gbk")
    # print df.ix[:, "订单编号"]

    order_list = df.ix[:,
                 ["订单编号", "买家会员名", "收货人姓名", "收货地址 ", "联系手机", "买家留言", "订单备注", "修改后的收货地址", "买家实际支付金额", "订单付款时间 ", "异常信息"]]
    order_list["收货人信息"] = order_list["收货人姓名"].map(unicode) + ',' + order_list["联系手机"].map(unicode) + ',' + order_list[
        "收货地址 "].map(unicode)
    order_list.drop(order_list.columns[[2, 3, 4]], axis=1, inplace=True)
    # print order_list

    df2 = pandas.read_csv(exportOrderDetailListPath, encoding="gbk", header=0, sep=',',
                          names=["订单编号", "标题", "价格", "购买数量", "外部系统编号", "商品属性", "套餐信息", "备注", "订单状态", "商家编码"])

    detail_list = df2.ix[:, ["订单编号", "商品属性", "购买数量", "订单状态", "标题"]]
    detail_list["拣货"] = '(' + detail_list["商品属性"].map(unicode) + '*' + detail_list["购买数量"].map(unicode) + ')'
    detail_list.drop(detail_list.columns[[1, 2]], axis=1, inplace=True)
    detail_list = detail_list.groupby("订单编号").aggregate(lambda x: '\n'.join(list(x)))
    # print detail_list
    # dg = detail_list.groupby("订单编号")
    # print dg

    out_list = pandas.merge(order_list, detail_list, how='outer', on="订单编号")
    out = out_list.groupby("买家会员名").aggregate(lambda x: set(x))
    out = out.sort_values(by="订单付款时间 ")
    columns = ["收货人信息", "拣货", "买家留言", "订单备注", "订单状态", "标题", "买家实际支付金额", "订单编号", "修改后的收货地址", "订单付款时间 ", "异常信息"]
    out.to_csv("result.csv", encoding="gbk", columns=columns)

    # out.reindex("订单付款时间 ")
    # columns = ["收货人信息", "拣货", "买家留言", "订单备注", "买家会员名", "买家实际支付金额", "订单编号", "修改后的收货地址", "异常信息"]
    # out.to_csv("result.csv", encoding="gbk", index=False, columns=columns)

    # for name, group in out_list.groupby("买家会员名"):
    #     print group["收货人姓名"].aggregate(lambda x: set(x))
    # out_data = {"收货人姓名": group["收货人姓名"][], "联系手机", "收货地址", "商品属性数量", "买家留言", "订单备注", "买家会员名": name, "买家实际支付金额", "修改后的收货地址"}
    # writeHead = ["收货人姓名", "联系手机", "收货地址", "商品属性数量", "买家留言", "订单备注", "买家会员名", "买家实际支付金额", "修改后的收货地址"]


if __name__ == "__main__":
    main(sys.argv)

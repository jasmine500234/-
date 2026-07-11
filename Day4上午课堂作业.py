import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f"{x:.2f}")

orders = pd.DataFrame({
    "order_id": [f"O{number}" for number in range(1001, 1019)],
    "region": ["华东","华北","华南","华东","西南","华北","华南","华东","西南","华北","华东","华南","西南","华东","华北","华南","华东","西南"],
    "product": ["机械键盘","无线鼠标","显示器","扩展坞","机械键盘","显示器","无线鼠标","显示器","扩展坞","机械键盘","无线鼠标","扩展坞","显示器","机械键盘","扩展坞","显示器","无线鼠标","机械键盘"],
    "category": ["外设","外设","显示设备","配件","外设","显示设备","外设","显示设备","配件","外设","外设","配件","显示设备","外设","配件","显示设备","外设","外设"],
    "quantity": [2,3,1,4,5,2,6,1,3,2,8,2,1,3,5,2,4,6],
    "unit_price": [289,129,1299,399,289,1299,129,1299,399,289,129,399,1299,289,399,1299,129,289],
    "member_level": ["金卡","普通","银卡","金卡","银卡","普通","金卡","银卡","普通","金卡","银卡","金卡","普通","银卡","金卡","金卡","普通","银卡"],
    "coupon_rate": [0.05,0.00,0.00,0.03,0.10,0.00,0.05,0.00,0.12,0.05,0.00,0.08,0.10,0.00,0.00,0.12,0.05,0.08],
    "salesperson": ["小林","小周","小陈","小林","小赵","小周","小陈","小林","小赵","小周","小林","小陈","小赵","小周","小陈","小林","小周","小赵"]
})

# =====================任务1：快速理解数据====================
row_count, col_count = orders.shape
col_names = orders.columns.tolist()
print("----------任务1‑1----------")
print(f"数据集行数：{row_count}，列数：{col_count}")
print("全部列名：", col_names)
print("")

#2.取出单列和多列，打印类型
ser_region = orders["region"]
df_part = orders[["order_id","product","quantity"]]
print("----------任务1‑2----------")
print("region列的数据类型：", type(ser_region))
print("order_id,product,quantity的数据类型：", type(df_part))
print("")

df_iloc = orders.iloc[3:8, 0:4]
print("----------任务1‑3 iloc选取结果----------")
print(df_iloc)
print("")

df_east = orders.loc[orders["region"] == "华东", ["order_id","product","member_level"]]
print("----------任务1‑4 华东订单----------")
print(df_east)
print("")

#5.简答：loc是基于标签名称选取，列名、行索引发生变化代码依旧稳定；iloc依靠数字下标，顺序改动就会出错，正式项目优先loc。
print("----------任务1‑5 回答----------")
print("loc依据行列名称筛选数据，下标顺序变动不会影响代码运行，长期维护更稳妥；iloc依靠数字位置取值，数据顺序改变结果就出错。\n")

# =====================任务2：构造订单结算指标=================
analysis = orders.copy()
analysis["gross_amount"] = analysis["quantity"] * analysis["unit_price"]
analysis["member_discount"] = np.where(analysis["member_level"] == "金卡",0.1,
                                       np.where(analysis["member_level"] == "银卡",0.05,0))
analysis["payable_amount"] = analysis["gross_amount"] * (1 - analysis["member_discount"]) * (1 - analysis["coupon_rate"])
analysis["shipping_fee"] = np.where(analysis["payable_amount"] >= 1000,0,20)
analysis["final_amount"] = analysis["payable_amount"] + analysis["shipping_fee"]
analysis = analysis.round(2)
print("----------任务2：前8行结算字段----------")
show_cols = ["order_id","quantity","unit_price","gross_amount","member_discount","payable_amount","shipping_fee","final_amount"]
print(analysis[show_cols].head(8))
print("任务2结果释义：通过向量化运算算出每一笔订单原价、会员折扣、优惠券扣减、运费以及顾客最后实际付款金额，全程没有写循环。\n")

# =====================任务3：复杂条件筛选====================
# 分别定义3个布尔条件
cond1 = (analysis["region"] == "华东") | (analysis["region"] == "华南")
cond2 = analysis["final_amount"] >= 700
cond3 = (analysis["quantity"] >= 2) | (analysis["member_level"] == "金卡")
mask = cond1 & cond2 & cond3
focus_df = analysis.loc[mask, ["order_id","region","product","quantity","member_level","final_amount"]].sort_values("final_amount", ascending=False)
print("----------任务3 重点跟进订单----------")
print(focus_df)
print("条件括号解释：&和|的优先级高于比较运算符，如果不加括号，判断逻辑错乱，因此每一个条件表达式都要用括号包裹。")
print("任务3释义：筛选出华东华南、付款不少于700，购买数量≥2或者金卡客户的订单，按照成交金额从高到低排序，这些订单是后续重点跟进对象。\n")

# =====================任务4：封装可复用处理函数====================
def add_order_level(df):
    df_copy = df.copy()
    # 嵌套np.where完成等级划分：>=2000战略；1000‑2000重点；<1000普通
    df_copy["order_level"] = np.where(df_copy["final_amount"] >= 2000, "战略订单",
                                np.where(df_copy["final_amount"] >= 1000, "重点订单", "普通订单"))
    return df_copy

leveled_orders = analysis.pipe(add_order_level)
level_count = leveled_orders["order_level"].value_counts()
print("----------任务4 订单等级统计----------")
print(level_count)
print("任务4释义：利用pipe和np.where划分订单等级，统计得出战略订单、重点订单、普通订单分别的数量，帮助区分订单重要程度。\n")

# =====================任务5：一条方法链完成经营汇总，不产生中间变量====================
region_report = (analysis
                 .pipe(add_order_level)
                 .query("final_amount > 500")
                 .groupby("region")
                 .agg(order_count = ("order_id", "count"),
                      total_goods = ("quantity", "sum"),
                      total_revenue = ("final_amount", "sum"),
                      avg_price = ("final_amount", "mean"))
                 .sort_values("total_revenue", ascending=False)
                 .round(2))
print("----------任务5 分地区经营报表----------")
print(region_report)
print("任务5释义：链式调用依次完成增加订单等级、过滤大额订单、按地区分组聚合统计，最后按总收入降序，得到各个区域订单情况。\n")

# =====================任务6：经营诊断分析====================
# 1.找出成交总额最高的销售人员
sales_total = analysis.groupby("salesperson")["final_amount"].sum()
top_sales_name = sales_total.idxmax()
top_sales_total = sales_total.max()

#2.该销售员各个地区销售额
sales_region_df = analysis[analysis["salesperson"] == top_sales_name].groupby("region")["final_amount"].sum()
best_region = sales_region_df.idxmax()
region_money = sales_region_df.max()

#3.地区贡献率
rate = (region_money / top_sales_total) * 100
rate = round(rate, 2)

print("----------任务6 经营诊断结果----------")
print(f"销售人员：{top_sales_name}")
print(f"总成交金额：{top_sales_total:.2f}")
print(f"核心地区：{best_region}")
print(f"核心地区金额：{region_money:.2f}")
print(f"该地区贡献率：{rate}%")
print("业务结论：该销售员业绩主要依靠对应核心地区，该地区贡献了他大部分销售额，后续可以在该区域继续深耕拓展更多客户。")

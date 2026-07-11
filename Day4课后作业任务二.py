import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 在线读取UCI官方空气质量数据集
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00381/PRSA_data_2010.1.1-2014.12.31.csv"
df = pd.read_csv(url)

# 构造完整时间字段
df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour"]])
df = df.set_index("datetime")

# 简单缺失插值清洗
df["pm2.5"] = df["pm2.5"].interpolate(method="linear")

# 2. 构造季节特征
def get_season(month):
    if month in [12, 1, 2]:
        return "冬季"
    elif month in [3, 4, 5]:
        return "春季"
    elif month in [6, 7, 8]:
        return "夏季"
    else:
        return "秋季"
df["season"] = df.index.month.map(get_season)

# 3. 计算统计指标与相关系数
print("=====污染物与气象因子描述性统计=====")
target_cols = ["pm2.5", "TEMP", "DEWP", "PRES", "Iws"]
print(df[target_cols].describe())

print("\n=====特征相关系数矩阵=====")
corr_matrix = df[target_cols].corr()
print(corr_matrix)

# 设置画布中文显示
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 图表1：折线图 - PM2.5月度均值时序
plt.figure(figsize=(14, 5))
month_data = df.resample("M").mean()
plt.plot(month_data.index, month_data["pm2.5"], color="#d62728", linewidth=1.3)
plt.title("2010-2014北京PM2.5月度浓度变化折线图")
plt.xlabel("时间")
plt.ylabel("PM2.5浓度 μg/m³")
plt.grid(alpha=0.3)
plt.show()

# 图表2：柱状图 - 四季PM2.5均值对比
plt.figure(figsize=(8, 5))
season_avg = df.groupby("season")["pm2.5"].mean().reindex(["春季", "夏季", "秋季", "冬季"])
plt.bar(season_avg.index, season_avg.values, color=["#7ccd7c", "#4192d9", "#ff9955", "#b82626"])
plt.title("四季PM2.5平均浓度柱状图")
plt.ylabel("PM2.5平均浓度")
plt.show()

# 图表3：散点图 - 风速与PM2.5关系
plt.figure(figsize=(8, 5))
plt.scatter(df["Iws"], df["pm2.5"], alpha=0.3, s=4, c="#2c3e50")
plt.title("累积风速Iws与PM2.5浓度散点图")
plt.xlabel("累积风速 Iws")
plt.ylabel("PM2.5浓度")
plt.show()

# 图表4：热力图 - 特征相关性
plt.figure(figsize=(7, 6))
sns.heatmap(corr_matrix, annot=True, cmap="RdBu_r", vmin=-1, vmax=1)
plt.title("气象与污染物特征相关性热力图")
plt.show()

# 季节性规律输出总结
print("\n=====空气质量季节规律分析=====")
print("1. 冬季PM2.5均值最高，供暖燃煤导致污染加重；")
print("2. 夏季降水多、风力强，污染物扩散快，浓度最低；")
print("3. 风速Iws与PM2.5呈明显负相关，大风利于污染物消散。")

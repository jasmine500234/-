import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 读取数据集（seaborn内置泰坦尼克数据，自带缺失、重复）
df_raw = sns.load_dataset("titanic")
print("=====原始数据基础信息=====")
print(f"原始数据行列数：{df_raw.shape}")
print("\n各列数据类型：")
print(df_raw.dtypes)
print("\n每列缺失值数量：")
print(df_raw.isnull().sum())
print(f"\n完全重复记录条数：{df_raw.duplicated().sum()}")

# 2. 识别并删除重复记录
dup_data = df_raw[df_raw.duplicated(keep=False)]
print("\n=====重复样本预览=====")
print(dup_data.head())
df_no_dup = df_raw.drop_duplicates()
print(f"\n去重后数据量：{df_no_dup.shape}")

# 3. 三种缺失值处理方法
# 方法1：删除法
df_del = df_no_dup.drop(columns=["deck"])  # 缺失率过高直接删列
df_del = df_del.dropna(subset=["embarked"]) # 少量缺失直接删行
print(f"\n删除缺失后数据：{df_del.shape}")

# 方法2：统计填充（数值中位数、分类众数）
df_fill = df_del.copy()
df_fill["age"].fillna(df_fill["age"].median(), inplace=True)
df_fill["embark_town"].fillna(df_fill["embark_town"].mode()[0], inplace=True)
print("\n填充后缺失值统计：")
print(df_fill.isnull().sum())

# 方法3：线性插值填充年龄
df_interp = df_del.copy()
df_interp["age"] = df_interp["age"].interpolate(method="linear")
print("\n插值填充后age缺失数：", df_interp["age"].isnull().sum())

# 4. 异常值处理：IQR箱线法过滤票价异常
df_clean = df_fill.copy()
Q1 = df_clean["fare"].quantile(0.25)
Q3 = df_clean["fare"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df_clean = df_clean[(df_clean["fare"] >= lower_bound) & (df_clean["fare"] <= upper_bound)]
print(f"\n剔除异常值后数据量：{df_clean.shape}")

# 5. 数据类型转换与标准化
# 数值类型统一
df_clean["pclass"] = df_clean["pclass"].astype("int32")
# 分类类型优化
df_clean["sex"] = df_clean["sex"].astype("category")
# 文本标准化：去空格、小写
df_clean["who"] = df_clean["who"].str.strip().str.lower()
# 分类特征独热编码
df_final = pd.get_dummies(df_clean, columns=["sex", "embarked"], drop_first=True)

print("\n=====最终清洗完成数据集预览=====")
print(df_final.head())
print(f"最终数据集行列：{df_final.shape}")

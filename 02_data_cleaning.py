"""
红酒品质数据分析与预测 - 第2步：数据清洗
功能：缺失值检查、描述性统计、品质分布分析、特征工程、保存清洗后数据
"""

import pandas as pd
import numpy as np
import warnings
import os
import sys
warnings.filterwarnings('ignore')

# 确保控制台输出 UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 基准目录（脚本所在目录）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("=" * 70)
print("红酒品质数据分析与预测 - 数据清洗")
print("=" * 70)

# =============================================================================
# 1. 读取原始数据
# =============================================================================
print("\n[1] 读取原始数据")
DATA_PATH = r"D:\邹睿\python实习\实习最终项目\winequality-red.csv"
df = pd.read_csv(DATA_PATH, sep=';')
print(f"  数据形状: {df.shape[0]} 行 × {df.shape[1]} 列")

# =============================================================================
# 2. 缺失值检查
# =============================================================================
print("\n[2] 缺失值检查")
print("-" * 50)
missing = df.isnull().sum()
print(missing.to_string())
if missing.sum() == 0:
    print("  [OK] 数据无缺失值")
else:
    print(f"  [WARN] 发现 {missing.sum()} 个缺失值")
    # 此处可添加缺失值处理逻辑
    # df = df.dropna()  # 或 df.fillna(...)

# =============================================================================
# 3. 描述性统计
# =============================================================================
print("\n[3] 描述性统计")
print("-" * 50)
print(df.describe().round(3).to_string())

# =============================================================================
# 4. 品质分布统计
# =============================================================================
print("\n[4] 品质分布")
print("-" * 50)
quality_counts = df['quality'].value_counts().sort_index()
for q, c in quality_counts.items():
    pct = c / len(df) * 100
    print(f"  品质={q}: {c} 条 ({pct:.1f}%)")
pct_5_6 = ((df['quality'] == 5) | (df['quality'] == 6)).sum() / len(df) * 100
print(f"  品质 5 或 6 占比: {pct_5_6:.1f}%")

# =============================================================================
# 5. 特征工程
# =============================================================================
print("\n[5] 特征工程")
print("-" * 50)

# 5.1 创建总酸度特征
df['total acidity'] = df['fixed acidity'] + df['volatile acidity'] + df['citric acid']
print(f"  新增特征 'total acidity' = fixed + volatile + citric acid")
print(f"  total acidity 范围: {df['total acidity'].min():.2f} ~ {df['total acidity'].max():.2f}")

# 5.2 创建甜度分类特征
sweetness_bins = [0, 4, 12, 45, float('inf')]
sweetness_labels = ['Dry (≤4)', 'Semi-Dry (4-12)', 'Semi-Sweet (12-45)', 'Sweet (>45)']
df['sweetness_type'] = pd.cut(df['residual sugar'], bins=sweetness_bins, labels=sweetness_labels)
print(f"  新增特征 'sweetness_type' - 甜度分类:")
for label, count in df['sweetness_type'].value_counts().items():
    print(f"    {label}: {count} 条 ({count/len(df)*100:.1f}%)")

# =============================================================================
# 6. 保存清洗后数据
# =============================================================================
CLEANED_DATA_PATH = os.path.join(BASE_DIR, 'winequality_cleaned.csv')
df.to_csv(CLEANED_DATA_PATH, index=False)
print(f"\n[6] 清洗后数据已保存至: {CLEANED_DATA_PATH}")
print(f"  数据形状: {df.shape[0]} 行 × {df.shape[1]} 列")
print(f"  列名: {list(df.columns)}")
print(f"  文件大小: {os.path.getsize(CLEANED_DATA_PATH):,} bytes")

print("\n>>> 数据清洗完成，请运行 03_eda.py 继续 <<<")

"""
红酒品质数据分析与预测 - 第1步：数据读取

"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import warnings
import os
import sys
warnings.filterwarnings('ignore')

# 确保控制台输出 UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 字体与编码设置
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False  # 使用 ASCII 减号替代 Unicode 减号

# 基准目录（脚本所在目录）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 输出目录
CHARTS_DIR = os.path.join(BASE_DIR, 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

print("=" * 70)
print("红酒品质数据分析与预测")
print("=" * 70)

# =============================================================================
# 1. 读取数据
# =============================================================================
print("\n[1] 读取数据")
DATA_PATH = r"D:\邹睿\python实习\实习最终项目\winequality-red.csv"
df = pd.read_csv(DATA_PATH, sep=';')
print(f"  数据形状: {df.shape[0]} 行 × {df.shape[1]} 列")
print(f"  列名: {list(df.columns)}")
print(f"\n数据前5行:")
print(df.head().to_string())

print("\n>>> 数据读取完成，请运行 02_data_cleaning.py 继续 <<<")

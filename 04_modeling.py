"""
红酒品质数据分析与预测 - 第4步：建模与评估
功能：特征准备、标准化、训练/测试集划分、线性回归建模、模型评估、系数分析、残差分析
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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

# 基准目录（脚本所在目录）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 字体与编码设置
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

CHARTS_DIR = os.path.join(BASE_DIR, 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

print("=" * 70)
print("红酒品质数据分析与预测 - 建模与评估")
print("=" * 70)

# =============================================================================
# 1. 读取清洗后数据
# =============================================================================
print("\n[1] 读取清洗后数据")
CLEANED_DATA_PATH = os.path.join(BASE_DIR, 'winequality_cleaned.csv')
df = pd.read_csv(CLEANED_DATA_PATH)
print(f"  数据形状: {df.shape[0]} 行 × {df.shape[1]} 列")

# =============================================================================
# 2. 准备特征与目标变量
# =============================================================================
print("\n[2] 准备特征与目标变量")
feature_names = ['fixed acidity', 'volatile acidity', 'citric acid',
                 'residual sugar', 'chlorides', 'free sulfur dioxide',
                 'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol']
X = df[feature_names]
y = df['quality']

print(f"  特征数量: {len(feature_names)}")
print(f"  目标变量: quality")

# =============================================================================
# 3. 特征标准化
# =============================================================================
print("\n[3] 特征标准化 (StandardScaler)")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=feature_names)
print("  标准化完成")

# =============================================================================
# 4. 划分训练集与测试集
# =============================================================================
print("\n[4] 划分训练集与测试集 (80/20)")
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

print(f"  训练集: {len(X_train)} 条")
print(f"  测试集: {len(X_test)} 条")

# =============================================================================
# 5. 训练线性回归模型
# =============================================================================
print("\n[5] 训练线性回归模型")
model = LinearRegression()
model.fit(X_train, y_train)
print("  模型训练完成")

# =============================================================================
# 6. 预测与评估
# =============================================================================
print("\n[6] 模型评估")
print("-" * 50)
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"  MSE  (均方误差):       {mse:.4f}")
print(f"  RMSE (均方根误差):     {rmse:.4f}")
print(f"  MAE  (平均绝对误差):   {mae:.4f}")
print(f"  R²   (决定系数):       {r2:.4f}")

# =============================================================================
# 7. 特征系数分析
# =============================================================================
print("\n[7] 特征系数分析")
print("-" * 50)
coef_df = pd.DataFrame({
    'Feature': feature_names,
    'Coefficient': model.coef_
}).sort_values('Coefficient', key=abs, ascending=False)
print(f"  {'Feature':25s}  Coefficient")
print(f"  {'-'*35}")
for _, row in coef_df.iterrows():
    print(f"  {row['Feature']:25s}: {row['Coefficient']:+8.4f}")

# =============================================================================
# 8. 可视化：预测值 vs 实际值 + 残差分析
# =============================================================================
print("\n[8] 绘制模型评估图")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 子图1: 预测值 vs 实际值
axes[0].scatter(y_test, y_pred, alpha=0.5, edgecolors='k', linewidth=0.3, color='steelblue')
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', linewidth=2, label='Perfect Prediction')
axes[0].set_xlabel('Actual Quality')
axes[0].set_ylabel('Predicted Quality')
axes[0].set_title(f'Predicted vs Actual Quality (R² = {r2:.3f})')
axes[0].legend()

# 子图2: 残差分析
residuals = y_test - y_pred
axes[1].scatter(y_pred, residuals, alpha=0.5, edgecolors='k', linewidth=0.3, color='steelblue')
axes[1].axhline(y=0, color='r', linestyle='--', linewidth=2)
axes[1].set_xlabel('Predicted Quality')
axes[1].set_ylabel('Residuals')
axes[1].set_title('Residual Analysis')

plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'model_evaluation.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  已保存: charts/model_evaluation.png")

# =============================================================================
# 9. 可视化：特征系数条形图
# =============================================================================
print("\n[9] 绘制特征系数图")
plt.figure(figsize=(10, 6))
colors = ['#2ecc71' if c > 0 else '#e74c3c' for c in coef_df['Coefficient']]
plt.barh(coef_df['Feature'][::-1], coef_df['Coefficient'][::-1], color=colors[::-1])
plt.xlabel('Coefficient')
plt.title('Linear Regression Coefficients')
plt.axvline(x=0, color='black', linewidth=0.8)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'feature_coefficients.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  已保存: charts/feature_coefficients.png")

# =============================================================================
# 10. 总结
# =============================================================================
print("\n" + "=" * 70)
print("建模总结")
print("=" * 70)
print(f"""
  ┌─────────────────────────────────────────────────────────┐
  │  1. 红酒品质主要与酒精浓度、挥发性酸、柠檬酸相关          │
  │  2. 品质 ≥ 7 或 ≤ 4 的酒在线性特征上可分                │
  │  3. 品质 5 和 6 的酒（占 82%）线性可分性较差            │
  │  4. 酒精浓度与品质正相关最强 (corr ≈ +0.48)              │
  │  5. 挥发性酸度与品质负相关最强 (corr ≈ -0.39)           │
  │  6. 线性回归 R² = {r2:.3f}，模型有一定预测能力               │
  │  7. 进一步提升方向: 决策树、随机森林等非线性模型          │
  └─────────────────────────────────────────────────────────┘
""")



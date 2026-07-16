"""
红酒品质数据分析与预测 - 第3步：探索性数据分析 (EDA)
功能：单变量分析、双变量分析、多变量分析、相关性分析、生成所有图表
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
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
print("红酒品质数据分析与预测 - 探索性数据分析 (EDA)")
print("=" * 70)

# =============================================================================
# 1. 读取清洗后数据
# =============================================================================
print("\n[1] 读取清洗后数据")
CLEANED_DATA_PATH = os.path.join(BASE_DIR, 'winequality_cleaned.csv')
df = pd.read_csv(CLEANED_DATA_PATH)
# 确保 sweetness_type 是 category 类型
if 'sweetness_type' in df.columns:
    df['sweetness_type'] = pd.Categorical(df['sweetness_type'])
print(f"  数据形状: {df.shape[0]} 行 × {df.shape[1]} 列")

# =============================================================================
# 2. 箱线图 - 各特征分布
# =============================================================================
print("\n[2] 绘制箱线图")
# 只选择数值列（排除 category 类型）
numeric_cols_all = [c for c in df.columns if df[c].dtype not in ['category']]
n_cols = len(numeric_cols_all)
n_rows = (n_cols + 2) // 3  # 每行3个子图，自动计算行数
fig, axes = plt.subplots(n_rows, 3, figsize=(18, 5 * n_rows))
axes = axes.flatten()
for i, col in enumerate(numeric_cols_all):
    axes[i].boxplot(df[col].dropna(), patch_artist=True,
                    boxprops=dict(facecolor='steelblue', alpha=0.7),
                    medianprops=dict(color='red', linewidth=2))
    axes[i].set_title(col, fontsize=11)
    axes[i].set_ylabel('Value')
for j in range(len(numeric_cols_all), len(axes)):
    axes[j].set_visible(False)
plt.suptitle('各特征箱线图 (Boxplot)', fontsize=16, y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'boxplot_all.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  已保存: charts/boxplot_all.png")

# =============================================================================
# 3. 单变量分析 - 直方图
# =============================================================================
print("\n[3] 单变量分析 - 分布直方图")
numeric_cols = [c for c in df.columns if df[c].dtype not in ['category']]
n_num_cols = len(numeric_cols)
n_rows_hist = (n_num_cols + 2) // 3
fig, axes = plt.subplots(n_rows_hist, 3, figsize=(18, 5 * n_rows_hist))
axes = axes.flatten()
for i, col in enumerate(numeric_cols):
    axes[i].hist(df[col].dropna(), bins=25, edgecolor='k', color='steelblue', alpha=0.7)
    axes[i].set_title(col, fontsize=11)
    axes[i].set_ylabel('Frequency')
for j in range(len(numeric_cols), len(axes)):
    axes[j].set_visible(False)
plt.suptitle('各特征分布直方图', fontsize=16, y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'hist_all.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  已保存: charts/hist_all.png")

# =============================================================================
# 4. 酸度分析
# =============================================================================
print("\n[4] 酸度分析")
acidity_cols = ['fixed acidity', 'volatile acidity', 'citric acid']
plt.figure(figsize=(12, 6))
bins = 10 ** (np.linspace(-2, 2, 30))
for col, label, alpha in zip(acidity_cols,
                               ['Fixed Acidity', 'Volatile Acidity', 'Citric Acid'],
                               [1.0, 1.0, 0.8]):
    plt.hist(df[col], bins=bins, edgecolor='k', label=label, alpha=alpha)
plt.xscale('log')
plt.xlabel('Acid Concentration (g/dm³)')
plt.ylabel('Frequency')
plt.title('Histogram of Acid Concentration')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'acid_histogram.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  已保存: charts/acid_histogram.png")

# =============================================================================
# 5. 甜度分析
# =============================================================================
print("\n[5] 甜度分析")
# 甜度饼图
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sweetness_counts = df['sweetness_type'].value_counts()
colors_sweet = ['#66b3ff', '#99ff99', '#ffcc99', '#ff9999']
sizes = sweetness_counts.values.tolist()
min_idx = sizes.index(min(sizes))
wedges, texts, autotexts = axes[0].pie(
    sweetness_counts.values,
    labels=None,
    autopct='%1.1f%%',
    colors=colors_sweet,
    startangle=90,
    textprops={'fontsize': 10, 'color': 'black', 'weight': 'bold'}
)
min_pct = sizes[min_idx] / sum(sizes) * 100
min_angle = (wedges[min_idx].theta2 + wedges[min_idx].theta1) / 2
x_start = 1.0 * np.cos(np.radians(min_angle))
y_start = 1.0 * np.sin(np.radians(min_angle))
x_end = 1.15 * np.cos(np.radians(min_angle))
y_end = 1.15 * np.sin(np.radians(min_angle))
x_text = 1.25 * np.cos(np.radians(min_angle))
y_text = 1.25 * np.sin(np.radians(min_angle))
if min_angle >= 0 and min_angle <= 30:
    x_text = 1.25 * np.cos(np.radians(min_angle))
    y_text = 1.25 * np.sin(np.radians(min_angle)) - 0.15
    ha = 'center'
    va = 'top'
else:
    ha = 'center'
    va = 'center'
autotexts[min_idx].set_text('')
axes[0].annotate(
    '',
    xy=(x_start, y_start),
    xytext=(x_end, y_end),
    arrowprops=dict(arrowstyle='->', lw=1.0, color='black')
)
axes[0].text(
    x_text, y_text, f'{min_pct:.1f}%',
    fontsize=9, weight='bold', color='black', ha=ha, va=va
)
axes[0].legend(
    wedges, sweetness_counts.index,
    title='Sweetness Type',
    loc='center left',
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=10
)
axes[0].set_title('Residual Sugar Distribution')
axes[1].hist(df['residual sugar'], bins=30, edgecolor='k', color='steelblue', alpha=0.7)
axes[1].axvline(x=4, color='red', linestyle='--', label='Dry ≤ 4 g/L')
axes[1].set_xlabel('Residual Sugar (g/dm³)')
axes[1].set_ylabel('Frequency')
axes[1].set_title('Residual Sugar Histogram')
axes[1].legend()
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'sweetness_analysis.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  已保存: charts/sweetness_analysis.png")

# =============================================================================
# 6. 相关性热力图
# =============================================================================
print("\n[6] 相关性分析")
# 删除分类列以计算相关性
df_corr = df.drop(columns=['sweetness_type'], errors='ignore')
corr_matrix = df_corr.corr()

plt.figure(figsize=(14, 10))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='RdBu_r',
            mask=mask, vmin=-1, vmax=1, square=True,
            linewidths=0.5, cbar_kws={'shrink': 0.8})
plt.title('特征相关性热力图', fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'correlation_heatmap.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  已保存: charts/correlation_heatmap.png")

# 打印与品质的相关性排名
quality_corr = corr_matrix['quality'].drop('quality').sort_values(key=abs, ascending=False)
print("\n  各特征与品质的相关性排名:")
for feat, corr in quality_corr.items():
    print(f"    {feat:25s}: {corr:+.3f}")

# =============================================================================
# 7. 双变量分析: 品质 vs 各理化特征
# =============================================================================
print("\n[7] 双变量分析: 品质 vs 各理化特征")

# 7.1 品质 vs 各特征箱线图
feature_cols = [c for c in df.columns if c not in ['quality', 'sweetness_type']]
fig, axes = plt.subplots(4, 3, figsize=(18, 18))
axes = axes.flatten()
for i, col in enumerate(feature_cols):
    data_for_box = [df[df['quality'] == q][col].values for q in sorted(df['quality'].unique())]
    bp = axes[i].boxplot(data_for_box, patch_artist=True,
                          boxprops=dict(facecolor='steelblue', alpha=0.6),
                          medianprops=dict(color='red', linewidth=1.5))
    axes[i].set_title(f'{col} vs Quality', fontsize=10)
    axes[i].set_xlabel('Quality')
    axes[i].set_ylabel(col)
    axes[i].set_xticklabels(sorted(df['quality'].unique()))
for j in range(len(feature_cols), len(axes)):
    axes[j].set_visible(False)
plt.suptitle('红酒品质与各理化特征的关系', fontsize=16, y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'quality_vs_features.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  已保存: charts/quality_vs_features.png")

# 7.2 密度 vs 酒精度
print("\n  [密度与酒精浓度关系]")
plt.figure(figsize=(10, 7))
scatter = plt.scatter(df['alcohol'], df['density'], c=df['quality'],
                      cmap='RdYlGn', alpha=0.6, edgecolors='k', linewidth=0.3)
plt.colorbar(scatter, label='Quality')
plt.xlabel('Alcohol (% vol)')
plt.ylabel('Density (g/cm³)')
plt.title('Density vs Alcohol Concentration')
# 添加趋势线
z = np.polyfit(df['alcohol'], df['density'], 1)
p = np.poly1d(z)
x_trend = np.linspace(df['alcohol'].min(), df['alcohol'].max(), 100)
plt.plot(x_trend, p(x_trend), 'r--', linewidth=2, label=f'Trend (ρ = {z[0]:.4f}×alc + {z[1]:.4f})')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'density_vs_alcohol.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  已保存: charts/density_vs_alcohol.png")

# 7.3 pH vs 酸度
print("\n  [pH与酸度关系]")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].scatter(df['fixed acidity'], df['pH'], c=df['quality'],
                cmap='RdYlGn', alpha=0.6, edgecolors='k', linewidth=0.3)
axes[0].set_xlabel('Fixed Acidity (g/dm³)')
axes[0].set_ylabel('pH')
axes[0].set_title('pH vs Fixed Acidity (corr = -0.683)')

axes[1].scatter(df['total acidity'], df['pH'], c=df['quality'],
                cmap='RdYlGn', alpha=0.6, edgecolors='k', linewidth=0.3)
axes[1].set_xlabel('Total Acidity (g/dm³)')
axes[1].set_ylabel('pH')
axes[1].set_title('pH vs Total Acidity')
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'ph_vs_acidity.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  已保存: charts/ph_vs_acidity.png")

# =============================================================================
# 8. 多变量分析
# =============================================================================
print("\n[8] 多变量分析")

# 8.1 酒精-挥发性酸-柠檬酸 三联图
top3_features = ['alcohol', 'volatile acidity', 'citric acid']
print(f"  与品质相关性最高的三个特征: {top3_features}")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# alcohol vs volatile acidity 着色品质
sc1 = axes[0].scatter(df['alcohol'], df['volatile acidity'],
                       c=df['quality'], cmap='RdYlGn', alpha=0.6, edgecolors='k', linewidth=0.3)
axes[0].set_xlabel('Alcohol (% vol)')
axes[0].set_ylabel('Volatile Acidity (g/dm³)')
axes[0].set_title('Alcohol vs Volatile Acidity\n(colored by Quality)')
plt.colorbar(sc1, ax=axes[0], label='Quality')

# alcohol vs citric acid
sc2 = axes[1].scatter(df['alcohol'], df['citric acid'],
                       c=df['quality'], cmap='RdYlGn', alpha=0.6, edgecolors='k', linewidth=0.3)
axes[1].set_xlabel('Alcohol (% vol)')
axes[1].set_ylabel('Citric Acid (g/dm³)')
axes[1].set_title('Alcohol vs Citric Acid\n(colored by Quality)')
plt.colorbar(sc2, ax=axes[1], label='Quality')

# pH vs fixed acidity vs citric acid
sc3 = axes[2].scatter(df['fixed acidity'], df['pH'],
                       c=df['citric acid'], cmap='plasma', alpha=0.6, edgecolors='k', linewidth=0.3)
axes[2].set_xlabel('Fixed Acidity (g/dm³)')
axes[2].set_ylabel('pH')
axes[2].set_title('pH vs Fixed Acidity\n(colored by Citric Acid)')
plt.colorbar(sc3, ax=axes[2], label='Citric Acid')

plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'multivariate_analysis.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  已保存: charts/multivariate_analysis.png")

# 8.2 Pairplot
print("\n  [Pairplot - 特征关系矩阵]")
top_features = ['alcohol', 'volatile acidity', 'citric acid', 'sulphates', 'density', 'quality']
pairplot_fig = sns.pairplot(df[top_features], diag_kind='kde',
                             plot_kws={'alpha': 0.5, 's': 15, 'edgecolor': 'k', 'linewidth': 0.2},
                             diag_kws={'fill': True})
pairplot_fig.fig.suptitle('Pairplot of Top Features', fontsize=16, y=1.02)
pairplot_fig.savefig(os.path.join(CHARTS_DIR, 'pairplot.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  已保存: charts/pairplot.png")

# =============================================================================
# 汇总
# =============================================================================
print("\n" + "=" * 70)
print("EDA 完成！共生成以下图表:")
for f in sorted(os.listdir(CHARTS_DIR)):
    print(f"  - charts/{f}")

print("\n>>> EDA 完成，请运行 04_modeling.py 继续 <<<")

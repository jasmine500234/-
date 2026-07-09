import numpy as np
import matplotlib.pyplot as plt

# 一：
print("=============任务1：NumPy数组基础操作=============")
# 1. 创建1维、2维、3维数组
arr_1d = np.array([1, 2, 3, 4, 5])
arr_2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
arr_3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print("1维数组：\n", arr_1d)
print("2维数组：\n", arr_2d)
print("3维数组：\n", arr_3d)
print(f"1D形状:{arr_1d.shape}, 2D形状:{arr_2d.shape}, 3D形状:{arr_3d.shape}\n")

# 2. 索引和切片
print("====数组索引与切片====")
print("2D数组第2行第3个元素：", arr_2d[1, 2])
print("2D数组前两行：\n", arr_2d[:2, :])
print("2D数组最后一列：", arr_2d[:, -1])

# 3. 形状变换
reshape_arr = arr_2d.reshape(9, )
transpose_arr = arr_2d.T
print("reshape展平：", reshape_arr)
print("矩阵转置：\n", transpose_arr)

# 4. 手动编写矩阵运算函数（加法、矩阵乘法、转置）
def mat_add(A, B):
    """矩阵加法"""
    return np.add(A, B)

def mat_mul(A, B):
    """矩阵乘法"""
    return np.matmul(A, B)

def mat_transpose(A):
    """矩阵转置"""
    return A.T

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print("\n====自定义矩阵运算====")
print("矩阵相加：\n", mat_add(A, B))
print("矩阵相乘：\n", mat_mul(A, B))
print("矩阵转置：\n", mat_transpose(A))

# 5. 随机数据 + 统计分析
rand_data = np.random.randn(20)
print("\n====随机数组统计分析====")
print(f"均值:{np.mean(rand_data):.2f},方差:{np.var(rand_data):.2f},标准差:{np.std(rand_data):.2f}")
print("最大值：", np.max(rand_data), "最小值：", np.min(rand_data))

# 二：
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
print("\n=============任务2：金融数据分析实战=============")
# 1.生成模拟股票数据（100个交易日）
np.random.seed(42)
days = 100
price = 100 + np.cumsum(np.random.normal(loc=0, scale=1.2, size=days))

# (1)计算每日对数收益率
returns = np.log(price[1:] / price[:-1])
annual_vol = np.std(returns) * np.sqrt(252)
print(f"年化波动率：{annual_vol:.3f}")

# (2) 5日、20‑日移动平均线
def moving_average(data, window):
    return np.convolve(data, np.ones(window) / window, mode="valid")

ma5 = moving_average(price, 5)
ma20 = moving_average(price, 20)

# (3)投资组合风险分析：3只股票
stock1 = np.random.normal(0.002, 0.012, days)
stock2 = np.random.normal(0.001, 0.010, days)
stock3 = np.random.normal(0.0015, 0.014, days)
port_data = np.vstack([stock1, stock2, stock3])

cov_matrix = np.cov(port_data)   # 协方差矩阵
corr_matrix = np.corrcoef(port_data) #相关系数矩阵
print("协方差矩阵：\n", cov_matrix)
print("相关系数矩阵：\n", corr_matrix)

# 4.绘图可视化
fig, axes = plt.subplots(2, 1, figsize=(12, 8))
# 第一张图
axes[0].plot(np.arange(days), price, label="Original Price", color="#4477dd")
axes[0].plot(np.arange(4, days), ma5, label="MA‑5", color="#ee7733")
axes[0].plot(np.arange(19, days), ma20, label="MA‑20", color="#22aa55")
axes[0].set_title("Stock Price and Moving‑Average")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# 第二张图
axes[1].plot(np.arange(len(returns)), returns, color="#9944bb")
axes[1].set_title("Daily Log‑Returns")
axes[1].axhline(y=0, color="red", linestyle="--")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
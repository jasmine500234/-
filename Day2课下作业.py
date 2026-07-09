import numpy as np
import timeit

# =========================练习1：矩阵运算与性能优化========================
# 1.矩阵乘法性能对比
np.random.seed(42)
A = np.random.rand(1000, 2000)
B = np.random.rand(2000, 3000)

def func_dot():
    return np.dot(A, B)

def func_at():
    return A @ B

def func_matmul():
    return np.matmul(A, B)

# %timeit 等价的Python代码测量运行时间
t1 = timeit.timeit(func_dot, number=3)
t2 = timeit.timeit(func_at, number=3)
t3 = timeit.timeit(func_matmul, number=3)

print("==========1.矩阵乘法耗时(运行3次)==========")
print(f"np.dot耗时：{t1:.2f} 秒")
print(f"@运算符耗时：{t2:.2f} 秒")
print(f"np.matmul耗时：{t3:.2f} 秒")
print("分析：底层实现上 @ 和 np.matmul 完全一致；np.dot 在二维矩阵场景下和matmul性能几乎相同，内部都会调用BLAS高性能库，细微差距来自函数调用开销；对于高维数组dot行为和matmul不同。\n")

# 2.内存布局（C‑order行优先 vs F‑order列优先）
arr_c = np.random.rand(1000, 1000)   # 默认order='C'，行优先存储
arr_f = np.array(arr_c, order="F")   # Fortran列优先存储

# 按行求和
time_c_row = timeit.timeit(lambda: arr_c.sum(axis=1), number=20)
time_f_row = timeit.timeit(lambda: arr_f.sum(axis=1), number=20)
# 按列求和
time_c_col = timeit.timeit(lambda: arr_c.sum(axis=0), number=20)
time_f_col = timeit.timeit(lambda: arr_f.sum(axis=0), number=20)

print("==========2.内存布局耗时==========")
print(f"C顺序数组按行求和：{time_c_row:.2f}")
print(f"F顺序数组按行求和：{time_f_row:.2f}")
print(f"C顺序数组按列求和：{time_c_col:.2f}")
print(f"F顺序数组按列求和：{time_f_col:.2f}")
print("分析：C顺序(行优先)，访问同一行元素内存连续，按行求和速度更快；F‑order列优先，同一列内存连续，按列求和更快。CPU缓存会优先加载连续内存的数据，离散访问会造成缓存缺失，速度下降。\n")

# 3.避免临时内存分配，计算 A^2 + 2*A +1
A_small = np.random.rand(800, 800)
result = np.empty_like(A_small)
# 使用np.add、np.multiply配合out参数，全程不产生临时数组
np.add(np.multiply(A_small, A_small, out=result), np.multiply(2, A_small), out=result)
np.add(result, 1, out=result)
print("==========3.避免临时内存分配完成==========\n")


# =====================练习2：金融数据分析实战=====================
# 1.股票对数收益率
prices = np.array([100, 102, 105, 103, 107])
returns = np.log(prices[1:] / prices[:-1])
print("1.每日对数收益率：")
print(returns, "\n")

# 2.移动平均线MA：生成100天随机股价
np.random.seed(42)
price_100 = np.random.normal(loc=100, scale=3, size=100)

def moving_avg_conv(data, window):
    return np.convolve(data, np.ones(window)/window, mode="valid")

ma5 = moving_avg_conv(price_100,5)
ma20 = moving_avg_conv(price_100,20)
print("2.5‑日均线：\n",ma5)
print("20‑日均线：\n",ma20,"\n")

# 3.风险分析：1000支股票，252个交易日
return_data = np.random.normal(loc=0, scale=0.01, size=(1000,252))
# 年化波动率 = 日标准差 × sqrt(252)
annual_vol = np.std(return_data, axis=1) * np.sqrt(252)
# 相关系数矩阵，np.corrcoef要求每行代表一只股票
corr_matrix = np.corrcoef(return_data)

print("3.每支股票年化波动率(前5个)：")
print(annual_vol[:5])
print("股票相关系数矩阵shape：", corr_matrix.shape)

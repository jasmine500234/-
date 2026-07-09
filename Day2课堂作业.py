import numpy as np
np.random.seed(0)
# 练习1
arr = np.random.randint(0, 10, size=(3, 4))
print("原始数组 arr：")
print(arr)

reshaped_arr = arr.reshape(4, 3).T
print("\nreshape(4,3)后转置：")
print(reshaped_arr)

filtered_arr = arr[arr > 5]
print("\n大于5的元素：")
print(filtered_arr)

# 练习2
arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
print("原数组：")
print(arr)

part1 = arr[1, 0:3]
print("\n任务1：第2行1~3列：", part1)

part2 = arr[:, 2]
print("任务2：所有行第3列：", part2)

part3 = arr[::2, :]
print("任务3：奇数行：")
print(part3)

# 练习3
A = np.random.randint(1, 6, size=(2, 3))
B = np.random.randint(1, 6, size=(2, 3))
print("A:\n", A)
print("B:\n", B)

elem_mul = A * B   
mat_mul = A @ B.T        
print("\n逐元素乘法 A*B：\n", elem_mul)
print("矩阵乘法 A @ B.T：\n", mat_mul)

M = np.array([[1, 2], [3, 4]])
sum_col = np.sum(M, axis=0)   
sum_row = np.sum(M, axis=1)   
print("\n数组M：\n", M)
print("按列求和(axis=0):", sum_col)
print("按行求和(axis=1):", sum_row)

vec = np.array([1.2, 3.5, 2.8])
mean_v = np.mean(vec)
std_v = np.std(vec)
round_v = np.round(vec)
print("\nvec =", vec)
print("均值：", mean_v)
print("标准差：", std_v)
print("四舍五入：", round_v)

# 练习4
x = np.random.rand(10)
print("原始浮点数组 x：\n", x)

x_min = x.min()
x_max = x.max()
x_norm = (x - x_min) / (x_max - x_min) * 100
print("\n归一化到0~100：\n", x_norm)

cumsum_x = np.cumsum(x_norm)
cummax_x = np.maximum.accumulate(x_norm)
print("\n累计和 cumsum：\n", cumsum_x)
print("累计最大值 cummax：\n", cummax_x)

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 参数
a = 1.0
n = 100
lim = 3

# 构建二维网格
x = np.linspace(-lim, lim, n)
y = np.linspace(-lim, lim, n)
X, Y = np.meshgrid(x, y)

# 计算二维高斯函数值作为高度 Z (z = f(x, y))
Z = np.exp(-a * (X**2 + Y**2))

# 绘图
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制曲面
surf = ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=0, antialiased=False)


ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# 添加颜色条
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
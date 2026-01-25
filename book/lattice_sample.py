import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

# 设置图形
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# 定义变换矩阵 A (虽然图中不需要显示数值，但需要一个具体的A来生成图形)
# 选择一个非对角矩阵以展示一般性
A = np.array([[1.5, 0.5], 
              [0, 1]])

# 计算对偶矩阵 A^{-T}
# A^{-1} = [[1/1.5, -0.5/1.5], [0, 1]] = [[2/3, -1/3], [0, 1]]
# A^{-T} = [[2/3, 0], [-1/3, 1]]
A_inv_T = np.linalg.inv(A).T

# ==========================================
# 左图：空间域上的采样点 (位于对偶格 L^*)
# ==========================================

# 对偶基向量 (L^* 的基)
u_star_1 = A_inv_T[:, 0]
u_star_2 = A_inv_T[:, 1]

# 生成网格点
k_range = 5
k_vals = np.arange(-k_range, k_range + 1)
K1, K2 = np.meshgrid(k_vals, k_vals)
K1_flat = K1.flatten()
K2_flat = K2.flatten()

# 计算采样点坐标: x = k1 * u_star_1 + k2 * u_star_2
X_samples = K1_flat * u_star_1[0] + K2_flat * u_star_2[0]
Y_samples = K1_flat * u_star_1[1] + K2_flat * u_star_2[1]

# 设置显示范围
limit_left = 3.5
mask = (np.abs(X_samples) < limit_left + 0.5) & (np.abs(Y_samples) < limit_left + 0.5)

# 绘制采样点
ax1.scatter(X_samples[mask], Y_samples[mask], color='black', s=15, zorder=5)

# 画坐标轴 (不标注)
ax1.plot([-limit_left, limit_left], [0, 0], 'k-', lw=1, zorder=1)
ax1.plot([0, 0], [-limit_left, limit_left], 'k-', lw=1, zorder=1)

# 画基向量
origin = [0, 0]
# 稍微加粗基向量以示区分
ax1.quiver(*origin, *u_star_1, color='red', angles='xy', scale_units='xy', scale=1, width=0.012, zorder=10)
ax1.quiver(*origin, *u_star_2, color='red', angles='xy', scale_units='xy', scale=1, width=0.012, zorder=10)

# 标注基向量名称
ax1.text(u_star_1[0], u_star_1[1]-0.3, r'$\mathbf{u}^*_1$', color='red', fontsize=14, fontweight='bold')
ax1.text(u_star_2[0]-0.3, u_star_2[1], r'$\mathbf{u}^*_2$', color='red', fontsize=14, fontweight='bold')

# 设置属性
ax1.set_xlim(-limit_left, limit_left)
ax1.set_ylim(-limit_left, limit_left)
ax1.set_aspect('equal')
ax1.axis('off') # 不显示外框和刻度


# ==========================================
# 右图：频域上的带限区域 (L 的基本平行四边形)
# ==========================================

# 原基向量 (L 的基)
u_1 = A[:, 0]
u_2 = A[:, 1]

# 计算基本平行四边形的顶点 (中心在原点)
# 区域由 { x1*u1 + x2*u2 | |x1|<=0.5, |x2|<=0.5 } 定义
v1 = -0.5 * u_1 - 0.5 * u_2
v2 = 0.5 * u_1 - 0.5 * u_2
v3 = 0.5 * u_1 + 0.5 * u_2
v4 = -0.5 * u_1 + 0.5 * u_2
poly_points = np.array([v1, v2, v3, v4])

# 绘制浅色阴影区域
polygon = Polygon(poly_points, closed=True, facecolor='skyblue', alpha=0.5, edgecolor='blue', linewidth=1.5, zorder=5)
ax2.add_patch(polygon)

# 设置显示范围
limit_right = 2
ax2.plot([-limit_right, limit_right], [0, 0], 'k-', lw=1, zorder=1)
ax2.plot([0, 0], [-limit_right, limit_right], 'k-', lw=1, zorder=1)

# 画基向量
# 注意：基向量长度是区域边长的两倍(从原点出发)，所以会超出阴影区域
ax2.quiver(*origin, *u_1, color='blue', angles='xy', scale_units='xy', scale=1, width=0.012, zorder=10)
ax2.quiver(*origin, *u_2, color='blue', angles='xy', scale_units='xy', scale=1, width=0.012, zorder=10)

# 标注基向量名称
ax2.text(u_1[0], u_1[1]-0.2, r'$\mathbf{u}_1$', color='blue', fontsize=14, fontweight='bold')
ax2.text(u_2[0]-0.2, u_2[1], r'$\mathbf{u}_2$', color='blue', fontsize=14, fontweight='bold')

# 设置属性
ax2.set_xlim(-limit_right, limit_right)
ax2.set_ylim(-limit_right, limit_right)
ax2.set_aspect('equal')
ax2.axis('off')

plt.tight_layout()
plt.show()

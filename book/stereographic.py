import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 设置中文字体，防止乱码 (Try to set a font that supports Chinese, fallback to default if not found)
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def inverse_stereographic(x, y):
    """
    Maps a point (x, y) on the complex plane to the unit sphere.
    Projection from North Pole (0, 0, 1) to the plane z=0.
    """
    denom = x**2 + y**2 + 1
    X = 2*x / denom
    Y = 2*y / denom
    Z = (x**2 + y**2 - 1) / denom
    return X, Y, Z

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# 1. 绘制单位球 (Draw the unit sphere)
u = np.linspace(0, 2 * np.pi, 50)
v = np.linspace(0, np.pi, 50)
x_sphere = np.outer(np.cos(u), np.sin(v))
y_sphere = np.outer(np.sin(u), np.sin(v))
z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))

# 绘制半透明球面
ax.plot_surface(x_sphere, y_sphere, z_sphere, color='c', alpha=0.1, edgecolor='none')
# 绘制经纬线 (Wireframe)
ax.plot_wireframe(x_sphere, y_sphere, z_sphere, color='k', alpha=0.05, rstride=5, cstride=5)

# 2. 绘制复平面 (z=0) (Draw the complex plane)
grid_range = 2
xx, yy = np.meshgrid(np.linspace(-grid_range, grid_range, 10), np.linspace(-grid_range, grid_range, 10))
zz = np.zeros_like(xx)
ax.plot_surface(xx, yy, zz, alpha=0.1, color='gray')

# 绘制单位圆 (Unit circle on plane)
theta = np.linspace(0, 2*np.pi, 100)
xc = np.cos(theta)
yc = np.sin(theta)
zc = np.zeros_like(theta)
ax.plot(xc, yc, zc, 'g-', linewidth=2, label='Unit Circle (Equator)')

# 3. 定义关键点 (Define points)
# 北极点 (North Pole)
N = np.array([0, 0, 1])
ax.scatter(N[0], N[1], N[2], color='k', s=60, label='North Pole (Infinity)')
ax.text(N[0], N[1], N[2]+0.1, 'N (0,0,1)', fontsize=10)

# 点1：单位圆内 (Inside Unit Circle) -> 南半球 (Southern Hemisphere)
# z1 = 0.6 + 0.2i (First quadrant, small angle)
p1_plane = np.array([0.6, 0.2, 0])
p1_sphere = inverse_stereographic(p1_plane[0], p1_plane[1])

# 点2：单位圆外 (Outside Unit Circle) -> 北半球 (Northern Hemisphere)
# z2 = -1.0 + 1.5i (Second quadrant, different angle)
p2_plane = np.array([-1.0, 1.5, 0])
p2_sphere = inverse_stereographic(p2_plane[0], p2_plane[1])

# 4. 绘制点和连线 (Plot points and lines)

# Point 1 (Inside)
ax.scatter(p1_plane[0], p1_plane[1], p1_plane[2], color='b', s=50)
ax.scatter(p1_sphere[0], p1_sphere[1], p1_sphere[2], color='b', s=50)
# Line from N to Sphere Point (since P1 is further than z1)
ax.plot([N[0], p1_sphere[0]], [N[1], p1_sphere[1]], [N[2], p1_sphere[2]], 'b--', alpha=0.5)
ax.text(p1_plane[0], p1_plane[1], p1_plane[2]-0.2, '$z_1$', fontsize=12, color='b')
ax.text(p1_sphere[0], p1_sphere[1], p1_sphere[2]-0.2, '$P_1$', fontsize=12, color='b')

# Point 2 (Outside)
ax.scatter(p2_plane[0], p2_plane[1], p2_plane[2], color='r', s=50)
ax.scatter(p2_sphere[0], p2_sphere[1], p2_sphere[2], color='r', s=50)
# Line from N to Plane Point (since z2 is further than P2)
ax.plot([N[0], p2_plane[0]], [N[1], p2_plane[1]], [N[2], p2_plane[2]], 'r--', alpha=0.5)
ax.text(p2_plane[0], p2_plane[1], p2_plane[2]-0.2, '$z_2$', fontsize=12, color='r')
ax.text(p2_sphere[0], p2_sphere[1], p2_sphere[2]+0.1, '$P_2$', fontsize=12, color='r')

# 坐标轴设置
# 移除默认坐标轴和背景
ax.set_axis_off()

# 设置等比例缩放，使球体看起来是圆的
# 注意：set_box_aspect 是 matplotlib 3.3+ 的功能
try:
    ax.set_box_aspect([1, 1, 1])
except AttributeError:
    # 对于旧版本 matplotlib，可能需要其他方法，或者忽略
    pass

# 设置坐标轴范围，保证比例正确
ax.set_xlim([-grid_range, grid_range])
ax.set_ylim([-grid_range, grid_range])
ax.set_zlim([-grid_range, grid_range]) # Z轴也设为同样的范围以保持比例

# 调整视角
ax.view_init(elev=20, azim=45)
ax.dist = 5.5  # Zoom in further (default is usually 10)

# 减少空白
plt.subplots_adjust(left=0, right=1, bottom=0, top=1)

plt.show()

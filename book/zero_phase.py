import numpy as np
import matplotlib.pyplot as plt

# 设置 xi
# 减小模长以增大零相面间距 d = 1 / |xi|
# xi = (0.5, 1.0) => |xi| = sqrt(1.25) approx 1.118 => d approx 0.89
xi = np.array([0.5, 1.0])

# 设置绘图范围
xlim = (-2.5, 2.5)
ylim = (-2.5, 2.5)

plt.figure(figsize=(8, 8))

# 绘制零相线: 0.5x + 1.0y = n  =>  y = n - 0.5x
# 只需要显示几条零相面 (-2 到 2)
n_values = range(-2, 3)

x_line = np.linspace(xlim[0], xlim[1], 100)

for n in n_values:
    y_line = n - 0.5 * x_line
    
    # 过滤掉超出 y 范围的点，以便绘图整洁
    mask = (y_line >= ylim[0]) & (y_line <= ylim[1])
    if np.any(mask):
        plt.plot(x_line[mask], y_line[mask], color='cornflowerblue', linewidth=1.5)
        
        # 在直线上标注 n
        # 挑选合适的位置标注，尽量避开边缘
        valid_indices = np.where(mask)[0]
        # 取靠近中间稍偏右的位置，避免挡住中心区域
        lbl_idx = valid_indices[int(len(valid_indices) * 0.6)]
        
        plt.text(x_line[lbl_idx], y_line[lbl_idx] + 0.1, f'n={n}', 
                 fontsize=10, color='royalblue', fontweight='bold', 
                 verticalalignment='bottom', horizontalalignment='center')

# 绘制向量 xi
# length_includes_head=True 确保箭头尖端精确指向 (xi[0], xi[1])
plt.arrow(0, 0, xi[0], xi[1], 
          head_width=0.15, head_length=0.2, length_includes_head=True, 
          fc='red', ec='red', linewidth=2, label=r'$\boldsymbol{\xi}=(0.5, 1)$', zorder=5)

# 原点
plt.scatter([0], [0], color='black', s=20, zorder=5)

# 装饰
plt.xlim(xlim)
plt.ylim(ylim)
plt.axhline(0, color='k', linewidth=0.5)
plt.axvline(0, color='k', linewidth=0.5)
plt.grid(True, linestyle='--', alpha=0.3)
plt.xlabel('x')
plt.ylabel('y')
#plt.title(r'Zero Phase Lines in $\mathbb{R}^2$: $\mathbf{x} \cdot \boldsymbol{\xi} = n \Rightarrow 0.5x + y = n$')
plt.legend(loc='lower right')
plt.axis('equal')

plt.show()

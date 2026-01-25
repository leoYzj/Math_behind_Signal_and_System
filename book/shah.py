import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(12, 6))

# 定义整数点的范围
n_min = -5
n_max = 5
integer_points = np.arange(n_min, n_max + 1)

# 绘制x轴
# ax.axhline(y=0, color='black', linewidth=0.8)
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_color('none')
ax.set_yticks([]) # Hide y ticks as we only want the shape? "仅保留图形" usually implies minimal axis clutter.
# But user said "横轴画到y=0的位置上", implying x-axis is needed.
# Let's keep x-ticks but hide y-ticks/labels if "幅度" is removed.
# The user said "删去时间、幅度两个词", so labels are gone.
# "不要标注每个箭头" -> text gone.
# "仅保留图形" -> maybe no ticks? But "横轴画到y=0" implies axis is visible.
# I will keep x-ticks as they are useful for the "comb" nature.

# 在每个整数点绘制单位长的箭头
for n in integer_points:
    # 创建箭头，从(n, 0)指向(n, 1)
    arrow = FancyArrow(n, 0, 0, 1, width=0.02, head_width=0.1, 
                      head_length=0.1, length_includes_head=True, 
                      fc='red', ec='red', alpha=0.7)
    ax.add_patch(arrow)
    
    # 在箭头旁边标注δ函数
    # ax.text(n + 0.1, 1.1, f'δ(t-{n})', fontsize=8, ha='left')

# 设置坐标轴范围
ax.set_xlim(n_min - 1, n_max + 1)
ax.set_ylim(-0.5, 1.8)

# 设置坐标轴标签
# ax.set_xlabel('时间 t', fontsize=12)
# ax.set_ylabel('幅度', fontsize=12)

# 设置标题
# ax.set_title('狄拉克梳状分布 (Dirac Comb) $\\sum_{n=-\\infty}^{\\infty} \\delta_n$', 
#              fontsize=14, pad=20)

# 添加网格
ax.grid(True, alpha=0.3, linestyle='--')

# 在整数点添加刻度标记
ax.set_xticks(integer_points)
ax.set_yticks([])

# 显示图形
plt.tight_layout()
plt.show()
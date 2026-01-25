import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
import matplotlib.patches as mpatches

def draw_finite_sampling_spectrum():
    # 设置中文字体，防止乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams.update({'font.size': 20})

    fig, ax = plt.subplots(figsize=(12, 5))

    # 参数设置 (用于绘图的定性值)
    T = 1.0
    N = 4
    fs = (2 * N + 1) / T
    
    # 定义频谱线 (Dirac combs)
    # 中心副本: k/T for k in -N to N
    k_central = np.arange(-N, N + 1)
    freq_central = k_central / T
    
    # 右侧副本: 以 fs 为中心
    k_right = np.arange(-N, N + 1)
    freq_right = (k_right / T) + fs
    
    # 左侧副本: 以 -fs 为中心
    k_left = np.arange(-N, N + 1)
    freq_left = (k_left / T) - fs

    # 绘制频谱线 (使用箭头表示 Dirac 分布)
    arrow_params = dict(head_width=0.2, head_length=0.15, length_includes_head=True)

    # 中心部分用蓝色
    for f in freq_central:
        ax.arrow(f, 0, 0, 1, fc='b', ec='b', **arrow_params)
        
    # 副本用灰色或浅色，表示周期化产生的
    for f in freq_right:
        ax.arrow(f, 0, 0, 1, fc='gray', ec='gray', alpha=0.6, **arrow_params)
        
    for f in freq_left:
        ax.arrow(f, 0, 0, 1, fc='gray', ec='gray', alpha=0.6, **arrow_params)

    # 绘制特征函数 (滤波器)
    # 矩形窗范围 [-fs/2, fs/2]
    # fs/2 = (N + 0.5)/T
    cutoff = fs / 2
    filter_height = 1.2
    
    # 绘制虚线框
    ax.plot([-cutoff, -cutoff, cutoff, cutoff], [0, filter_height, filter_height, 0], 'r--', linewidth=2, label='Characteristic Function')

    # 坐标轴设置
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.set_yticks([])
    ax.set_xticks([])
    
    # 标注关键信息
    
    # 1. 标注间隔 1/T
    # 绘制向下的大括号
    x1, x2 = 0, 1/T
    y = -0.05
    h = 0.1
    mid = (x1 + x2) / 2
    
    # Path codes
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    
    # Left half
    verts_left = [
        (x1, y), 
        (x1, y - h/2), 
        (mid - (x2-x1)/4, y - h), 
        (mid, y - h)
    ]
    
    # Right half
    verts_right = [
        (x2, y),
        (x2, y - h/2),
        (mid + (x2-x1)/4, y - h),
        (mid, y - h)
    ]
    
    path_left = Path(verts_left, codes)
    path_right = Path(verts_right, codes)
    
    ax.add_patch(mpatches.PathPatch(path_left, facecolor='none', edgecolor='k', lw=1.5))
    ax.add_patch(mpatches.PathPatch(path_right, facecolor='none', edgecolor='k', lw=1.5))
    
    ax.text(mid, y - h - 0.02, r'$1/T$', ha='center', va='top', fontsize=24)

    # 2. 标注带宽边界 N/T
    ax.text(N/T, -0.1, r'$N/T$', ha='center', fontsize=24)
    ax.text(-N/T, -0.1, r'$-N/T$', ha='center', fontsize=24)

    # 3. 标注采样频率 fs
    # ax.text(fs, -0.1, r'$f_s$', ha='center', fontsize=12)
    # 可以在 fs 处画一个虚线指示中心
    # ax.vlines(fs, 0, 1.3, colors='k', linestyles=':', alpha=0.3)

    # 4. 标注特征函数边界 fs/2
    # fs/2 位于 N/T 和 (N+1)/T 之间
    ax.text(cutoff, filter_height + 0.05, r'$f_s/2$', ha='center', color='r', fontsize=24)
    ax.text(-cutoff, filter_height + 0.05, r'$-f_s/2$', ha='center', color='r', fontsize=24)

    # 5. 标注 N (通过点数暗示，或者直接在标题/图例中说明)
    # 这里我们在 N/T 处已经体现了 N
    
    # 添加标题
    # ax.set_title('Finite Sampling Theorem: Spectrum Periodization and Reconstruction', y=1.05, fontsize=14)
    
    # 调整布局
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    draw_finite_sampling_spectrum()

import numpy as np
import matplotlib.pyplot as plt

def square_wave(x):
    """
    定义周期为 2pi 的方波信号
    0 < x < pi: 1
    -pi < x < 0: -1
    """
    # 使用 x % (2*pi) 将 x 映射到 [0, 2*pi)
    # 如果在 [0, pi) 范围内则为 1，否则为 -1
    return np.where(x % (2 * np.pi) < np.pi, 1, -1)

def fourier_series_sum(x, N):
    """
    计算方波的傅里叶级数部分和
    f(x) = (4/pi) * sum_{n=1, 3, ..., 2N-1} (1/n) * sin(n*x)
    这里 N 代表取前 N 个非零项（即奇数项）
    """
    result = np.zeros_like(x)
    # 累加前 N 个奇数项: k=1 对应 n=1, k=2 对应 n=3, ...
    for k in range(1, N + 1):
        n = 2 * k - 1
        result += (1 / n) * np.sin(n * x)
    return (4 / np.pi) * result

def plot_gibbs_phenomenon():
    # 设置中文字体，防止乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 定义 x 轴范围
    x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
    y_exact = square_wave(x)

    # 选择不同的项数 N 进行展示
    Ns = [1, 3, 10, 50]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    # fig.suptitle('Gibbs Phenomenon with Different Partial Sums', fontsize=16)

    for i, N in enumerate(Ns):
        row = i // 2
        col = i % 2
        ax = axes[row, col]
        
        y_approx = fourier_series_sum(x, N)
        
        # 绘制原信号（虚线）
        ax.plot(x, y_exact, 'k--', linewidth=1, alpha=0.5, label='原信号')
        # 绘制近似信号（实线）
        ax.plot(x, y_approx, 'b-', linewidth=1.5, label='部分和')
        
        ax.set_title(f'N = {N}')
        ax.set_ylim(-1.5, 1.5)
        ax.grid(True, alpha=0.3)
        
    # 全局图例
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', fontsize=14, bbox_to_anchor=(0.95, 0.95))

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_gibbs_phenomenon()

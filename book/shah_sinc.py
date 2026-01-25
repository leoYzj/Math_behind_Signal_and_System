import numpy as np
import matplotlib.pyplot as plt

# 近似狄拉克梳状分布的卷积和
# 公式: sum_{k=-N}^N sinc(t-k)

def plot_shah_sinc(N_list, t_range=(-5, 5), num=2000):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()
    for idx, N in enumerate(N_list):
        t_range = (-1.5*N, 1.5*N)
        t = np.linspace(t_range[0], t_range[1], num)
        y = np.zeros_like(t)
        for k in range(-N, N+1):
            y += np.sinc(t - k)
        axes[idx].plot(t, y)
        axes[idx].set_title(f"N={N}")
        axes[idx].set_xlabel("t")
        axes[idx].set_xlim(t_range)
        axes[idx].grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    N_list = [10, 50, 100, 200]
    plot_shah_sinc(N_list, t_range=(-5, 5), num=2000)

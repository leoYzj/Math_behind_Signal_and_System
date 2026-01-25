import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False

t = np.linspace(-3, 3, 600)

# 创建周期矩形脉冲
y1 = np.zeros_like(t)
pulse_positions = [-2, 0, 2]  # 脉冲中心位置
pulse_width = 1               # 脉冲宽度

for center in pulse_positions:
    mask = (t >= center - pulse_width/2) & (t <= center + pulse_width/2)
    y1[mask] = 1

# 加密频谱点数
w_dense = np.linspace(-2.5*np.pi, 2.5*np.pi, 100)  # 加密到100个点
Fk_dense = 0.5 * np.sinc(0.5 * w_dense)

# 为了对比，也画出连续的sinc函数
w_continuous = np.linspace(-2.5*np.pi, 2.5*np.pi, 1000)
sinc_continuous = 0.5 * np.sinc(0.5 * w_continuous)

# 绘图
plt.figure(figsize=(12, 10))

plt.subplot(2, 1, 1)
plt.title('周期矩形脉冲函数', fontsize=14)
plt.grid(True, alpha=0.3)
plt.plot(t, y1, 'b-', linewidth=2)
plt.xlabel('t')
plt.ylabel('幅度')
plt.xlim(-3, 3)

plt.subplot(2, 1, 2)
plt.title('双边频谱', fontsize=14)
plt.grid(True, alpha=0.3)

# 绘制连续的sinc函数
plt.plot(w_continuous, sinc_continuous, 'g-', linewidth=1, alpha=0.7, label='连续sinc函数')

# 绘制加密的stem图
plt.stem(w_dense, Fk_dense)

plt.xlabel('ω')
plt.ylabel('c_k')
plt.legend()
plt.xlim(-2.5*np.pi, 2.5*np.pi)

plt.tight_layout()
plt.show()
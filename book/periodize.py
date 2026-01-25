import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow

# 设置中文字体和图形参数
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建子图，调整高度比例减少空白
fig, axes = plt.subplots(2, 2, figsize=(14, 8))
plt.subplots_adjust(hspace=0.3, wspace=0.3)

# 参数设置
fs = 1000  # 采样频率
T = 2      # 信号时长
t = np.linspace(-T/2, T/2, int(fs * T), endpoint=False)
freq = np.fft.fftshift(np.fft.fftfreq(len(t), 1/fs))

# 1. 生成非周期偶信号
np.random.seed(42)

# 生成非周期函数（高斯脉冲的组合）
def non_periodic_function(t):
    # 使用多个高斯脉冲构建非周期信号
    result = np.zeros_like(t)
    # 添加几个不同位置和宽度的高斯脉冲
    pulses = [
        (0.3, 0.4, 1.0),   # (位置, 宽度, 幅度) - 增加宽度使频谱更均匀
        (-0.5, 0.5, 0.8),
        (0.0, 0.6, 0.9),
        (0.7, 0.3, 0.7)
    ]
    for pos, width, amp in pulses:
        result += amp * np.exp(-((t - pos) / width) ** 2)
    return result

# 构建偶信号：f(t) = g(t) + g(-t)
g_t = non_periodic_function(t)
original_signal = g_t + non_periodic_function(-t)

# 计算原信号的频谱
original_spectrum = np.fft.fftshift(np.fft.fft(original_signal)) / len(t)

# 绘制原信号的时域图
axes[0, 0].plot(t, original_signal, 'b-', linewidth=2)
axes[0, 0].set_xlabel('时间 (s)')
axes[0, 0].set_ylabel('幅度')
axes[0, 0].set_title('原信号 - 时域')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].set_xlim(-1, 1)

# 绘制原信号的频谱
axes[0, 1].plot(freq, np.abs(original_spectrum), 'b-', linewidth=2)
axes[0, 1].set_xlabel('频率 (Hz)')
axes[0, 1].set_ylabel('幅度')
axes[0, 1].set_title('原信号 - 频域')
axes[0, 1].set_xlim(-2, 2)
axes[0, 1].grid(True, alpha=0.3)

# 2. 周期化信号
T_period = 1.0  # 周期
N_periods = 5   # 显示的周期数

# 扩展时间轴以显示多个周期
t_extended = np.linspace(-N_periods*T_period/2, N_periods*T_period/2, 
                         int(fs * N_periods * T_period), endpoint=False)

# 创建周期化信号
periodic_signal = np.zeros_like(t_extended)
for n in range(-N_periods//2, N_periods//2 + 1):
    # 将原信号周期延拓
    periodic_signal += np.interp(t_extended - n * T_period, t, original_signal, 
                                left=0, right=0)

# 计算周期化信号的频谱
periodic_spectrum = np.fft.fftshift(np.fft.fft(periodic_signal)) / len(periodic_signal)
freq_extended = np.fft.fftshift(np.fft.fftfreq(len(t_extended), 1/fs))

# 绘制周期化信号的时域图
axes[1, 0].plot(t_extended, periodic_signal, 'r-', linewidth=2, label='周期化信号')
# 用浅色标出原信号（居中显示）
center_idx = len(t_extended) // 2
half_len = len(t) // 2
start_idx = center_idx - half_len
end_idx = center_idx + half_len
axes[1, 0].plot(t_extended[start_idx:end_idx], original_signal, 'b--', alpha=0.5, 
               linewidth=1.5, label='原信号')

# 标记周期边界
for n in range(-N_periods//2, N_periods//2 + 1):
    axes[1, 0].axvline(x=n * T_period, color='gray', linestyle=':', alpha=0.7)

axes[1, 0].set_xlabel('时间 (s)')
axes[1, 0].set_ylabel('幅度')
axes[1, 0].set_title(f'周期化信号 (T={T_period}s) - 时域')
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].legend()
axes[1, 0].set_xlim(-2, 2)

# 绘制周期化信号的频谱（用狄拉克箭头）
# 先用浅色绘制原信号频谱
axes[1, 1].plot(freq, np.abs(original_spectrum), 'b--', alpha=0.5, 
               linewidth=1.5, label='原信号频谱')

# 计算狄拉克梳的位置（基频的整数倍）
f0 = 1 / T_period  # 基频
max_harmonic = int(15 / f0)  # 显示到15Hz以内的谐波

# 用箭头表示狄拉克分布
for n in range(-max_harmonic, max_harmonic + 1):
    freq_pos = n * f0
    if abs(freq_pos) <= 15:  # 只在显示范围内绘制
        # 找到最接近的频率点的索引
        idx = np.argmin(np.abs(freq_extended - freq_pos))
        magnitude = np.abs(periodic_spectrum[idx]) * len(periodic_signal) / len(original_signal)
        
        # 绘制箭头 - 增加最小高度确保箭头可见
        min_height = 0.1  # 最小箭头高度
        arrow_height = max(magnitude, min_height)
        
        # 绘制箭头
        arrow = FancyArrow(freq_pos, 0, 0, arrow_height, 
                         width=0.02, head_width=0.05, head_length=0.05,
                         length_includes_head=True, fc='red', ec='red', alpha=0.8)
        axes[1, 1].add_patch(arrow)

# 添加周期化信号频谱的图例（使用红色箭头）
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='b', linestyle='--', alpha=0.5, linewidth=1.5, label='原信号频谱'),
    Line2D([0], [0], color='r', linewidth=2, label='周期化信号频谱')
]
axes[1, 1].legend(handles=legend_elements)

axes[1, 1].set_xlabel('频率 (Hz)')
axes[1, 1].set_ylabel('幅度')
axes[1, 1].set_title(f'周期化信号频谱 (狄拉克梳状分布)')
axes[1, 1].set_xlim(-2, 2)
axes[1, 1].set_ylim(0, 3.0)
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 打印频谱信息
print(f"周期化信号的基频: {f0:.2f} Hz")
print("显著的频率分量:")
for n in range(0, max_harmonic + 1):
    freq_pos = n * f0
    if abs(freq_pos) <= 15:
        idx = np.argmin(np.abs(freq_extended - freq_pos))
        magnitude = np.abs(periodic_spectrum[idx]) * len(periodic_signal) / len(original_signal)
        if magnitude > 0.01:
            print(f"  {freq_pos:.1f} Hz: 幅度 = {magnitude:.3f}")
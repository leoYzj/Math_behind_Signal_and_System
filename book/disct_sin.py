import numpy as np
import matplotlib.pylab as plt

plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False

Omega=5
t = np.linspace(0,5,30)
y=np.sin(Omega*t)

plt.stem(t,y)
plt.xlabel('t')
plt.title('离散正弦信号')
plt.show()
import numpy as np
import matplotlib.pylab as plt
from scipy import ndimage
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

t = np.linspace(-2,2,400)
R = np.heaviside(t+0.5,1)-np.heaviside(t-0.5,1)

# 直接通过参数平移创建函数，避免使用ndimage.shift
r1 = np.heaviside(t-1.5+0.5,1)-np.heaviside(t-1.5-0.5,1)  # 右移1.5
r2 = np.heaviside(t+0.25+0.5,1)-np.heaviside(t+0.25-0.5,1)  # 左移0.25

g=np.piecewise(t,[t<=-1,(t<0) & (t>-1),(t<1) & (t>=0),t>=1],
               [0,lambda t:1+t,lambda t:1-t,0])

plt.subplot(2,2,1)
plt.title('$\Pi$函数')
plt.xlabel('t')
plt.grid()
plt.plot(t,R)

plt.subplot(2,2,2)
plt.title('$|x|>1$')
plt.xlabel('t')
plt.grid()
plt.plot(t,R)
plt.plot(t,r1)
plt.legend(labels=['$\Pi(y)$', '$\Pi(x-y)$'])

plt.subplot(2,2,3)
plt.title('$|x|<1$')
plt.xlabel('t')
plt.grid()
plt.plot(t,R)
plt.plot(t,r2)
plt.legend(labels=['$\Pi(y)$', '$\Pi(x-y)$'])

# 计算重叠区域
overlap = np.minimum(R, r2)
plt.fill_between(t, overlap, where=(overlap > 0), alpha=0.3, color='red', label='重叠区域')

plt.subplot(2,2,4)
plt.title('$\Lambda$函数')
plt.xlabel('t')
plt.grid()
plt.plot(t,g)

plt.tight_layout()
conv=plt.show()
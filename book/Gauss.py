import numpy as np
import matplotlib.pylab as plt

t = np.linspace(-3,3,2000)
g=np.piecewise(t,[t<=-1,(t<0) & (t>-1),(t<1) & (t>=0),t>=1],
               [0,lambda t:1+t,lambda t:1-t,0])

plt.plot(t,g)
plt.grid()
plt.show()
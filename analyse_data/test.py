import matplotlib.pyplot as plt
import numpy as np

N = 100
r0 = 0.6
x = 0.9*np.random.rand(N)
y = 0.9*np.random.rand(N)
area = np.pi*(10 * np.random.rand(N))**2  # 0 to 10 point radiuses

c = np.sqrt(area)
r = np.sqrt(x*x + y*y)

area1 = np.ma.masked_where(r < r0, area)
area2 = np.ma.masked_where(r >= r0, area)

plt.scatter(x, y, s=area1, marker='^', c='r', hold='on')
plt.scatter(x, y, s=area2, marker='o', c='c')
# Show the boundary between the regions:
# theta = np.arange(0, np.pi/2, 0.01)
# plt.plot(r0*np.cos(theta), r0*np.sin(theta))

x = [1,2,3,4,5,6,7]
y = [2,5,6,7,8,10]

plt.scatter()





plt.show()
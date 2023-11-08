import matplotlib.pyplot as plt
import numpy as np
from pyads1292 import *

pyads1292 = Pyads1292()

pyads1292.clk = 10000
print(pyads1292.clk)

# ftest = 60
# N = 128000
# t = np.linspace(0, N/pyads1292.fmod, N)
# u = 0.5*np.sin(2*np.pi*ftest*t)      #Senal de testeo
#
# plt.figure(figsize=(20, 4))
# v, xn, xmax, y = pyads1292.simulateDSM(u)
# #t = np.arange(N)
# plt.step(t, u,'r')
# plt.step(t, v, 'g')
# plt.xlim((0,0.003))
# plt.xlabel('Sample Number')
# plt.ylabel('u, v')
# plt.title('Modulator Input & Output')
# plt.show()
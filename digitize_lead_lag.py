# For online discussion:
# https://www.reddit.com/r/ControlTheory/comments/c1w5r6/lead_lag_for_inexpensive_plc/
# To verify if my proposed solution is correct or not by simulation
# Digitization method: https://imgur.com/lnOZI8W
# Confirmed correct

import numpy as np
import matplotlib.pyplot as plt
import control

# parameter for a lag compensator
a = 5.0
b = 10.0

# Simulate continous transfer function response
sys = control.TransferFunction([a, 1], [b, 1])
dT = 1
T_max = 50.0
T = np.linspace(0.0, T_max, num=int(T_max/dT))

T, yout = control.step_response(sys, T)
# plt.figure(0)
# mag, phase, omega = control.bode_plot(sys)

# Simulate plot digitized version
c = np.zeros_like(T)
c[0] = (a + dT) / (b + dT)
for i in range(1, len(T)):
    c[i] = dT / (b + dT) * 1.0 + 0.0 + b / (b + dT) * c[i-1]

# plot both results in the same figure as comparison
plt.figure(2)
plt.plot(T, c)
plt.plot(T, yout)
plt.title('Step response')
plt.xlabel('Time (s)')
plt.legend({'Step response of digitized system at ' + str(dT) + ' sec', 
           'Step response of continous transfer function'})
plt.show()

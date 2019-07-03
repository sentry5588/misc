# For online discussion:
# https://www.reddit.com/r/controlengineering/comments/c8fui6/update_pid_controller_for_buck_converter/

import numpy as np
import matplotlib.pyplot as plt
import control

# Simulate continous transfer function response
sys = control.TransferFunction([2.812e7], [1, 1.397e4, 2.268e8])
# control.bode_plot(sys)
T_max = 1e-3
T = np.linspace(0.0, T_max, num=1000)
T, yout = control.step_response(sys, T)

plt.figure(2)
plt.plot(T, yout)
plt.title('Step response')
plt.xlabel('Time (s)')
plt.show()

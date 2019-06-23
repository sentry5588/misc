# Complementary filter uses a constant linear combination between
# two sensor measurements to estimate one system state.
# One is a incremental and the other one is direct.
# An integration of the incremental sensor is need to obtain an indirect
# measurement.
#
# Typically much more weight (0.98) is put on to the incremental 
# measurement, which has drift issues (low freq noise). 
# Less weight is put on to the direct measurement, 
# which is noisy (high freq noise).
# 
# The bode plot shows that the complementary filter resulting 
# *** a HIGH PASS filter for the incremental measurement
# *** a LOW PASS filter for the direct measurement
# and the summation is 1

import matplotlib.pyplot as plt
import control

alpha = 0.9 # The weight on the incremental measurement

dT = 0.1 # sample time
# TF from accumulative measurement to the final estimation
tf_a = control.TransferFunction([alpha, -alpha], [1, -alpha], dT)
# TF from direct measurement to the final estimation
tf_v = control.TransferFunction([1-alpha, 0.0], [1, -alpha], dT)

plt.figure(0)
p1 = control.bode_plot(tf_a)
p2 = control.bode_plot(tf_v)
print(tf_a, tf_v)

# Simply example of Kalman filter/estimator for speed estimation

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def speed_profile(t):
    v_true = np.zeros_like(t)
    for i in range(0, len(t)):
        if i < 800:
            v_true[i] = t[i] * 4
        elif i < 1000:
            v_true[i] = v_true[i-1]
        elif i < 1100:
            v_true[i] = v_true[999] - (t[i]-t[999]) * 8
        else:
            v_true[i] = v_true[1099] + \
                np.sin(0.2 * t[i] * (t[i]-t[1099])) * 5
    return v_true

matplotlib.pyplot.close("all")

dT = 0.01 # simulation time step
T_total = 21.12 # Total simulation time
t = np.linspace(0.0, T_total, num=int(T_total/dT + 1)) # time steps

# create variables
v_est = np.zeros_like(t) # estimated speed
v_pred = np.zeros_like(t) # predicted speed
v_meas = np.zeros_like(t) # measured speed from sensors
v_incr = np.zeros_like(t) # incremental speed calc'ed from accel sensor
a = np.zeros_like(t) # accelerometer reading
P_est = np.zeros_like(t) # speed estimation variance
P_priori = np.zeros_like(t) # predicted speed variance
P_total =  np.zeros_like(t) # Total variance for calc'ing Kalman gain
K = np.zeros_like(t) # Kalman gain
v_diff = np.zeros_like(t) 
v_corr = np.zeros_like(t)

# complementary filter
v_est_CF = np.zeros_like(t)
compl_factor = 0.98

# Define noise
Q = 0.001 # var of a
R = 0.002 # var of v_meas

# Initialize 
P_est[0] = 0.1
v_est[0] = v_meas[0]
v_est_CF[0] = v_meas[0]

# create input signals
a_noise = np.random.normal(0.0, np.sqrt(Q), len(t))
v_meas_noise = np.random.normal(0.0, np.sqrt(R), len(t))
print('Var of a_noise (Q={0:.2e}): {1:.2e} '\
      .format(Q, np.var(a_noise)))
print('Var of v_meas_noise (R={0:.2e}): {1:.2e}'\
      .format(R, np.var(v_meas_noise)))

v_true = speed_profile(t) # use the speed_profile function
v_meas = v_true + v_meas_noise
a_true = np.zeros_like(t)
a_true[0] = (v_true[1] - v_true[0]) / dT
a_true[len(t)-1] = (v_true[len(t)-1] - v_true[len(t)-2]) / dT
for i in range(1, len(t)-1):
    a_true[i] = (v_true[i+1] - v_true[i-1]) / (2.0 * dT)
a = a_true + a_noise

# %% Estimator logic
for i in range(1, len(t)):
    # Kalman prediction step
    v_incr[i] = (a[i] + a[i-1]) * 0.5 * dT
    v_pred[i] = v_est[i-1] + v_incr[i]
    P_priori[i] = P_est[i-1] + 0.5 * Q * dT * dT
    
    # Kalman correction/update step
    P_total[i] = P_priori[i] + R
    K[i] = P_priori[i] / P_total[i]
    v_est[i] = v_pred[i] + K[i] * (v_meas[i] - v_pred[i])
    P_est[i] = P_priori[i] - K[i] * P_priori[i]
    
    # Complementary 
    v_est_CF[i] = compl_factor * (v_est_CF[i-1] + v_incr[i]) \
        + (1 - compl_factor) * v_meas[i]

# %% plot data code section
f = plt.figure()
mngr = plt.get_current_fig_manager()
mngr.window.setGeometry(1600, -150, 1900, 1100)

# plot speed
ax_v = f.add_subplot(4,2,1)
ax_v.plot(t, v_meas)
ax_v.plot(t, v_est)
ax_v.plot(t, v_est_CF)
ax_v.plot(t, v_true)
ax_v.set_title('Speed estimation')
ax_v.legend(('Meas', 'Est Kalman', 'Est CF', 'True'))

# plot speed error
ax_err = f.add_subplot(4,2,2, sharex = ax_v)
ax_err.plot(t, v_meas - v_true)
ax_err.plot(t, v_est - v_true)
ax_err.plot(t, v_est_CF - v_true)
ax_err.set_title('Speed estimation Error')
ax_err.legend(('Meas Noise', 'Kalman Error', 'CF Error'))
ax_err.plot(t, np.zeros_like(t))

# plot variance 
plt.subplot(4,2,3, sharex = ax_v)
plt.plot(t, P_priori)
plt.plot(t, P_est)
plt.plot(t, P_total)
plt.plot(t, np.ones_like(t) * R)
plt.legend(('P_priori', 'P_est', 'P_total', 'R'))
plt.title('Variance')

# plot acceleration
plt.subplot(4,2,4, sharex = ax_v)
plt.plot(t, a)
plt.plot(t, a_true)
plt.legend(('a', 'a_true'))
plt.title('Acceleration')

# plot Kalman gain
plt.subplot(4,2,5)
plt.title('Kalman gain')
plt.plot(t, K)

plt.subplot(4,2,7)
plt.hist(v_meas_noise, bins = 50)
plt.title('V meas noise histogram')

plt.subplot(4,2,8)
plt.hist(a_noise, bins = 50)
plt.title('Accel noise histogram')

# statistic analysis
print('Var of Kalman Est Error: {0:.2e}'\
      .format(np.var(v_est[len(t)-500:len(t)] - v_true[len(t)-500:len(t)])))
print('Last P_est: {0:.2e}'.format(P_est[len(t)-1]))

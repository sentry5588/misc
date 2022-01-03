import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt

# alternative data: https://uhslc.soest.hawaii.edu/stations/?stn=007#levels


def load_tide_data(f):
    # use Pandas to read data and then convert to a numpy array
    d = pd.read_csv(f, header=None).to_numpy()
    return d

def fourier_coeff(w, d):
    d = d.flatten()
    T = np.array(list(range(0, d.shape[0])))
    e = np.exp(np.multiply(T, 1j*w*2*math.pi))
    fourier_a_b = sum(np.multiply(e, d)) / d.shape[0]
    
    # return fourier_integral.real, fourier_integral.imag
    return fourier_a_b

def main():
    d = load_tide_data('calq_rad_processed.csv')
    find_cycle(d, 10)
    d_mean = np.mean(d)
    d = d - d_mean
    
    N = d.shape[0]
    N_train = math.ceil(N*0.9) # Training data index
    
    N_train = 50 ################
    
    N_vali = 80
    d_train = d[0:N_train]
    d_vali = d[0:N_vali]
    print("N_train=", N_train, "N_vali=", N_vali)
    T = np.array(list(range(0, d_vali.shape[0])))
    
    d_train = np.sin(T*0.152145 - 0.5) ################
    d_vali = np.sin(T*0.152145 - 0.5) ################
    
    w = np.arange(1, d_train.shape[0]+1, 1) / d_train.shape[0]
    print("T.shape = ", T.shape, "w.shape = ", w.shape)
    F = np.full(w.shape[0], 0j)
    d_predict = 0 * d_vali.flatten()
    terms_count = 0
    for k in range(0, w.shape[0]):
        F[k] = fourier_coeff(w[k], d_train)
        if (np.abs(F[k]) > -0.001):
            # print("k=", k, ", w[", k, "]=", w[k], ", F[", k, "]=", F[k])
            d_predict = d_predict + F[k].real * np.cos(T*w[k]*2*np.pi)
            d_predict = d_predict + F[k].imag * np.sin(T*w[k]*2*np.pi)
            terms_count = terms_count + 1
    
    print(terms_count, "out of", w.shape[0], "terms of Fourier series are used.")
    # print("w[20] = ", w[20], "w[40] = ", w[40])
    
    plt.figure(0)
    plt.plot(d_train[0:N_train], 'o', markersize=10)
    plt.plot(d_vali, '.')
    # plt.plot(d_predict[N_train - 20 : N_train + 50])
    plt.plot(d_predict)
    plt.ylabel('Train data vs Fourier Series')
    plt.show()
    
    plt.figure(1)
    plt.plot(np.abs(F))
    plt.ylabel('Magnitude of F')
    plt.show()
    
    plt.plot(F.real)
    plt.plot(F.imag)
    plt.ylabel('Real and Imag of F')
    plt.show()
    

def find_cycle(d, N):
    cycle_flag = 0
    for m in range(N, d.shape[0]-N):
        # print("in for loop, m=", m, "d[m]=", d[m])
        n = 0
        while abs(d[n] - d[m+n]) < 0.03 and n < N:
            n = n + 1
        if n == N:
            cycle_flag = 1
            break
    print("at d[", m, "]=", d[m], ", it's the cycle")
    
if __name__ == "__main__":
    main()
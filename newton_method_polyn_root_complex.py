# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 17:07:36 2021

@author: jh
"""
import array as arr
import matplotlib.pyplot as plt

p = arr.array('d', [1, 5, 4])

def f(z):
   return p[0]*z**2 + p[1]*z + p[2]

def df(z):
   return 2*p[0]*z + p[1]
    
z = complex(-5, -3)
print("Initial value: ", z)

fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlim([-5, 5])
plt.ylim([-4, 4])
ax.set_aspect('equal', adjustable='box')

i = 0
while (i <= 6):
    i = i + 1
    if df(z) == 0:
        print("df is 0, exit!")
    else:
        z = z - f(z)/df(z)
        plt.scatter(z.real, z.imag, 20)
        print("After the", i, "-th iteration: ", z)

plt.ylabel('some numbers')
plt.show()

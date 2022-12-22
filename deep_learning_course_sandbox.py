# -*- coding: utf-8 -*-
"""
Test numpy and other python code that are used in deep learning course
"""
import numpy as np

X = np.array([[[0, 0, 0],
    [1, 1, 1]],
    [[100, 100, 100],
    [101, 101, 101]],
    [[200, 200, 200],
    [201, 201, 201]]])
X_flatten = X.reshape(X.shape[0], -1).T      # X.T is the transpose of X
print("X_flatten=", X_flatten)
print("X.shape=", X.shape)
print("X_flatten.shape=", X_flatten.shape)

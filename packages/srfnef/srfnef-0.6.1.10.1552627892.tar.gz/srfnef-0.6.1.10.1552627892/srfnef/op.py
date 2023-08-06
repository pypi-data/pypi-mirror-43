# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: op.py
@date: 3/4/2019
@desc:
'''

import math

from numba import float32, guvectorize


@guvectorize([(float32[:, :, :], float32, float32[:, :, :])], '(m,n,p),()->(m,n,p)',
             target = 'cuda')
def weighted_add(x, wei, y):
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            for k in range(x.shape[2]):
                y[i, j, k] += x[i, j, k] * wei


@guvectorize([(float32[:, :, :], float32, float32[:, :, :])], '(m,n,p),()->(m,n,p)',
             target = 'cuda')
def shift_ind_z(x, off, y):
    '''
    move a 3d image x with off forward and added on a same-shaped image y
    '''

    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            for k in range(x.shape[2]):
                ind1 = int(math.floor(k - off))
                ind2 = ind1 + 1
                wt2 = k - off - ind1
                wt1 = 1.0 - wt2
                print(k, ind1, ind2, wt1, wt2)
                if 0 <= ind1 and ind2 < x.shape[2]:
                    y[i, j, k] += x[i, j, ind1] * wt1 + x[i, j, ind2] * wt2
                elif ind2 == 0:
                    y[i, j, k] += x[i, j, 0] * wt2
                elif ind1 == x.shape[2] - 1:
                    y[i, j, k] += x[i, j, -1] * wt1
                else:
                    pass

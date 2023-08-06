# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: typings.py
@date: 3/13/2019
@desc:
'''
import typing

Vector = typing.List[float]
Index = typing.List[int]


class Vector3(Vector):
    def ndim(self):
        return 3


class Index3(Index):
    def ndim(self):
        return 3

#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# Use from hy:
#
# (require [minifiedpy [*]])
# (import [minifiedpy [F]])
# (print ((L x x) 1)) -> 1
import hy
from hy.core.language import first, is_coll, is_instance, last, reduce, rest, second
from hy import HyExpression, HyList, HySymbol

def A(x):
    return is_instance(F, x)

def B(x):
    return '(%s)' % ' '.join(map(B, x)) if is_coll(x) else str(x)

def C(x):
    return B(map(str, map(C, x))) if is_coll(x) and not A(x) else x

def D(x, y):
    while callable(x) and y:
        x = x(y.pop(0))
    if y:
        x.extend(y)
    return x

def E(x):
    if is_coll(x):
        if A(first(x)):
            return D(first(x), list(rest(x)))
        elif not A(x):
            y = list(map(E, x))
            return E(y) if A(first(y)) else y
    return x

class F(list):
    def __repr__(self):
        return "(\xce\xbb%s.%s)" % (first(self), C(second(self)))
    def __call__(self, x, *y):
        v = (lambda z: D(z, list(y)) if y else z)(E(last(self)(x)))
        return v if A(v) else B(v)

def G(_x, *x):
    v = list(x)
    v.reverse()
    return reduce(lambda y, z: HyExpression([] + [HyExpression([] + [
        HySymbol('fn')] + [HyList([])] + [HyExpression([] + [HySymbol(
        'setv')] + [z] + [HyExpression([] + [HySymbol('str')] + [
        HyExpression([] + [HySymbol('quote')] + [z])])])] + [HyExpression([
        ] + [HySymbol('F')] + [HyList([] + [HyExpression([] + [HySymbol(
        'quote')] + [z])] + [y] + [HyExpression([] + [HySymbol('fn')] + [
        HyList([] + [z])] + [y])])])])]), v)

hy.macros.macro('L')(G)

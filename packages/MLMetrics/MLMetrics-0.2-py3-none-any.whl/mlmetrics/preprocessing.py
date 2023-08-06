#!/usr/bin/env python
# encoding: utf-8

import math


def linear_normalize(column_series):
    """
    Normalize column data to 0~1 with linear function
    """
    column_min = column_series.min()
    column_max = column_series.max()
    return (column_series - column_min) / (column_max - column_min)


def log_normalize(column_series):
    """
    Normalize column data to 0~1 with log 10 function
    """
    column_max = column_series.max()
    return column_series.apply(lambda x: math.log10(x)/ math.log10(column_max))


def atan_normalize(column_series):
    """
    Normalize column data to 0~1 with atan function
    """
    return column_series.apply(lambda x: math.atan(x)*2/math.pi)

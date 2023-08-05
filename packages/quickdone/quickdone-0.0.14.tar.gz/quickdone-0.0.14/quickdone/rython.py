#!/usr/bin/env python
# coding: utf-8

import ctypes

fib=ctypes.CDLL('/test/quickdone/quickdone/libfib.so').fib
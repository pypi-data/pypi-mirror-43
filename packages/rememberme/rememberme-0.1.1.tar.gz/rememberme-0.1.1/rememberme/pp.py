import pstats, cProfile

import pyximport
pyximport.install()

import rememberme

from flask import Flask

def foo():
    f = Flask("b")
    for i in range(10):
        print(rememberme.memory(f))

cProfile.runctx("foo()", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()

import pstats, cProfile

#import pyximport
#pyximport.install()

import rememberme

from flask import Flask

def foo():
    for i in range(10):
        print(rememberme.memory(list(range(int(1e5)))))

cProfile.runctx("foo()", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()

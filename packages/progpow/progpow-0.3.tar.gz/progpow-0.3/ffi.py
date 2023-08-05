from cffi import FFI
from build_helper import absolute, ensure_system
ensure_system()

ffi = FFI()
with open("include/progpow.h", 'rt') as h:
    ffi.cdef(h.read())
include_path = absolute("include/")
ffi.set_source("_libprogpow", r'#include "progpow.h"', include_dirs = [include_path], libraries = ['progpow'])

ffi.compile()

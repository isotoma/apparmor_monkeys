from __future__ import absolute_import
import ctypes.util


_find_library = ctypes.util.find_library


libraries = {
    "c": "libc.so.6",
    "uuid": "libuuid.so.1",
}


def find_library(library):
    # Normally ctypes uses subprocess to invoke ldconfig. Whilst ldconfig is
    # relatively safe, we prefer to completely block our code from using
    # subprocess.
    if library not in libraries:
        raise RuntimeError(
            "Cannot find soname for {!r}. Please update {}".format(
                library,
                __name__
            )
        )
    return libraries[library]


def patch_module():
    ctypes.util.find_library = find_library

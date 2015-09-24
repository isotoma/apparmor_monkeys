from __future__ import absolute_import

import os
import platform
import sys


_uname = platform.uname


def uname():
    # platform.uname() is the same as os.uname(), but with extra data about the
    # processor. Unfortunately this needs to shell out and does something like
    # [sh, -c, "%s 2>%s"].
    # We avoid this - it saves us having to give our apparmor profile access to
    # run a full sh!!!
    processor = "x86_64" if sys.maxsize > 2 ** 32 else 'i686'
    return os.uname() + (processor, )
uname.__doc__ = _uname.__doc__


def patch_module():
    platform.uname = uname

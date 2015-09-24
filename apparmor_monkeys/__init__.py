from __future__ import absolute_import

import os
import ctypes as _ctypes
from . import ctypes, platform


__all__ = ["patch_modules", "change_profile"]


def patch_modules():
    ctypes.patch_module()
    platform.patch_module()


def change_profile(profile_name):
    apparmor = _ctypes.CDLL("libapparmor.so.1", use_errno=True)
    if apparmor.aa_change_profile(profile_name) < 0:
        error_code = _ctypes.get_errno()
        raise RuntimeError("Cannot change profile to {!r}. Result: {}".format(
            profile_name,
            os.strerror(error_code),
        ))

import unittest
from . import ctypes, platform


class TestCtypes(unittest.TestCase):

    def test_all_libraries_match(self):
        for library, soname in ctypes.libraries.items():
            self.assertEqual(
                ctypes.find_library(library),
                ctypes._find_library(library),
            )

    def test_runtime_error(self):
        self.assertRaises(RuntimeError, ctypes.find_library, "not-a-library")


class TestPlatform(unittest.TestCase):

    def test_uname(self):
        self.assertEqual(platform.uname(), platform._uname())

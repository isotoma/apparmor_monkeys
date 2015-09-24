import glob
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from . import ctypes, platform


class TestPthInstallation(unittest.TestCase):

    def setUp(self):
        self.directory = tempfile.mkdtemp(prefix=os.getcwd())
        subprocess.check_call(['virtualenv', '-p', sys.executable, self.directory])
        self.python = os.path.join(self.directory, "bin", "python")

    def pip(self, *command):
        subprocess.check_call([self.python, "-m", "pip", "install"] + list(command))

    def tearDown(self):
        shutil.rmtree(self.directory)

    def test_wheel(self):
        self.pip("wheel")
        subprocess.check_call([self.python, "setup.py", "bdist_wheel", "-d", self.directory])
        self.pip(*glob.glob(os.path.join(self.directory, "*.whl")))
        subprocess.check_call([
            self.python,
            "-c",
            "assert __import__('platform').uname == __import__('apparmor_monkeys').platform.uname",
        ])

    def test_sdist(self):
        subprocess.check_call([self.python, "setup.py", "sdist", "-d", self.directory])
        self.pip(*glob.glob(os.path.join(self.directory, "*.tar.gz")))
        subprocess.check_call([
            self.python,
            "-c",
            "assert __import__('platform').uname == __import__('apparmor_monkeys').platform.uname",
        ])


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

import subprocess
import sys

from log_wtf import main

def test_main():
    subprocess.check_call([sys.executable, main.__file__])

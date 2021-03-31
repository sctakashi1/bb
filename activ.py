import os
import subprocess
import sys
import time

print("Press ENTER for start...")

input()  

while (True):
    process = subprocess.Popen([sys.executable, "main.py"])
    process.wait()
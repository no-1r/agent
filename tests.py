import os
import sys

# Force the correct path for function imports
script_dir = os.path.dirname(os.path.realpath(__file__))  # gets /home/crimson/agent
functions_path = os.path.join(script_dir, "functions")
sys.path.insert(0, functions_path)

from run_python_file import run_python_file

print(run_python_file("calculator", "main.py"))
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py"))
print(run_python_file("calculator", "nonexistent.py"))

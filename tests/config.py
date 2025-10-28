import sys
import os

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "lgsync"))
sys.path.insert(0, lib_path)

print(f"Lib path: {lib_path}")
print(os.path.exists(lib_path))

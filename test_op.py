# test_op.py

from credentials import get_credentials
import os

# 1. Test a standard environment variable (no 'op://')
os.environ["TEST_VAR"] = "hello_world"
print(f"Standard test: {get_credentials('TEST_VAR')}")

# 2. Test a 1Password reference
# Replace this with a real reference from your vault
OP_REF = "op://Employee/APP869/username"
os.environ["OP_TEST_VAR"] = OP_REF

print(f"Attempting to read from 1Password: {OP_REF}...")
secret = get_credentials("OP_TEST_VAR")

if secret:
    print(f"Success! Retrieved: {secret}")
else:
    print("Failed to retrieve secret. Check if 'op' is installed and you are signed in.")

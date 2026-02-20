import os
import subprocess
from dotenv import load_dotenv

# Find the .env file in the same directory as this file
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(env_path)

def get_credentials(var_name):
    """
    Get the value of an environment variable. If the value is a 1Password 
    secret reference (starts with 'op://'), it resolves it using the 1Password CLI.
    """
    value = os.getenv(var_name)
    
    if value and value.startswith("op://"):
        try:
            # Use 1Password CLI to read the secret
            result = subprocess.run(
                ["op", "read", value], 
                capture_output=True, 
                text=True, 
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error reading secret from 1Password for {var_name}: {e.stderr}")
            return None
        except FileNotFoundError:
            print("1Password CLI ('op') not found. Please install it to use secret references.")
            return None
    
    return value

def get_all_credentials(var_names):
    """
    Helper function to get multiple credentials at once.
    """
    return {name: get_credentials(name) for name in var_names}

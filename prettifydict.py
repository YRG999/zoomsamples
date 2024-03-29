import ast
import json

# Prompt for a dictionary or list of dictionaries string
dict_str = input("Enter a Python dictionary or list of dictionaries string:\n")

# Parse the string as a Python dictionary
dict_data = ast.literal_eval(dict_str)

# Convert the dictionary to a prettified JSON string
pretty_json = json.dumps(dict_data, indent=4)

# Print the prettified JSON string
print(pretty_json)

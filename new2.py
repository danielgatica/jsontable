import pandas as pd
import json
import ast

# Step 1: Read the CSV file
df = pd.read_csv('your_file.csv')

# Step 2: Initialize an empty set to collect all unique keys
all_fields = set()

# Step 3: Process each cell in the specification column
for spec_str in df['specification']:
    try:
        # First try to parse as JSON
        try:
            spec_dict = json.loads(spec_str)
        except:
            # If JSON parsing fails, try Python's literal_eval (safer than eval)
            spec_dict = ast.literal_eval(spec_str)
        
        # Get the nested data dictionary
        if 'data' in spec_dict:
            data_dict = spec_dict['data']
            # Add all keys to our set
            all_fields.update(data_dict.keys())
    except Exception as e:
        print(f"Error processing entry: {e}")
        
# Step 4: Convert to sorted list if needed
unique_fields = sorted(list(all_fields))

print(f"Found {len(unique_fields)} unique fields:")
print(unique_fields)
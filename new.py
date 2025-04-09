import json
import pandas as pd
import re
import os

# File paths - replace with your actual file
excel_file = 'your_appliance_data.xlsx'  # Input Excel file
output_file = 'unique_json_fields.xlsx'  # Output Excel file
sheet_name = 'Sheet1'                    # Sheet containing your data
column_name = 'specification'            # Column containing the JSON strings

# Function to clean up and extract JSON data from Excel cell content
def extract_json_from_text(text):
    if not isinstance(text, str):
        return {}
    
    # Handle Python literals in the JSON string
    try:
        json_str = text.replace("'", '"').replace('None', 'null').replace('True', 'true').replace('False', 'false')
        return json.loads(json_str)
    except:
        try:
            # Try to extract with regex if first method fails
            match = re.search(r'(\{.*\})', text)
            if match:
                json_str = match.group(1).replace("'", '"').replace('None', 'null').replace('True', 'true').replace('False', 'false')
                return json.loads(json_str)
        except:
            pass
    return {}

# Function to recursively extract all keys from nested JSON
def extract_all_keys(json_obj, prefix='', keys=None):
    if keys is None:
        keys = set()
    
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            new_key = f"{prefix}.{k}" if prefix else k
            keys.add(new_key)
            if isinstance(v, (dict, list)):
                extract_all_keys(v, new_key, keys)
    elif isinstance(json_obj, list):
        for item in json_obj:
            extract_all_keys(item, prefix, keys)
    
    return keys

# Main execution block
try:
    # Load the Excel file
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    print(f"Loaded {len(df)} rows from {excel_file}")
    
    # Extract unique keys from all JSON in the column
    all_unique_keys = set()
    error_count = 0
    
    for idx, json_str in enumerate(df[column_name].dropna()):
        try:
            json_data = extract_json_from_text(json_str)
            keys = extract_all_keys(json_data)
            all_unique_keys.update(keys)
        except Exception as e:
            error_count += 1
            if error_count <= 3:  # Limit error reporting to avoid excessive output
                print(f"Error processing row {idx}: {str(e)[:100]}...")
    
    # Sort keys and remove 'data.' prefix if desired
    sorted_keys = sorted(all_unique_keys)
    # Uncomment next line to remove 'data.' prefix from all keys
    # sorted_keys = [k.replace('data.', '') if k.startswith('data.') else k for k in sorted_keys]
    
    # Save results to Excel
    result_df = pd.DataFrame(sorted_keys, columns=['Field_Names'])
    result_df.to_excel(output_file, index=False)
    
    print(f"Found {len(sorted_keys)} unique keys")
    print(f"Processed {len(df[column_name].dropna())} rows with {error_count} errors")
    print(f"Results saved to {output_file}")
    
    # Display first 10 keys as a sample
    print("\nSample of field names found:")
    for key in sorted(sorted_keys)[:10]:
        print(f"  - {key}")
        
except Exception as e:
    print(f"Error: {e}")
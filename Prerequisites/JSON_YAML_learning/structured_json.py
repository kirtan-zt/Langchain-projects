# Convert an unstructured paragraph into a JSON schema manually.

import json

def text_to_json(paragraph_text, output_json):
    """
    Manually defines a Python dictionary that acts as a JSON schema 
    based on the content of an unstructured text and converts it to a JSON string.

    Args:
        paragraph_text (str): The original unstructured text (for reference).

    Returns:
        str: A formatted JSON string representing the defined schema.
    """

    data={}
    with open(paragraph_text, 'r') as file:
        for line in file:
            if ':' in line:
                key, value = line.strip().split(':', 1)
                data[key.strip()] = value.strip()
            else:
                continue
            key, value=line.strip().split(':')
            data[key]=value
    
    with open(output_json, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        print(f"Successfully wrote JSON to {output_json}")

if __name__=='__main__':
    text_to_json('unstructured_paragraph.txt', 'output.json')
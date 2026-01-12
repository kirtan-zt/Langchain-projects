import json

def check_json_structure(json_string):
    """Check JSON syntax of key-value pairs"""
    try:
        json.loads(json_string)
        return True, "Valid JSON syntax"
    except json.JSONDecodeError as e:
        return False, f"Invalid syntax: {e}"
    
print(check_json_structure('{"key": "value", "number": 123}')) 
print(check_json_structure("{'bad': 'quotes'}")) 
print(check_json_structure('invalid text')) 
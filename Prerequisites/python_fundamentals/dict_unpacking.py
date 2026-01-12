# Task: Parse a JSON file and extract specific values.

json_data={"widget": {
    "debug": "on",
    "window": {
        "title": "Sample Konfabulator Widget",
        "name": "main_window",
        "width": 500,
        "height": 500
    },
    "image": { 
        "src": "Images/Sun.png",
        "name": "sun1",
        "hOffset": 250,
        "vOffset": 250,
        "alignment": "center"
    },
    "text": {
        "data": "Click Here",
        "size": 36,
        "style": "bold",
        "name": "text1",
        "hOffset": 250,
        "vOffset": 100,
        "alignment": "center",
        "onMouseUp": "sun1.opacity = (sun1.opacity / 100) * 90;"
    }
}}    

# JSON essentials: Reading data from JSON 
print(f"Name of title of Widget inside window is {json_data["widget"]["window"]["title"]}")
print(f"Style of text in widget is {json_data["widget"]["text"]["style"]}")

# Editing data from JSON
json_data["widget"]["image"]["src"]="Images/Moon.png"
print(f"Image name changed to {json_data['widget']['image']['src']} ")

# JSON Validation
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
# Reading the contents of YAML file

import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

if __name__=='__main__':
    file_name = 'demo.yaml'
    with open(file_name, 'r') as stream:
        dictionary = yaml.load(stream, Loader=Loader) # yaml.load converts yaml to python objects.
        print("---Reading contents from YAML file---")
    for key, value in dictionary.items():
        print(key + ":" + str(value))

# Producing a YAML file from Python object.
data = {
    'name': 'Alice',
    'age': 30,
    'city': 'New York',
    'skills': ['Python', 'Data Analysis', 'Machine Learning'],
    'education': {
        'degree': "Master's",
        'field': 'Computer Science',
        'year': 2021
    }
}

with open('output_data.yaml', 'w') as file:
    yaml.dump(data, file) # Saving the contents in 'output_data.yaml' file
    print("\n")
    print("---Producing a new YAML file from dictionary---")
    print(yaml.dump(data)) 
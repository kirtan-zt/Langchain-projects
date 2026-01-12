# Convert plain text into structured Python dictionaries.

demo_dict={}

with open('data.txt', 'r') as data:
    for line in data:
        try:
            key, value=line.strip().split(':', 1)
            demo_dict[key]=value
        except ValueError:
            continue

print(demo_dict)

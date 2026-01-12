# Create a small script that reads a text file and sends its content as a prompt template.


with open('script.txt', 'r') as script:
    script_content=script.read()
    print("Prompt Template Start from the text file")
    print(script_content)
    
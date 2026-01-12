# Calculate tokens of a sample input using a tokenizer tool.

from transformers import AutoTokenizer

sample_text="""The sun dipped below the horizon, casting a warm golden glow over the tranquil lake.
 In that moment, time seemed to stand still, inviting anyone who witnessed it to pause and appreciate the beauty of nature.
"""

model_name="bert-base-uncased"

tokenizer=AutoTokenizer.from_pretrained(model_name)

tokens=tokenizer.encode(sample_text, add_special_tokens=True)
token_count=len(tokens)

print(f"The sample text is {sample_text}")
print(f"The token count for model {model_name} is: {token_count}")
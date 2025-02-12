from deliverable2 import *
validator = URLValidator()

# Define user prompt and URL
user_prompt = "What mods should i use on volt prime"
url_to_check = "https://overframe.gg/items/arsenal/61/volt-prime/"

# Run the validation
result = validator.rate_url_validity(user_prompt, url_to_check)

# Print the results
import json
print(json.dumps(result, indent=2))
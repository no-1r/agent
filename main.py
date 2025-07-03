import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")



client = genai.Client(api_key=api_key)


if len(sys.argv) < 2:
    print("Error: prompt required")
    sys.exit(1)

verbose = "--verbose" in sys.argv[1:]
prompt_args = [arg for arg in sys.argv[1:] if arg != '--verbose']
user_prompt = prompt_args[0] 
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
response = client.models.generate_content(model="gemini-2.0-flash-001",contents=messages,)
prompt_token = response.usage_metadata.prompt_token_count
response_token = response.usage_metadata.candidates_token_count

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_token}")
    print(f"Response tokens: {response_token}")

print(response.text)
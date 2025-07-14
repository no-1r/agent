import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.write_file import write_file, schema_write_file
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.call_function import call_function  # This must be your fixed version

# Load API key from .env
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment.")
    sys.exit(1)

genai.configure(api_key=api_key)

# System instructions to the model
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Tool declaration
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

# Generation tuning (optional)
generation_config = types.GenerationConfig(
    temperature=0.7,
    top_p=1
)

# Get user prompt
if len(sys.argv) < 2:
    print("Usage: python main.py \"<your prompt>\" [--verbose]")
    sys.exit(1)

verbose = "--verbose" in sys.argv
prompt_text = " ".join(arg for arg in sys.argv[1:] if arg != "--verbose")

# Set up the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    tools=[available_functions],
    system_instruction=system_prompt,
    generation_config=generation_config
)

# Generate response
response = model.generate_content([
    {"role": "user", "parts": [{"text": prompt_text}]}
])
model_reply = response.candidates[0].content.parts[0].text
messages=[]
messages.append({
    "role": "model", 
    "parts": [{"text": model_reply}]
})
print(response, messages)
# Parse model output
function_calls = response.candidates[0].content.parts

for part in function_calls:
    if hasattr(part, "function_call"):
        fn = part.function_call

        # Call function dynamically
        function_result_part = call_function(fn, verbose=verbose)
        response_data = function_result_part.get("function_response", {}).get("response")

        if not response_data:
            raise RuntimeError("Invalid function result: missing function_response")

        if verbose:
            print(f"-> {response_data}")
        break
else:
    # If no function call, just print the text
    print(response.text)

# Optional verbose token count
if verbose and hasattr(response, "usage_metadata"):
    usage = response.usage_metadata
    print(f"\nPrompt tokens: {usage.prompt_token_count}")
    print(f"Response tokens: {usage.candidates_token_count}")

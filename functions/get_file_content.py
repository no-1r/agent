import os

def get_file_content(working_directory, file_path):
    acc_path = os.path.abspath(os.path.join(working_directory, file_path))
    wrkdir = os.path.abspath(working_directory)
    print(f"DEBUG: Reading file at {acc_path}")

    if not (acc_path == wrkdir or acc_path.startswith(wrkdir + os.sep)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(acc_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    MAX_CHARS = 10000

    try:
        with open(acc_path, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
            if len(file_content_string) > MAX_CHARS:
                return file_content_string[:MAX_CHARS] + f'\n\n[...File "{file_path}" truncated at 10000 characters]'
            else:
                return file_content_string
    except Exception as e:
        return f'Error: {e}'

from google.generativeai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a file, constrained to the working directory.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative path to the file you want to read.",
            }
        },
        "required": ["path"]
    }
)
import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Ensure file is inside working_directory
    if not abs_file_path.startswith(abs_working_dir + os.sep) and abs_file_path != abs_working_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        # Ensure the parent directory exists
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        # Write to the file
        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'

from google.generativeai import types
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file. Overwrites if the file already exists.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative path where the file will be written.",
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file.",
            }
        },
        "required": ["path", "content"]
    }
)

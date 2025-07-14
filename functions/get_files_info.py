# functions/get_files_info.py

import os
from google.generativeai import types

def get_files_info(working_directory, directory=None):
    target = directory or "."
    abs_dir = os.path.abspath(os.path.join(working_directory, target))
    abs_working = os.path.abspath(working_directory)

    if not abs_dir.startswith(abs_working):
        return f'Error: Cannot list "{target}" – outside the permitted working directory.'
    if not os.path.isdir(abs_dir):
        return f'Error: "{target}" is not a directory.'

    entries = []
    try:
        for fname in os.listdir(abs_dir):
            full = os.path.join(abs_dir, fname)
            size = os.path.getsize(full)
            is_dir = os.path.isdir(full)
            entries.append(f'- {fname}: file_size={size} bytes, is_dir={is_dir}')
        return "\n".join(entries) or "(no files)"
    except Exception as exc:
        return f'Error: {exc}'


from google.generativeai import types

# 
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="List files in a directory (with file size and directory flag), constrained to the working directory.",
    parameters={
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "Relative path from the working directory. Defaults to the working directory if omitted.",
            }
        },
        "required": []
    }
)

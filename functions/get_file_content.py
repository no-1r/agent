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
                truncated_content = file_content_string[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'
                return truncated_content
            else:
                return file_content_string
    except Exception as e:
        return f'Error: {e}'
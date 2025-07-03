import os

def get_files_info(working_directory, directory=None):
    abs_dir = os.path.abspath(os.path.join(working_directory, directory))
    abs_working = os.path.abspath(working_directory)
    if not abs_dir.startswith(abs_working):
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    elif not os.path.isdir(abs_dir):
        return (f'Error: "{directory}" is not a directory')
    
    f = []
    try:
        for file in os.listdir(abs_dir): 
            full_path = os.path.join(abs_dir,file)
            size = os.path.getsize(full_path)
            name = os.path.basename(full_path)
            dirb = os.path.isdir(full_path)
            f.append(f'- {name}: file_size={size} bytes, is_dir={dirb}')
        return "\n".join(f)

    except Exception as e:
        return f'Error: {e}'


    
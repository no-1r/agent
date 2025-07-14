import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file_path.startswith(abs_working_dir + os.sep) and abs_file_path != abs_working_dir:
        return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    elif not os.path.isfile(abs_file_path):
        return (f'Error: File "{file_path}" not found.')
    elif not file_path.lower().endswith(".py"):
        return (f'Error: "{file_path}" is not a Python file.')
    else: 
        try: 
            result = subprocess.run(
                ["python3", abs_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
                cwd=abs_working_dir)
            stdout = result.stdout.decode()
            stderr = result.stderr.decode()
            
            if not stdout and not stderr:
                return "No output produced."

            
            output = ""
            if stdout:
                output += f'STDOUT: {stdout}\n'

            if stderr: 
                output += (f'STDERR: {stderr}')
            
            if result.returncode != 0: 
                output += f"Process exited with code {result.returncode}"
            
            return output.strip()
        
        except Exception as e:
            return f"Error: executing Python file: {e}"
    
from google.generativeai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python script and returns the output or any errors.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative path to the Python file to execute.",
            }
        },
        "required": ["path"]
    }
)

import os
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    if function_call_part.args is not None:
        function_args = dict(function_call_part.args)
    else:
        function_args = {}
 
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # Normalize key names
    function_args["working_directory"] = "./calculator"
    if "path" in function_args:
        function_args["file_path"] = function_args.pop("path")

    # Function lookup table
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    func = function_map.get(function_name)
    if not func:
        return {
            "function_response": {
                "name": function_name,
                "response": {"error": f"Unknown function: {function_name}"},
            }
        }

    try:
        result = func(**function_args)
        return {
            "function_response": {
                "name": function_name,
                "response": {"result": result},
            }
        }
    except Exception as e:
        return {
            "function_response": {
                "name": function_name,
                "response": {"error": str(e)},
            }
        }

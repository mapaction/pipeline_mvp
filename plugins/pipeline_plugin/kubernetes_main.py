import os
import json
import importlib


if __name__ == '__main__':
    function_arguments = json.loads(os.getenv("FUNCTION_ARGUMENTS"))

    # Dynamic module load
    function_module = os.getenv("FUNCTION_MODULE")
    function_name = os.getenv("FUNCTION_NAME")

    module = importlib.import_module(function_module)
    function = getattr(module, function_name)

    # Call function
    function(**function_arguments)

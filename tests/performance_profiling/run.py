import os
import importlib.util
import inspect

def run_all_functions_in_directory():
    # Get the current directory where this script is located
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Iterate through all files in the current directory
    for filename in os.listdir(current_directory):
        if filename.endswith(".py") and filename != os.path.basename(__file__):  # Ignore this script itself
            filepath = os.path.join(current_directory, filename)
            module_name = filename[:-3]  # Remove the .py extension

            # Dynamically import the module
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Get all functions defined in the module
            functions = inspect.getmembers(module, inspect.isfunction)

            # Run each function
            for function_name, function in functions:
                print(f"Running function: {function_name} from {filename}")
                try:
                    result = function()  # Call the function
                    print(f"Result of {function_name}: {result}")
                except Exception as e:
                    print(f"Error running {function_name}: {e}")

# Run the functions
if __name__ == "__main__":
    run_all_functions_in_directory()

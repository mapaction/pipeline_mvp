import inspect


def get_function_information(function, base_folder=None, **kwargs):
    if base_folder is None:
        base_folder = "pipeline_plugin/"
    absolute_path = inspect.getfile(function)
    base_path = absolute_path.split(base_folder)[-1]
    import_location = base_path[:-3].replace("/", ".")
    name = function.__name__
    return name, import_location

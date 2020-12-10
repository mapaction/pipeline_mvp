import inspect


def get_function_information(function):
    absolute_path = inspect.getfile(function)
    base_path = absolute_path.split('pipeline_plugin/')[-1]
    import_location = base_path[:-3].replace('/', '.')
    name = function.__name__
    return name, import_location


def testje():
    print("TEST")


print(get_function_information(testje))
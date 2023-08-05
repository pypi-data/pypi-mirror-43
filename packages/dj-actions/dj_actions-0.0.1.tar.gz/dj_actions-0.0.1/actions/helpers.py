import importlib, yaml

def get_action_map(paths_to_maps):
    action_map = {}
    for path in paths_to_maps:
        action_map.update(yaml.load(open(path, 'r')))
    return action_map

def get_object_from_path(path):
    bits = path.split('.')
    class_name = bits.pop()
    module_string = (".").join(bits)
    mod = importlib.import_module(module_string)
    return getattr(mod, class_name)

def serialize_object(obj, serializer_path):
    serializer = get_object_from_path(serializer_path)
    return serializer(obj).data

def get_path(obj, string, default = None):
    """
    Given a obj and a dotted string, return the value at that location
    return `default` if not found

    Example:
    ```
    d = {"foo": {"bar": "baz" } }
    get_path(d, "foo.bar")
    >> "baz"
    ```
    """
    bits = string.split(".")
    for bit in bits:
        if obj is None: return default
        is_dictionary = isinstance(obj, dict)
        if is_dictionary:
            obj = obj.get(bit)
        else:
            obj = getattr(obj, bit)
    return obj

def map_payload(mapper, dictionary):
    mapped_payload = {}
    for task_arg_name, payload_keypath in mapper.items():
        mapped_payload[task_arg_name] = get_path(
            dictionary,
            payload_keypath
        )
    return mapped_payload

def SerializableClass(object_type: type):
    serializable_types[object_type.__name__] = object_type
    return object_type


serializable_types = {}

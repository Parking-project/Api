def create_dict(dict1, dict2):
    if dict1 is None and dict2 is None:
        return {}
    if dict1 is None:
        return {**(dict2.__dict__)}
    if dict2 is None:
        return {**(dict1.__dict__)}
    
    return {**(dict1.__dict__), **(dict2.__dict__)}
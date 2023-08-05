class Wrapper:

    def __init__(self, name, alt_names):
        self.name = name
        self.alt_names = alt_names


class WrapperSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(WrapperSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

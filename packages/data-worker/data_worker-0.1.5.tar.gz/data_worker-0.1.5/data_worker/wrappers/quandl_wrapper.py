from data_worker.wrappers.wrapper import Wrapper, WrapperSingleton


class QuandlWrapper(Wrapper, metaclass=WrapperSingleton):

    def __init__(self, name, alt_names, api_meta_data):
        super().__init__(name, alt_names)

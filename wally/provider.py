import typing

class BaseProvider(object):

    def __init__(self):
        pass

    def save_state(self):
        raise NotImplementedError("Providers must implement save state")

    def restore_state(self):
        raise NotImplementedError("Providers must implement restore state")


class Provider(object):

    providers = {} 

    def __init__(self):
        raise Exception("Not allowed to create instance of Provider")

    @staticmethod
    def register(cls):
        Provider.providers[cls.__name__.lower()] = cls
        return cls

    @staticmethod
    def resolve(ident):
        return Provider.providers.get(ident, None)
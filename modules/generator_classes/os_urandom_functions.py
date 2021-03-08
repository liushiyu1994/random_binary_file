from ..packages import os


class CurrentGenerator(object):
    """
    This is much faster, enough for medium use. Detailed efficiency varies from platform.
    """

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def random_binary_stream(binary_length):
        return bytearray(os.urandom(binary_length))

from ..packages import random


class CurrentGenerator(object):
    """
    This is the basic intuitive one that is very slow. The bottleneck is b"".join() function.
    """
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def random_binary_stream(binary_length):
        randint_array = [random.randint(0, 255) for _ in range(binary_length)]
        random_binary_list = map(lambda x: chr(x).encode('utf-8'), randint_array)
        return b"".join(random_binary_list)

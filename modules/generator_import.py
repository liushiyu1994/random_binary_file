from .packages import os, Cipher, algorithms, modes
from .default_config import generator_name_list


def generator_import(generator_name, current_file_size, seed_length=None):
    if generator_name == "basic_randint":
        from .generator_classes.basic_randint_functions import CurrentGenerator
        generator = CurrentGenerator()
    elif generator_name == "bytearray_getrandbits":
        from .generator_classes.bytearray_and_getrandbits_functions import CurrentGenerator
        generator = CurrentGenerator()
    elif generator_name == "map_getrandbits":
        from .generator_classes.map_and_getrandbits_functions import CurrentGenerator
        generator = CurrentGenerator()
    elif generator_name == "os_urandom":
        if os is None:
            raise ValueError("'os_urandom' algorithm must rely on os module in python!")
        from .generator_classes.os_urandom_functions import CurrentGenerator
        generator = CurrentGenerator()
    elif generator_name == "itertools_and_struct":
        from .generator_classes.itertools_and_struct_functions import CurrentGenerator
        generator = CurrentGenerator()
    elif generator_name == "itertools_optimized":
        from .generator_classes.itertools_and_struct_optimized_functions import CurrentGenerator
        generator = CurrentGenerator()
    elif generator_name == "python_native_crypto":
        from .generator_classes.python_native_crypto_functions import CurrentGenerator
        if seed_length is None:
            raise ValueError("Seed length must be assigned for 'python_native_crypto' algorithm")
        generator = CurrentGenerator(seed_length)
    elif generator_name == "cryptography_package":
        error_string = "'cryptography_package' algorithm must rely on cryptography module in python!\n" \
                       "cryptography.hazmat.primitives.ciphers.{} cannot be found!"
        if Cipher is None:
            raise ValueError(error_string.format('Cipher'))
        elif algorithms is None:
            raise ValueError(error_string.format('algorithms'))
        elif modes is None:
            raise ValueError(error_string.format('modes'))
        from .generator_classes.cryptography_package_functions import CurrentGenerator
        if seed_length is None:
            raise ValueError("Seed length must be assigned for 'cryptography_package' algorithm")
        generator = CurrentGenerator(seed_length, current_file_size)
    else:
        raise ValueError(
            "Cannot detect generator: {}\nGenerator should be among the following list:\n{}".format(
                generator_name, generator_name_list))
    return generator

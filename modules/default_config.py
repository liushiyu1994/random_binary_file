# Store default parameters in config

current_file_num = 1000

current_file_size = int(25 * 10 ** 6)

current_file_name_length = 24

current_output_folder = "output_folder"

benchmark_output_folder = "benchmark_output_folder"

generator_name = "cryptography_package"

parallel = False

generator_name_list = [
    "basic_randint", "bytearray_getrandbits", "map_getrandbits", "os_urandom",
    "itertools_and_struct", "itertools_optimized", "python_native_crypto", "cryptography_package"]

parallel_num = 4

seed_length = 32

parallel_file_name_prefix_length = 6


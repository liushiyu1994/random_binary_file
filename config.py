######################### Common settings ################################

# Number of files that need to generate.
current_file_num = 200

# Size of each file. Only the 'current_file_size' will be read, and its unit is byte.
current_file_size_mib = 25  # Size unit is MiB
current_file_size_unit = int(10 ** 6)
current_file_size = int(current_file_size_mib * current_file_size_unit)

# Length of random file name. Uppercase character and digit will be used for file name.
current_file_name_length = 24

# Location of output files.
current_output_folder = "output_folder"

# Location of benchmark results.
benchmark_output_folder = "benchmark_output_folder"

# Method that used to generate random binary files.
generator_name = "cryptography_package"

# If any parallel method is utilized.
parallel = False

######################### Common settings ################################


######################### Uncommon settings ################################

# List of all possible methods
generator_name_list = [
    "basic_randint", "bytearray_getrandbits", "map_getrandbits", "os_urandom",
    "itertools_and_struct", "itertools_optimized", "python_native_crypto", "cryptography_package"]

# Number of parallel processes.
parallel_num = 4

# Length of seed for crypto methods.
seed_length = 32

parallel_file_name_prefix_length = 6

######################### Uncommon settings ################################

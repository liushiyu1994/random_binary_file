from .packages import os, random, string, mp, time, math
from .generator_import import generator_import
from . import default_config


def time_stamp():
    return time.strftime("%H:%M:%S")


def random_byte_seed_generator(length):
    if os is not None:
        return os.urandom(length)
    else:
        return bytearray(map(random.getrandbits, (8,)*length))


def random_file_name_iter_generator(file_name_length):
    file_name_char_list = string.ascii_uppercase + string.digits
    file_name_set = set()
    while True:
        new_file_name = ''.join(random.choices(file_name_char_list, k=file_name_length))
        if new_file_name in file_name_set:
            continue
        file_name_set.add(new_file_name)
        yield new_file_name


def random_binary_files_single(
        generator_name, file_num, file_size, file_name_length, output_folder,
        file_name_prefix='', seed_length=None, print_func=None):
    generator_obj = generator_import(generator_name, file_size, seed_length)
    random_file_name_iter = random_file_name_iter_generator(file_name_length)
    file_count = 0
    report_time = 5
    report_list = [True] * report_time
    t_start = time.time()
    while file_count < file_num:
        new_file_name = next(random_file_name_iter)
        new_file_path = "{}/{}{}".format(output_folder, file_name_prefix, new_file_name)
        with open(new_file_path, 'wb') as f_out:
            new_file_content = generator_obj.random_binary_stream(file_size)
            f_out.write(new_file_content)
        file_count += 1
        if print_func is not None:
            report_index = math.floor(file_count / file_num * report_time - 1)
            if report_index >= 0 and report_list[report_index]:
                report_list[report_index] = False
                print_func(file_count)
    t_end = time.time()
    return t_end - t_start


def random_binary_files_parallel(
        generator_name, file_num, file_size, file_name_length, output_folder,
        parallel_num, parallel_file_name_prefix_length, seed_length=None):
    random_file_name_prefix_iter = random_file_name_iter_generator(parallel_file_name_prefix_length)
    process_list = []
    average_file_num = file_num // parallel_num
    rest_file_num = file_num % parallel_num
    t_start = time.time()
    for index in parallel_num:
        random_file_name_prefix = next(random_file_name_prefix_iter)
        current_file_num = average_file_num + 1 if index < rest_file_num else average_file_num
        p = mp.Process(
            target=random_binary_files_single,
            args=(
                generator_name, current_file_num, file_size, file_name_length, output_folder,
                random_file_name_prefix, seed_length))
        process_list.append(p)
        p.start()
    for process in process_list:
        process.join()
    t_end = time.time()
    return t_end - t_start


def parameter_check_function(config):
    error_string = "config.py must include following attributes: {}"
    try:
        generator_name = config.generator_name
    except AttributeError:
        raise ValueError(error_string.format("generator_name"))
    try:
        current_file_num = config.current_file_num
    except AttributeError:
        raise ValueError(error_string.format("current_file_num"))
    try:
        current_file_size = config.current_file_size
    except AttributeError:
        raise ValueError(error_string.format("current_file_size"))
    try:
        current_file_name_length = config.current_file_name_length
    except AttributeError:
        raise ValueError(error_string.format("current_file_name_length"))
    try:
        current_output_folder = config.current_output_folder
    except AttributeError:
        raise ValueError(error_string.format("current_output_folder"))
    if os is not None and not os.path.isdir(current_output_folder):
        raise ValueError("Cannot find output folder: {}".format(current_output_folder))
    try:
        with open("{}/test.txt".format(current_output_folder), 'w') as f_out:
            f_out.write("This is just a test for the output folder")
    except Exception:
        raise ValueError("Cannot write file to folder: {}".format(current_output_folder))
    try:
        seed_length = config.seed_length
    except AttributeError:
        seed_length = default_config.seed_length
    try:
        parallel = config.parallel
    except AttributeError:
        parallel = False
    if parallel:
        try:
            parallel_num = config.parallel_num
        except AttributeError:
            parallel_num = default_config.parallel_num
        try:
            parallel_file_name_prefix_length = config.parallel_file_name_prefix_length
        except AttributeError:
            parallel_file_name_prefix_length = default_config.parallel_file_name_prefix_length
    else:
        parallel_num = None
        parallel_file_name_prefix_length = None
    return (
        generator_name, current_file_num, current_file_size, current_file_name_length, current_output_folder,
        seed_length, parallel, parallel_num, parallel_file_name_prefix_length)


def entry_function(config):
    (
        generator_name, current_file_num, current_file_size, current_file_name_length, current_output_folder,
        seed_length, parallel, parallel_num, parallel_file_name_prefix_length) = parameter_check_function(config)
    if not parallel:
        random_binary_files_single(
            generator_name, current_file_num, current_file_size, current_file_name_length,
            current_output_folder, seed_length=seed_length)
    else:
        random_binary_files_parallel(
            generator_name, current_file_num, current_file_size, current_file_name_length,
            current_output_folder, parallel_num, parallel_file_name_prefix_length, seed_length=seed_length)

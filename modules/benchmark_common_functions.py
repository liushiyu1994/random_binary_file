from .packages import os, plt
from .common_functions import parameter_check_function, random_binary_files_single, time_stamp


def benchmark_text_output(result_sorted_list, output_file_name, output_folder_name):
    headline = "Generator name,\t\t Running time,\t\t File count rate (count/s),\t\t File size rate (MiB/s)"
    text_output_line_list = [headline]
    for generator_name, current_time, file_num_rate, file_size_rate in result_sorted_list:
        newline = "{},\t\t {},\t\t {},\t\t {}".format(generator_name, current_time, file_num_rate, file_size_rate)
        text_output_line_list.append(newline)
    output_file_path = "{}/{}".format(output_folder_name, output_file_name)
    with open(output_file_path, 'w') as f_out:
        f_out.write("\n".join(text_output_line_list))


def benchmark_plotting(result_sorted_list, output_figure_name, output_folder_name):
    x_loc_left_offset = 0.5
    width = 0.5
    x_loc_list = []
    x_label_list = []
    data_list = []
    for index, (generator_name, _, _, file_size_rate) in enumerate(result_sorted_list):
        x_loc_list.append(x_loc_left_offset + index)
        x_label_list.append(generator_name)
        data_list.append(file_size_rate)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.bar(x_loc_list, data_list, width)
    ax.set_xlim([0, len(result_sorted_list) + x_loc_left_offset])
    ax.set_ylabel('File size rate (MiB/s)')
    ax.set_xticks(x_loc_list)
    ax.set_xticklabels(x_label_list, rotation=15)
    save_path = "{}/{}".format(output_folder_name, output_figure_name)
    fig.savefig(save_path, dpi=fig.dpi)


def benchmark_parameter_check_function(config):
    error_string = "config.py must include following attributes for benchmark: {}"
    try:
        generator_name_set = config.generator_name_list
    except AttributeError:
        raise ValueError(error_string.format("generator_name_list"))
    try:
        benchmark_output_folder = config.benchmark_output_folder
    except AttributeError:
        raise ValueError(error_string.format("benchmark_output_folder"))
    if os is not None and not os.path.isdir(benchmark_output_folder):
        raise ValueError("Cannot find benchmark output folder: {}".format(benchmark_output_folder))
    try:
        with open("{}/test.txt".format(benchmark_output_folder), 'w') as f_out:
            f_out.write("This is just a test for the benchmark output folder")
    except Exception:
        raise ValueError("Cannot write file to folder: {}".format(benchmark_output_folder))
    return generator_name_set, benchmark_output_folder


def make_son_folder(parent_folder_path, target_son_folder_name):
    target_son_folder_path = "{}/{}".format(parent_folder_path, target_son_folder_name)
    if os is not None:
        if not os.path.isdir(target_son_folder_path):
            os.mkdir(target_son_folder_path)
        return target_son_folder_path
    else:
        return parent_folder_path


def benchmark_entry_function(config):
    (
        _, current_file_num, current_file_size, current_file_name_length, current_output_folder,
        seed_length, parallel, parallel_num, parallel_file_name_prefix_length) = parameter_check_function(config)

    def current_print_func(file_count):
        print("[{}] {}({:.2f}%) finished".format(time_stamp(), file_count, file_count / current_file_num * 100))

    generator_name_list, benchmark_output_folder = benchmark_parameter_check_function(config)
    benchmark_file_output_folder = make_son_folder(benchmark_output_folder, "output_files")

    total_file_size = current_file_size * current_file_num
    final_time_list = []
    print("[{}] Start benchmark".format(time_stamp()))
    for generator_name in generator_name_list:
        print("[{}] Start generator: {}".format(time_stamp(), generator_name))
        current_generator_output_folder = make_son_folder(benchmark_file_output_folder, generator_name)
        current_time = random_binary_files_single(
            generator_name, current_file_num, current_file_size, current_file_name_length,
            current_generator_output_folder, seed_length=seed_length, print_func=current_print_func)
        file_num_rate = current_file_num / current_time
        file_size_rate = total_file_size / current_time / 10**6
        final_time_list.append((generator_name, current_time, file_num_rate, file_size_rate))
        print("[{}] Finish generator: {}".format(time_stamp(), generator_name))
    sorted_final_time_list = sorted(final_time_list, key=lambda x: x[3])
    text_output_file_name = "benchmark_result.csv"
    benchmark_text_output(sorted_final_time_list, text_output_file_name, benchmark_file_output_folder)
    if plt is not None:
        figure_name = "benchmark_result.png"
        benchmark_plotting(sorted_final_time_list, figure_name, benchmark_file_output_folder)
        plt.show()

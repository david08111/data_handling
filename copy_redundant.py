import os
import argparse
import shutil

def copy_redundant(base_data_path, copy_data_path, output_data_path):

    # base_data_list = [f.split(".") for f in os.listdir(base_data_path) if os.path.isfile(os.path.join(base_data_path, f))]
    base_data_list = []
    base_data_name_list = []

    copy_data_list = []
    copy_data_name_list = []

    base_data_file_ending = []

    for f in os.listdir(base_data_path):
        if os.path.isfile(os.path.join(base_data_path, f)):
            if not "label" in f:
                base_data_list.append(f)
                base_data_name_list.append(f.split(".")[0])
                base_data_file_ending.append(f.split(".")[1])

    if base_data_file_ending.count(base_data_file_ending[0]) == len(base_data_file_ending):
        src_file_ending = base_data_file_ending[0]
    else:
        raise Exception("Hardcode different file endings copying")

    # copy_data_list = [f for f in os.listdir(copy_data_path) if
    #                   os.path.isfile(os.path.join(copy_data_path, f))]

    copy_data_file_ending = []

    for f in os.listdir(copy_data_path):
        if os.path.isfile(os.path.join(copy_data_path, f)):

            copy_data_list.append(f)
            if not "label" in f:
                copy_data_name_list.append(f.split(".")[0])
            else:
                copy_data_name_list.append(f.split(".")[0] + "." + f.split(".")[1])
            copy_data_file_ending.append(f.split(".")[1])

    if copy_data_file_ending.count(copy_data_file_ending[0]) == len(copy_data_file_ending) or copy_data_file_ending[0] == "jpg" or copy_data_file_ending[0] == "png":
        out_file_ending = copy_data_file_ending[0]
    else:
        raise Exception("Hardcode different file endings copying")

    # intersection_data_list = [file for file in copy_data_name_list if file in base_data_name_list]

    intersection_data_list = []
    for file_cp in copy_data_name_list:
        for file_base in base_data_name_list:
            if file_base in file_cp:
                intersection_data_list.append(file_cp)

    if not os.path.isdir(output_data_path):
        os.makedirs(output_data_path)

    for file in intersection_data_list:
        # file_path_out = os.path.join(output_data_path, file + "." + out_file_ending)
        if "_label" in file:
            file_path_src = os.path.join(copy_data_path, file + "." + "png")
            file_path_out = os.path.join(output_data_path, file + "." + "png")
            shutil.copyfile(file_path_src, file_path_out)
        else:
            file_path_src = os.path.join(copy_data_path, file + "." + out_file_ending)
            file_path_out = os.path.join(output_data_path, file + "." + out_file_ending)
            shutil.copyfile(file_path_src, file_path_out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-bd", "--base_data_path", type=str,
                        help="Filepath to base data")
    parser.add_argument("-cd", "--copy_data_path", type=str,
                        help="Filepath to copied data")
    parser.add_argument("-out", "--output_data_path", type=str,
                        help="Filepath to output folder")
    args = parser.parse_args()

    copy_redundant(args.base_data_path, args.copy_data_path, args.output_data_path)
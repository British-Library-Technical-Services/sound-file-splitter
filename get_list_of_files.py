import glob
import os


def get_file_list_for_processing(file_path: str, file_type: str) -> list[str]:
    files_list = []
    try:
        files_list = sorted(glob.glob(os.path.join(file_path, file_type)))
    except OSError as ose:
        print("Failed to glob %s files in %s - %s" % (file_type, file_path, ose))

    return files_list

from typing import List
import os
import glob


def get_files_to_process(root_directory: str, file_type: str) -> List[str]:
    list_of_files = []
    try:
        list_of_files = glob.glob(os.path.join(root_directory, file_type))
    except OSError as ose:
        raise OSError("Failed to glob files in %s - %s" % (root_directory, ose))

    return list_of_files


def is_audio_file_in_mets(audio_files: List[str], files_in_mets: List[str]) -> bool:
    pass

from typing import List, Dict
import xml.etree.ElementTree as ET
import os
import tkinter as tk
from tkinter import filedialog

from rich import print
from rich.prompt import Prompt
from tqdm import tqdm

from datamodels import SoundFileObject, RecordTitleData, RecordedAreaData
from file_service import get_files_to_process

from xml_parser import (
    extract_root_element_from_file,
    extract_filenames,
    extract_original_file_ids,
    extract_recorded_area_elements,
    extract_struct_link_elements,
    extract_record_titles,
    parse_recorded_area_data,
)

from csv_writer import write_csv_file
from file_splitter import convert_frames_to_ms, timecode_split

from service_messages import (
    welcome_message,
    source_directory_list,
    service_information,
    error_list,
)


def open_filedialog() -> str:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    source_directory: str = None

    try:
        source_directory = filedialog.askdirectory()
    except FileNotFoundError as fnfe:
        print(f"Error selecting directory {fnfe}")

    return source_directory


def parse_mets_xml_file(
    location: str, xml_file: str, namespaces: Dict[str, str]
) -> List[SoundFileObject]:
    try:
        root_element = extract_root_element_from_file(file_to_read=xml_file)
        if root_element is None:
            print(f"{xml_file} returned no root element tree")
            return
    except ET.ParseError as epe:
        print(epe)
    except OSError as ose:
        print(ose)

    files_to_split = extract_filenames(xml_root_tree=root_element, namespace=namespaces)
    if not files_to_split or None in files_to_split or "" in files_to_split:
        print(f"Error extracting file names from {xml_file}")
        return

    """Get list of orignal file ids"""
    file_ids = extract_original_file_ids(
        xml_root_tree=root_element, namespace=namespaces
    )
    if not file_ids or None in file_ids or "" in file_ids:
        print(f"Error extracting file ids from {xml_file}")
        return

    """Get list of recorded area data elements"""
    recorded_area_elements = extract_recorded_area_elements(
        xml_root_tree=root_element, namespace=namespaces
    )
    if not recorded_area_elements or None in recorded_area_elements:
        print(f"Error extracting physical ids from {xml_file}")
        return

    """Get record title and physcial id reference"""
    struct_link_elements = extract_struct_link_elements(
        xml_root_tree=root_element, namespace=namespaces
    )
    if not struct_link_elements or None in struct_link_elements:
        print(f"Error extracting struct_link data from {xml_file}")
        return

    record_title_objects = [
        extract_record_titles(element=struct_links, namespace=namespaces)
        for struct_links in struct_link_elements
    ]

    if not record_title_objects or None in record_title_objects:
        print("Error parsing record titles from {xml_file}")
        return

    return (
        files_to_split,
        file_ids,
        recorded_area_elements,
        struct_link_elements,
        record_title_objects,
    )


def build_file_and_title_lookups(
    file_list: List[str], file_id_list: List[str], record_titles: RecordTitleData
):
    file_and_id_lookup = dict(zip(file_id_list, file_list))
    if not file_and_id_lookup or None in file_and_id_lookup:
        print("Error parsing file names from {xml_file}")
        return

    title_lookup = {obj.physical_id.strip("#"): obj.title for obj in record_titles}
    if not title_lookup or None in file_and_id_lookup:
        print(f"Error parsing record titles from {xml_file}")
        return

    return file_and_id_lookup, title_lookup


def build_sound_file_object(
    file_and_tc_data: RecordedAreaData,
    file_lookup_table: List[str],
    title_lookup_table: List[str],
) -> SoundFileObject:
    sound_file_object = SoundFileObject(
        filename=file_lookup_table.get(file_and_tc_data.file_id, ""),
        file_id=file_and_tc_data.file_id,
        physical_id=file_and_tc_data.physical_id,
        timecode_in=file_and_tc_data.timecode_in,
        timecode_out=file_and_tc_data.timecode_out,
        record_title=title_lookup_table.get(file_and_tc_data.physical_id, ""),
    )

    return sound_file_object


def is_sound_file_object_valid(object_data: SoundFileObject) -> bool:
    if (
        object_data.filename is None
        or object_data.filename == ""
        or object_data.file_id is None
        or object_data.file_id == ""
        or object_data.physical_id is None
        or object_data.physical_id == ""
        or object_data.timecode_in is None
        or object_data.timecode_in == ""
        or object_data.timecode_out is None
        or object_data.timecode_out == ""
        or object_data.record_title is None
        or object_data.record_title == ""
    ):
        return

    return True


def construct_soundcloud_filename(source_title: str) -> str:
    ## filenaming convention
    ## call number, title
    ## use _ for all separators
    ## e.g. "C540_1_1, title"

    title_edit: List[str] = source_title.split(": ")
    shelf_mark: str = title_edit.pop(1).replace("/", "_").replace(" ", "_")
    title: str = title_edit.pop(-1)

    return f"{shelf_mark}, {title}.mp4"


def invalid_sound_object(errors: List[str]):
    if errors != []:
        print("""
The following files were not processed as the extracted data is does not meet the criteria for splitting: """)
        for error in errors:
            print(error_list(file=error))


def main():
    namespaces = {"mets": "http://www.loc.gov/METS/", "mediaMD": "mediaMDv2.1.xsd"}
    data_errors: List[str] = []

    METS_XML = "*.xml"
    AUDIO_FILE = "*.mp4"

    Prompt.ask(welcome_message())

    location = open_filedialog()
    if not location:
        print("Error opening source directory - exiting service")
        return
    elif location == "":
        print("No directory selected - exiting service")
        return

    # return
    # location = "METS_FILES"
    # location = "with_audio_files"

    try:
        xml_files_to_parse = get_files_to_process(
            root_directory=location, file_type=METS_XML
        )

        if not xml_files_to_parse:
            print(f"No xml files found in {location} - exiting service")
            return

        audio_files_to_split = get_files_to_process(
            root_directory=location, file_type=AUDIO_FILE
        )
        if not audio_files_to_split:
            print(f"No audio access files found in {location} - exiting service")
            return

        Prompt.ask(
            source_directory_list(
                directory=location,
                number_of_xml_files=(len(xml_files_to_parse)),
                number_of_audio_files=(len(audio_files_to_split)),
            )
        )

        audio_filenames = [
            os.path.basename(filename) for filename in audio_files_to_split
        ]

        audio_file_paths = [
            os.path.abspath(file_path) for file_path in audio_files_to_split
        ]

    except OSError as ose:
        print(f"Error accessing files - {ose}")

    # mets and audio file list comparison
    print(service_information())

    for xml_file in tqdm(xml_files_to_parse):
        (
            files_to_split,
            file_ids,
            recorded_area_elements,
            struct_link_elements,
            record_title_objects,
        ) = parse_mets_xml_file(
            location=location, xml_file=xml_file, namespaces=namespaces
        )

        sound_object_edit_list: List[SoundFileObject] = []

        for recorded_area in recorded_area_elements:
            area_data = parse_recorded_area_data(
                element=recorded_area, namespace=namespaces
            )

            file_lookup_table, title_lookup_table = build_file_and_title_lookups(
                file_list=files_to_split,
                file_id_list=file_ids,
                record_titles=record_title_objects,
            )

            sound_object = build_sound_file_object(
                file_and_tc_data=area_data,
                file_lookup_table=file_lookup_table,
                title_lookup_table=title_lookup_table,
            )

            is_valid = is_sound_file_object_valid(object_data=sound_object)
            if not is_valid:
                data_errors.append(xml_file)
                sound_object_edit_list = []
                break

            sound_object_edit_list.append(sound_object)

        if not sound_object_edit_list:
            continue

        write_csv_file(file_to_write=xml_file, data_to_write=sound_object_edit_list)

        for file in sound_object_edit_list:
            access_file = file.filename.replace("wav", "mp4")
            if access_file in audio_filenames:
                file_index = audio_filenames.index(access_file)
                soundcloud_filename = construct_soundcloud_filename(
                    source_title=file.record_title,
                )

                timecode_in_seconds = convert_frames_to_ms(
                    smpte_timecode=file.timecode_in
                )
                timecode_out_in_seconds = convert_frames_to_ms(
                    smpte_timecode=file.timecode_out
                )
                current_path = os.path.dirname(
                    os.path.abspath(audio_files_to_split[file_index])
                )
                output_path = os.path.join(current_path, "_split_files_ranges")

                if not os.path.exists(output_path):
                    os.mkdir(output_path)

                try:
                    timecode_split(
                        input_file=audio_files_to_split[file_index],
                        timecode_in=timecode_in_seconds,
                        timecode_out=timecode_out_in_seconds,
                        output_file=os.path.join(output_path, soundcloud_filename),
                    )
                except OSError as ose:
                    print(f"Error splitting file {ose}")

    invalid_sound_object(errors=data_errors)


if __name__ == "__main__":
    main()
    input()

from typing import List, Dict, Tuple
import get_list_of_files
from mets_xml_parser import XMLTreeParser

# filename
# fileid
# physID -> fileID -> recorded area -> begin --> end
# physID -> cat record title (comment)


def extract_file_splitting_data(ns: Dict[str, str], file_to_read: str):
    xml_data_parse = XMLTreeParser(ns=ns, source_file=file_to_read)
    xml_data_parse.get_xml_root()

    xml_data_parse.get_filenames()
    if xml_data_parse.filenames == []:
        return

    xml_data_parse.get_fileids()
    if xml_data_parse.fileids == []:
        return

    xml_data_parse.get_physids()
    if xml_data_parse.physids == []:
        return

    xml_data_parse.get_record_title()
    if xml_data_parse.record_titles == []:
        return

    return (
        xml_data_parse.filenames,
        xml_data_parse.fileids,
        xml_data_parse.physids,
        xml_data_parse.record_titles,
    )


# def write_timecode_and_title_object_data(filename


def main():
    data_object: Dict[str, str] = {
        "filename": "",
        "fileid": "",
        "physid": "",
        "begin": "",
        "end": "",
        "title": "",
    }
    object_list: List[Dict[str, str]] = []
    filename_and_file_id = []

    location = "./sc_files/C324/"
    namespaces = {"mets": "http://www.loc.gov/METS/", "mediaMD": "mediaMDv2.1.xsd"}

    xml_file_list = get_list_of_files.get_file_list_for_processing(
        file_path=location, file_type="*.xml"
    )
    if xml_file_list == []:
        return

    for xml_file in xml_file_list:
        files_to_split, original_file_ids, phys_structure_data, record_titles = (
            extract_file_splitting_data(ns=namespaces, file_to_read=xml_file)
        )

        for file_id in original_file_ids:
            data_object["fileid"] = file_id

            for data in phys_structure_data:
                phys_id = data[0]
                file_id_check = data[1]
                timecode_in = data[2]
                timecode_out = data[3]

                if file_id_check == data_object["fileid"]:
                    data_object["physid"] = phys_id
                    data_object["begin"] = timecode_in
                    data_object["end"] = timecode_out

                    for title_data in record_titles:
                        phys_id_check = title_data[0]
                        title = title_data[1]

                        if data_object["physid"] == phys_id_check:
                            data_object["title"] = title

                            object_list.append(data_object.copy())
                            break

        for i, file in enumerate(files_to_split):
            filename_and_file_id.append([original_file_ids[i], file])

        for file_object in object_list:
            for data in filename_and_file_id:
                if file_object["fileid"] == data[0]:
                    file_object["filename"] = data[1]

        print(object_list)


if __name__ == "__main__":
    main()

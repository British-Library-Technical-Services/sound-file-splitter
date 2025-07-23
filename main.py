
## filename(s)
# mediaMD:fileData

## File ID
# :fileSec
# |- :fileGrp = "Orignal"
# |___ :file = ID="fileN"

# dm == log
# log == phys
# phys get cuts


import get_list_of_files
from extract_data_from_mets import XMLDataExtrator

unique_file_reference = set()
unique_catalogue_reference = set()

directory = "./sc_files/C325/"
xml_file_glob = "*.xml"
audio_file_glob = "*.mp4"
namespace = {"mets": "http://www.loc.gov/METS/", "mediaMD": "mediaMDv2.1.xsd"}

# object_map = {
#     "filename": None,
#     "file_ref": None,
#     "cat_ref": None,
#     "tc_in": None,
#     "tc_out": None,
#     "title": None,
# }

object_list = []

def main():
    xml_file_list = get_list_of_files.get_file_list_for_processing(
        file_path=directory, file_type=xml_file_glob
    )

    # audio_file_list = get_list_of_files.get_file_list_for_processing(
    #     file_path=directory, file_type=audio_file
    # )
    if xml_file_list == []:
        print(f"{directory} is empty")
        return

    else:
        for xml_file in xml_file_list:
            xml_data_extract = XMLDataExtrator(ns=namespace)
            xml_data_extract.get_root_data(file_to_read=xml_file)

            filenames = xml_data_extract.get_filename()
            if filenames == []:  
                break

            
            file_ids = xml_data_extract.get_file_ids()
            if file_ids == []:
                break


            dmid_record_titles = xml_data_extract.get_dmid_and_record_title()
            if dmid_record_titles == []:
                break

            logid_and_record_titles = xml_data_extract.get_logid_and_record_title()
            if logid_and_record_titles == []:
                break
            
            
            for file in file_ids:
                physid_timecodes = xml_data_extract.get_timecodes(original_file=file)
                if physid_timecodes == []:
                    break
                
                # print(physid_timecodes)


            # print(filenames)
            # print(file_ids)
            # print(logid_and_record_titles)

            object_map = {
                    "filename": "",
                    "file_id": ""
                    }
            object_data = []

            if len(filenames) == len(file_ids):
                for i, file in enumerate(filenames):
                    object_map["filename"] = file
                    object_map["file_id"] = file_ids[i]

                    object_data.append(object_map.copy())

            print(object_data)


            break  
    #                     # object_map["filename"] = xml_data_extract.filename
    #                     # object_map["file_ref"] = xml_data_extract.file_reference
    #                     # object_map["cat_ref"] = xml_data_extract.catalogue_reference
    #                     # object_map["tc_in"] = xml_data_extract.tc_in
    #                     # object_map["tc_out"] = xml_data_extract.tc_out
    #                     # object_map["title"] = xml_data_extract.record_title
    #
    #                     # print(object_map)
    #
    #                     object_list.append(object_map.copy())
    #
    # # print(object_list)


if __name__ == "__main__":
    main()

import os
import xml.etree.ElementTree as et

file_path = "sc_files/C325"
# xml_file = "C0324X10X02X_METS.xml"
xml_file = "BL_C325-1_s1_METS.xml"

## [call_number],[title].mp4


class XMLDataExtrator:

    def get_filename(self, root, ns) -> str:
        filename = root.find(".//mediaMD:fileName", namespaces=ns).text
        return filename

    def get_file_reference(self, area) -> str:
        if not area.attrib.get("TYPE") == "Recorded Area":
            pass
        else:
            file_reference = area.attrib.get("ID")
            return file_reference

    def get_timecode_ranges(self, timecodes) -> str:
        tc_in, tc_out = timecodes.attrib.get("BEGIN"), timecodes.attrib.get("END")
        return (tc_in, tc_out)

    def get_catalogue_title(self, child) -> str:
        if child.tag == et.Comment and child.text.startswith("Parent"):
            record_title = child.text

        sm_link = child.attrib.get("{http://www.w3.org/1999/xlink}href")
        if sm_link != None and sm_link.startswith("#phys"):
            catalogue_reference = sm_link.strip("#")
            return (record_title, catalogue_reference)


def main() -> None:
    parser = et.XMLParser(target=et.TreeBuilder(insert_comments=True))
    data = et.parse(os.path.join(file_path, xml_file), parser=parser)
    root = data.getroot()
    ns = {"mets": "http://www.loc.gov/METS/", "mediaMD": "mediaMDv2.1.xsd"}

    object_map = {
        "file": None,
        "ref": None,
        "tc_in": None,
        "tc_out": None,
        "record_title": None,
    }

    object_data = []
    unique_keys = set()

    extract = XMLDataExtrator()
    filename = extract.get_filename(root, ns)

    object_map["file"] = filename

    recorded_area = root.find(
        ".//mets:structMap[2]/mets:div/mets:div/mets:div[1]", namespaces=ns
    )

    for area in recorded_area:
        file_reference = extract.get_file_reference(area)

        timecodes = area.findall(".//mets:area", namespaces=ns)
        for timecode in timecodes:
            tc_in, tc_out = extract.get_timecode_ranges(timecode)
            if (
                file_reference is not None
                and file_reference not in unique_keys
            ):
                unique_keys.add(object_map["ref"])
                object_map["ref"] = file_reference
                object_map["tc_in"] = tc_in
                object_map["tc_out"] = tc_out

            for link_group in root.findall(".//mets:smLinkGrp", namespaces=ns):
                for child in link_group.iter():
                    catalogue_title, catalogue_reference = extract.get_catalogue_title(child)
                    if (
                        catalogue_reference == object_map["ref"]
                        and catalogue_title not in unique_keys
                    ):
                        unique_keys.add(catalogue_title)
                        object_map["record_title"] = catalogue_title

                        object_data.append(object_map.copy())
    for data in object_data:
        print(data)


if __name__ == "__main__":
    main()

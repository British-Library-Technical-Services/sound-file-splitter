import os
import xml.etree.ElementTree as et

file_path = "sc_files/C325"
# xml_file = "C0324X10X02X_METS.xml"
xml_file = "BL_C325-1_s1_METS.xml"

## [call_number],[title].mp4


class XMLDataExtrator:
    def __init__(self, root, ns):
        self.root = root
        self.ns = ns
        self.filename = None
        self.tc_in = None
        self.tc_out = None
        self.file_reference = None
        self.catalogue_reference = None
        self.record_title = None

    def get_filename(self) -> None:
        self.filename = self.root.find(".//mediaMD:fileName", namespaces=self.ns).text

    def get_file_reference(self, area) -> None:
        if not area.attrib.get("TYPE") == "Recorded Area":
            pass
        else:
            self.file_reference = area.attrib.get("ID")

    def get_timecode_ranges(self, timecodes) -> None:
        self.tc_in, self.tc_out = timecodes.attrib.get("BEGIN"), timecodes.attrib.get(
            "END"
        )

    def get_catalogue_title(self, child) -> None:
        if child.tag == et.Comment and child.text.startswith("Parent"):
            self.record_title = child.text

        sm_link = child.attrib.get("{http://www.w3.org/1999/xlink}href")
        if sm_link != None and sm_link.startswith("#phys"):
            self.catalogue_reference = sm_link.strip("#")


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

    extract = XMLDataExtrator(root, ns)
    extract.get_filename()

    object_map["file"] = extract.filename

    recorded_area = root.find(
        ".//mets:structMap[2]/mets:div/mets:div/mets:div[1]", namespaces=ns
    )

    for area in recorded_area:
        extract.get_file_reference(area)

        timecodes = area.findall(".//mets:area", namespaces=ns)
        for timecode in timecodes:
            extract.get_timecode_ranges(timecode)
            if (
                extract.file_reference is not None
                and extract.file_reference not in unique_keys
            ):
                unique_keys.add(object_map["ref"])
                object_map["ref"] = extract.file_reference
                object_map["tc_in"] = extract.tc_in
                object_map["tc_out"] = extract.tc_out

            for link_group in root.findall(".//mets:smLinkGrp", namespaces=ns):
                for child in link_group.iter():
                    extract.get_catalogue_title(child)
                    if (
                        extract.catalogue_reference == object_map["ref"]
                        and extract.record_title not in unique_keys
                    ):
                        unique_keys.add(extract.record_title)
                        object_map["record_title"] = extract.record_title

                        object_data.append(object_map.copy())
    for data in object_data:
        print(data)

if __name__ == "__main__":
    main()

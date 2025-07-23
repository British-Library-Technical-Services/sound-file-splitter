from typing import Optional, List
import xml.etree.ElementTree as et


# file_path = "sc_files/C325"
# # xml_file = "C0324X10X02X_METS.xml"
# xml_file = "BL_C325-1_s1_METS.xml"

## [call_number],[title].mp4


class XMLDataExtrator:

    def __init__(self, ns):
        self.parser = et.XMLParser(target=et.TreeBuilder(insert_comments=True))
        self.namespace = ns
        self.root = None
        self.recorded_area = None
        self.timecodes = None
        self.link_group = None
        self.file_reference = None
        self.tc_in = None
        self.tc_out = None
        self.record_title = None
        self.catalogue_reference = None

    def get_root_data(self, file_to_read: str) -> None:
        try:
            xml_data = et.parse(file_to_read, parser=self.parser)
            self.root = xml_data.getroot()
            if self.root is None:
                print(f"No root element found in {file_to_read}")
                return
            else:
                self.recorded_area = self.root.find(
                    ".//mets:structMap[2]/mets:div/mets:div/mets:div[1]",
                    namespaces=self.namespace,
                )
                self.link_group = self.root.findall(
                    ".//mets:smLinkGrp", namespaces=self.namespace
                )
        except Exception as e:
            raise e

    def get_filename(self) -> Optional[List[str]]:
        filename: List[str] = []
        try:
            extract_file_name = self.root.findall(
                ".//mediaMD:fileName", namespaces=self.namespace
            )
            if extract_file_name is None:
                print("No filename found")
                return

            filename = [name.text for name in extract_file_name]
            
            return filename

        except Exception as e:
            raise e


    def get_file_ids(self) -> Optional[List[str]]:
        file_ids: List[str] = []

        file_group = self.root.findall(".//mets:fileSec/mets:fileGrp[@USE='Original']//mets:file", namespaces=self.namespace)
        file_ids = [id.attrib.get("ID") for id in file_group]

        return file_ids

    def get_dmid_and_record_title(self) -> List[str]:
        id_and_record_title: List[str] = []
        record_id: str = ""
        record_title: str = ""

        get_dmid = self.root.findall(".//mets:dmdSec", namespaces=self.namespace)
        for dmid in get_dmid:
            record_id = dmid.attrib.get("ID")
            for child in dmid:
                if child.tag is et.Comment and not None:
                    record_title = child.text

            id_and_record_title.append([record_id, record_title]) 
    
        return id_and_record_title

    def get_logid_and_record_title(self) -> List[str]:
        logid_and_record_title: List[str] = []
        logid: str = ""
        record_title: str = ""

        get_logid = self.root.findall(".//mets:structMap[@TYPE='LOGICAL']//mets:div", namespaces=self.namespace)
        for logid in get_logid:
            record_id = logid.attrib.get("ID")
            for child in logid:
                if child.tag is et.Comment and not None:
                    record_title = child.text

            logid_and_record_title.append([record_id, record_title]) 
    
        return logid_and_record_title
    
    def get_timecodes(self, original_file: str) -> List[str]:
        timecodes: List[str] = []
        record_id: str = ""
        fileid: str = ""
        timecode_in: str = ""
        timecode_out: str = ""

        get_recorded_area = self.root.findall(".//mets:structMap[@TYPE='PHYSICAL']//mets:div[@TYPE='Recorded Area']", namespaces=self.namespace)

        for physid in get_recorded_area:
            record_id = physid.attrib.get("ID")
            timecode = physid.findall(".//mets:fptr/mets:area", namespaces=self.namespace)
            
            for item in timecode:
                if item.attrib.get("FILEID") != original_file:
                    pass
                else:
                    fileid = item.attrib.get("FILEID")
                    timecode_in = item.attrib.get("BEGIN")
                    timecode_out = item.attrib.get("END")

                    timecodes.append([fileid, record_id, timecode_in, timecode_out])

        return timecodes



    # def get_timecode_data(self, area: Element):
    #     self.timecodes = area.findall(".//mets:area", namespaces=self.namespace)
    #
    #
    # def get_file_reference(self, area):
    #     if not area.attrib.get("TYPE") == "Recorded Area":
    #         pass
    #     else:
    #         self.file_reference = area.attrib.get("ID")
    #
    # def get_timecode_ranges(self, timecode):
    #     self.tc_in, self.tc_out = timecode.attrib.get("BEGIN"), timecode.attrib.get(
    #         "END"
    #     )
    #
    # def get_catalogue_reference(self, child):
    #     sm_link = child.attrib.get("{http://www.w3.org/1999/xlink}href")
    #     if sm_link != None and sm_link.startswith("#phys"):
    #         self.catalogue_reference = sm_link.strip("#")
    #
    # def get_catalogue_title(self, child):
    #     print(child.text)
    #     if child.tag == et.Comment and child.tag != "Parent":
    #         self.record_title = child.text
    #     else:

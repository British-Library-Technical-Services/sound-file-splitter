from typing import Dict, List
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import (
    ElementTree,
    Element,
)  # import required to define ELementTree and Element as types

# filename, begin, end
# object_map = {filename, fileid, physid, begin, end}
# [filename, fileid]
# x = [fileid, physid, begin, end]
# [record_title, physid]
# for filid in x insert filename
# for physid in x insert record_title
# inset begin, end


class XMLTreeParser:
    def __init__(self, ns: Dict[str, str], source_file: str):
        self.ns: Dict[str, str] = ns
        self.source_file: str = source_file
        self.root: ElementTree = None
        self.filenames: List[str] = []
        self.fileids: List[str] = []
        self.physids: List[str] = []
        self.record_titles: List[str] = []

    def get_xml_root(self):
        read_file: Element = None
        parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
        try:
            read_file = ET.parse(self.source_file, parser=parser)
            self.root = read_file.getroot()
            if self.root is None:
                return
        except Exception as e:
            raise e

    def get_filenames(self):
        filename_elements: List[str] = []
        filename_elements = self.root.findall(".//mediaMD:fileName", self.ns)

        self.filenames = [filename.text for filename in filename_elements]

    def get_fileids(self):
        fileid_elements: List[str] = []
        fileid_elements = self.root.findall(
            ".//mets:fileSec/mets:fileGrp[@USE='Original']//mets:file", self.ns
        )
        self.fileids = [id.attrib.get("ID") for id in fileid_elements]

    def get_physids(self):
        phys_elements: Element = None
        phys_elements = self.root.findall(
            ".//mets:structMap/[@TYPE='PHYSICAL']//mets:div[@TYPE='Recorded Area']",
            self.ns,
        )

        for element in phys_elements:
            phys_ids = element.attrib.get("ID")
            recorded_area = element.find(
                "./mets:fptr/mets:area", self.ns
            )  # use .find to return the first element in mets:area (i.e. 'Orignal' file)
            fileid = recorded_area.attrib.get("FILEID")
            timecode_in = recorded_area.attrib.get("BEGIN")
            timecode_out = recorded_area.attrib.get("END")
            self.physids.append([phys_ids, fileid, timecode_in, timecode_out])

    def get_record_title(self):
        struct_link = self.root.findall(".//mets:structLink//mets:smLinkGrp", self.ns)

        for link in struct_link:
            for child in link:
                if child.tag is ET.Comment:
                    title = child.text
                elif child.tag == "{http://www.loc.gov/METS/}smLocatorLink":
                    smLocator = child.attrib.get("{http://www.w3.org/1999/xlink}href")
                    if smLocator.startswith("#phys"):
                        physid = smLocator.strip("#")

                        self.record_titles.append([physid, title])

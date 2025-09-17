from typing import Dict, List
import xml.etree.ElementTree as ET

from datamodels import RecordedAreaData, RecordTitleData
from xml.etree.ElementTree import (
    ElementTree,
    Element,
)  # import required to define ELementTree and Element as types


def extract_root_element_from_file(file_to_read: str) -> Element:
    tree: ElementTree = None
    root: Element = None
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))

    try:
        tree = ET.parse(file_to_read, parser=parser)
        root = tree.getroot()
    except ET.ParseError as epe:
        raise ET.ParseError(
            "Failed to extract xml data tree from %s - %s" % file_to_read, epe
        )
    except OSError as ose:
        raise OSError("Failed to read %s - %s" % file_to_read, ose)

    return root


def extract_filenames(xml_root_tree: Element, namespace: Dict[str, str]) -> List[str]:
    filename_data: List[str] = []
    filename_data = xml_root_tree.findall(".//mediaMD:fileName", namespace)

    filenames = [filename.text for filename in filename_data]

    return filenames


def extract_original_file_ids(
    xml_root_tree: Element, namespace: Dict[str, str]
) -> List[str]:
    file_id_data: List[str] = []
    file_id_data = xml_root_tree.findall(
        ".//mets:fileSec/mets:fileGrp[@USE='Original']//mets:file", namespace
    )
    file_ids = [file_id.attrib.get("ID") for file_id in file_id_data]

    return file_ids


def extract_recorded_area_elements(
    xml_root_tree: Element, namespace: Dict[str, str]
) -> List[Element]:
    recorded_area_elements: List[Element] = []

    recorded_area_elements = xml_root_tree.findall(
        ".//mets:structMap/[@TYPE='PHYSICAL']//mets:div[@TYPE='Recorded Area']",
        namespace,
    )
    return recorded_area_elements


def parse_recorded_area_data(
    element: List[Element], namespace: Dict[str, str]
) -> RecordedAreaData:
    physical_id = element.attrib.get("ID")
    recorded_area = element.find(
        "./mets:fptr/mets:area", namespace
    )  # use .find to return the first element in mets:area (i.e. 'Orignal' file)
    file_id = recorded_area.attrib.get("FILEID")
    timecode_in = recorded_area.attrib.get("BEGIN")
    timecode_out = recorded_area.attrib.get("END")

    return RecordedAreaData(physical_id, file_id, timecode_in, timecode_out)


def extract_struct_link_elements(
    xml_root_tree: Element, namespace: List[Dict[str, str]]
) -> List[Element]:
    struct_link_elements = xml_root_tree.findall(
        ".//mets:structLink//mets:smLinkGrp", namespace
    )
    return struct_link_elements


def extract_record_titles(
    element: List[Element], namespace: List[Dict[str, str]]
) -> RecordTitleData:
    title: str = None
    physical_id: str = None

    for child in element:
        if child.tag is ET.Comment:
            title = child.text
        elif (
            child.tag == "{http://www.loc.gov/METS/}smLocatorLink"
            and child.attrib.get("{http://www.w3.org/1999/xlink}href").startswith(
                "#phys"
            )
        ):
            physical_id = child.attrib.get("{http://www.w3.org/1999/xlink}href")

            return RecordTitleData(title, physical_id)

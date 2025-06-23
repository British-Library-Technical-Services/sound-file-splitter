import os
import xml.etree.ElementTree as et

file_path = "sc_files/C324"
xml_file = "C0324X10X01X_METS.xml"

objects = []
unique_items = set()

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


    def get_filename(self):
        self.filename = (self.root.find(".//mediaMD:fileName", namespaces=self.ns).text)

    def get_file_reference(self, area):
        if area.attrib.get("TYPE") == "Recorded Area":
            self.file_reference = area.attrib.get("ID")

    def get_timecode_ranges(self, timecodes):
        self.tc_in, self.tc_out = timecodes.attrib.get("BEGIN"), timecodes.attrib.get("END")

        #             unique_key = (item, tc_in, tc_out)
        #             if unique_key not in unique_items:
        #                 unique_items.add(unique_key)
        #                 objects.append({
        #                     "item": item,
        #                     "tc_in": tc_in,
        #                     "tc_out": tc_out
        #                 })
        # return objects

    def get_catalogue_title(self):
        for link_group in self.root.findall(".//mets:smLinkGrp", namespaces=self.ns):
            for child in link_group.iter():
                if child.tag == et.Comment and child.text.startswith("Parent"):
                    self.record_title = child.text

                sm_link = child.attrib.get("{http://www.w3.org/1999/xlink}href")
                if sm_link != None and sm_link.startswith("#phys"):
                    self.catalogue_reference = sm_link.strip("#")

def main():
    
    parser = et.XMLParser(target=et.TreeBuilder(insert_comments=True))
    data = et.parse(os.path.join(file_path, xml_file), parser=parser)
    root = data.getroot()
    ns = {"mets": "http://www.loc.gov/METS/", "mediaMD": "mediaMDv2.1.xsd"}

    object_data = []
    unique_keys = set()
    item_tc_data = []

    extract = XMLDataExtrator(root, ns)
    extract.get_filename()

    object_data.append({"file": extract.filename})
    
    recorded_area = root.find(".//mets:structMap[2]/mets:div/mets:div/mets:div[1]",
        namespaces=ns)

    for area in recorded_area: 
        extract.get_file_reference(area)
        if extract.file_reference not in unique_keys:
            unique_keys.add(extract.file_reference)
            object_data.append({"ref": extract.file_reference})

            # timecodes = root.findall(".//mets:area", namespaces=ns)
            # for timecode in timecodes:
            #     extract.get_timecode_ranges(timecode)
            
            #     item_tc_data = (extract.file_reference, extract.tc_in, extract.tc_out)
            #     # if item_tc_data not in unique_keys:
            #     #     unique_keys.add(item_tc_data)
            #     object_data.append({"ref": extract.file_reference, "tc_in": extract.tc_in, "tc_out": extract.tc_out})
        
    for obj in object_data:
        print(obj)
        
        # extract.get_catalogue_title()

if __name__ == "__main__":
    main()
        #             unique_key = (item, tc_in, tc_out)
        #             if unique_key not in unique_items:
        #                 unique_items.add(unique_key)
        #                 objects.append({
        #                     "item": item,
        #                     "tc_in": tc_in,
        #                     "tc_out": tc_out
        #                 })
        # return objects
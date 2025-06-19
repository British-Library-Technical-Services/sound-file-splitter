import xml.etree.ElementTree as et

xml_file = "C0324X10X01X_METS.xml"

data = et.parse(xml_file)
root = data.getroot()

ns = {"mets": "http://www.loc.gov/METS/"}
area = root.find("./mets:structMap[2]/mets:div/mets:div/mets:div[1]/mets:div[1]/mets:fptr/mets:area",
    namespaces=ns)
print(area.attrib)

struct_element = root.findall("mets:structMap", namespaces=ns)

#print(struct_element.get("BEGIN")

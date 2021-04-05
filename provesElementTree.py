#Script per probar funcionament de la Llibreria Element tree per a crear Fitxers XML

import xml.etree.ElementTree as ET

def createSampleTree1():
    root = ET.Element("entailment-corpus")
    root.set("num_edges","43")
    root.set("num_nodes","44")
    args = ET.SubElement(root, "argument-list")
    for i in range(1,10):
        arg = ET.SubElement(args, "arg"+str(i))
        arg.set("author", str(i))
        arg.text = "hotal"
    tree = ET.ElementTree()
    tree._setroot(root)
    tree.write("output.xml")

def main():
    createSampleTree1()

if __name__ == "__main__":
    main()

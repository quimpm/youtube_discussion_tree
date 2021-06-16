import xml.etree.ElementTree as ET

def _serialize_tree(output_file, nodes, aditional_atributes):
    root = ET.Element("entailment-corpus")
    root.set("num_edges", str(len(nodes)-1))
    root.set("num_nodes", str(len(nodes)))
    argument_lists = ET.SubElement(root, "argument-list")
    argument_pairs = ET.SubElement(root, "argument-pairs")
    for i,node in enumerate(nodes):
        _create_argument(argument_lists, node, aditional_atributes)
        _create_pair(argument_pairs, node, i)
    tree = ET.ElementTree()
    tree._setroot(root)
    tree.write(output_file)

def _create_argument(argument_list, node, aditional_atributes):
    arg = ET.SubElement(argument_list, "arg")
    arg.text = node.text
    arg.set("author", node.author_name)
    arg.set("author_id", node.author_id)
    arg.set("id", node.id)
    arg.set("likeCount", str(node.like_count))
    if aditional_atributes:
        atributes = aditional_atributes(node)
        for label,value in atributes.items():
            arg.set(label, value)

def _create_pair(argument_pair, node, i):
    if node.parent_id:
        pair = ET.SubElement(argument_pair, "pair")
        pair.set("id", str(i))
        t = ET.SubElement(pair, "t")
        t.set("id", node.id)
        h = ET.SubElement(pair, "h")
        h.set("id", node.parent_id)

    
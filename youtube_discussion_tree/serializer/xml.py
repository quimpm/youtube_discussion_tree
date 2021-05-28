from transformers import pipeline
import xml.etree.ElementTree as ET
from ..utils import bcolors

def serialize_tree(output_file, nodes, sa):
    print(bcolors.HEADER+"Serializing discussion tree"+bcolors.ENDC)
    root = ET.Element("entailment-corpus")
    root.set("num_edges", str(len(nodes)-1))
    root.set("num_nodes", str(len(nodes)))
    argument_lists = ET.SubElement(root, "argument-list")
    argument_pairs = ET.SubElement(root, "argument-pairs")
    for i,node in enumerate(nodes):
        create_argument(argument_lists, node, sa)
        create_pair(argument_pairs, node, i)
    tree = ET.ElementTree()
    tree._setroot(root)
    tree.write(output_file)

def create_argument(argument_list, node, sa):
    arg = ET.SubElement(argument_list, "arg")
    arg.text = node.text
    arg.set("author", node.author_name)
    arg.set("author_id", node.author_id)
    arg.set("id", node.id)
    arg.set("score", str(node.likeCount))
    if sa:
        sentiment_analysis = do_sentiment_analysis(node)
        for key,value in sentiment_analysis.items():
            arg.set(key, str(value))

def do_sentiment_analysis(node):
    sentiment_analysis = pipeline("sentiment-analysis")
    result = sentiment_analysis(node.text)[0]
    return {
        "sentiment" : result["label"],
        "sentiment_prob" : round(result["score"], 4)
    }

def create_pair(argument_pair, node, i):
    if node.parent_id:
        pair = ET.SubElement(argument_pair, "pair")
        pair.set("id", str(i))
        t = ET.SubElement(pair, "t")
        t.set("id", node.id)
        h = ET.SubElement(pair, "h")
        h.set("id", node.parent_id)

    
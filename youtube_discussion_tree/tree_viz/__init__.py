from treelib import Node, Tree
from ..utils import bcolors

def print_graph(nodes):
        tree = Tree()
        for node in nodes:
            if node.parent_id == None:
                tree.create_node(node.id, node.id)
            else:
                tree.create_node(node.id, node.id, parent=node.parent_id)
        print(bcolors.HEADER+"Generated Discusion Tree: \n"+bcolors.ENDC)
        tree.show()
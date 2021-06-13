from treelib import Node, Tree

def _print_graph(nodes):
        tree = Tree()
        for node in nodes:
            if node.parent_id == None:
                tree.create_node(node.id, node.id)
            else:
                tree.create_node(node.id, node.id, parent=node.parent_id)
        tree.show()
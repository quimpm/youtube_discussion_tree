import networkx as nx

class DiscusionTreeVisualizer():

    def __init__(self, tree):
        self.tree = tree

    def print_graph(self):
        G=nx.Graph()
        for node in self.tree.nodes:
            if node.parent_id != None:
                G.add_node(node.id)
                edge = (node.id, node.parent_id)
                G.add_edge(*edge)
            else:
                G.add_node(node.id)
        nx.draw(G)

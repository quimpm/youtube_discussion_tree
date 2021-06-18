from datetime import datetime
from unittest import TestCase
import xml.etree.ElementTree as ET
from youtube_discussion_tree_api.utils import Node
from youtube_discussion_tree_api._xml import _create_argument, _create_pair, _serialize_tree
import os


class TestXmlTreeConstruction(TestCase):

    def test_create_argument(self):
        argument_list = ET.Element("argument-list")
        node = Node(
                id = "comment1",
                author_name = "Ororo",
                author_id = "author1",
                text = "Hello, I love turtles and dogs",
                like_count = 10000000,
                parent_id = None,
                published_at = "12-12-2012"
            )
        _create_argument(argument_list, node, None)
        self.assertEqual(node.id, argument_list.find("arg").get("id"))

    def test_create_pair(self):
        argument_pair = argument_list = ET.Element("argument-list")
        node = Node(
                id = "comment1",
                author_name = "Ororo",
                author_id = "author1",
                text = "Hello, I love turtles and dogs",
                like_count = 10000000,
                parent_id = "Turtle",
                published_at = "12-12-2012"
            )
        _create_pair(argument_pair, node, 0)
        self.assertEqual('0', argument_list.find("pair").get("id"))
        self.assertEqual(node.id, argument_list.find("pair").find("t").get("id"))
        self.assertEqual(node.parent_id, argument_list.find("pair").find("h").get("id"))

    def test_serialize_tree(self):
        nodes = [
            Node(
                id = "comment1",
                author_name = "Ororo",
                author_id = "author1",
                text = "Hello, I love turtles and dogs",
                like_count = 10000000,
                parent_id = None,
                published_at = "12-12-2012"
            ),
            Node(
                id = "comment2",
                author_name = "Horno Microondas",
                author_id = "author2",
                text = "Cats are the best animals in the whole world",
                like_count = 10000000,
                parent_id = "comment1",
                published_at = "12-12-2012"
            ),
            Node(
                id = "comment3",
                author_name = "Kekino",
                author_id = "author3",
                text = "I'm more of a dogs person, they are so cute",
                like_count = 10000000,
                parent_id = "comment1",
                published_at = "12-12-2012"
            )
        ]
        _serialize_tree("./youtube_discussion_tree_api/tests/output.xml", nodes, None)
        self.assertTrue(os.path.isfile("./youtube_discussion_tree_api/tests/output.xml"))
        tree = ET.parse('./youtube_discussion_tree_api/tests/output.xml')
        self.assertEqual("entailment-corpus",tree.findall(".")[0].tag)
        self.assertTrue(tree.find("./argument-list") != None)
        self.assertTrue(tree.find("./argument-pairs") != None)
        self.assertTrue(3,len(tree.findall("./argument-list/arg")))
        self.assertTrue(3,len(tree.findall("./argument-pairs/pairs")))
        
        
from unittest import TestCase
from youtube_discussion_tree_api._tree import YoutubeDiscussionTree
from youtube_discussion_tree_api._conflicts import _tf_idf_automatic_algorithm
import json
import os
from youtube_discussion_tree_api.utils import Node

class TestYoutubeDisscusionTree(TestCase):

    def setUp(self):
        self.tree = YoutubeDiscussionTree("9GHmfg54gg8", _tf_idf_automatic_algorithm)

    def test_make_tree(self):
        with open("./youtube_discussion_tree_api/tests/comments.json", "r") as f:
            comments = json.load(f)
        tree = self.tree.make_tree(
                        {
                            "id" : "video1",
                            "snippet" : {
                                "channelTitle" : "authorOfVideo1",
                                "channelId" : "author1",
                                "publishedAt" : "12-12-2012"
                            },
                            "statistics" : {
                                "likeCount" : 10000000
                            }
                        },
                        "Video of turtles",
                        comments["items"]
                    )
        self.assertEqual(8, len(tree.nodes))
        self.assertEqual(tree.nodes[0].id, "video1")
        self.assertEqual(tree.nodes[0].parent_id, None)
        self.assertEqual(tree.nodes[1].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg")
        self.assertEqual(tree.nodes[1].parent_id, "video1")
        self.assertEqual(tree.nodes[2].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYLPbgx68")
        self.assertEqual(tree.nodes[2].parent_id, "UgznJ9jPP_p6uIF5Wfp4AaABAg")
        self.assertEqual(tree.nodes[3].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYRUvooiC")
        self.assertEqual(tree.nodes[3].parent_id, "UgznJ9jPP_p6uIF5Wfp4AaABAg")
        self.assertEqual(tree.nodes[4].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYTJqtQ01")
        self.assertEqual(tree.nodes[5].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYcfNG7h0")
        self.assertEqual(tree.nodes[6].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9Nnv216MjLV")
        self.assertEqual(tree.nodes[6].parent_id, "UgznJ9jPP_p6uIF5Wfp4AaABAg")
        self.assertEqual(tree.nodes[7].id, "Ugzrk4QCbElug58ycGp4AaABAg")
        self.assertEqual(tree.nodes[7].parent_id, "video1")
        
    def test_serialize(self):
        with open("./youtube_discussion_tree_api/tests/comments.json", "r") as f:
            comments = json.load(f)
        tree = self.tree.make_tree(
                        {
                            "id" : "video1",
                            "snippet" : {
                                "channelTitle" : "authorOfVideo1",
                                "channelId" : "author1",
                                "publishedAt" : "12-12-2012"
                            },
                            "statistics" : {
                                "likeCount" : 10000000
                            }
                        },
                        "Video of turtles",
                        comments["items"]
                    )
        tree.serialize("./youtube_discussion_tree_api/tests/output.xml")
        self.assertTrue(os.path.isfile("./youtube_discussion_tree_api/tests/output.xml"))

    def test_create_comment_nodes(self):
        with open("./youtube_discussion_tree_api/tests/comments.json", "r") as f:
            comments = json.load(f)
        self.tree._create_comment_nodes(comments["items"], "video1")
        self.assertEqual(self.tree.nodes[0].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg")
        self.assertEqual(self.tree.nodes[0].parent_id, "video1")
        self.assertEqual(self.tree.nodes[1].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYLPbgx68")
        self.assertEqual(self.tree.nodes[1].parent_id, "UgznJ9jPP_p6uIF5Wfp4AaABAg")
        self.assertEqual(self.tree.nodes[2].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYRUvooiC")
        self.assertEqual(self.tree.nodes[2].parent_id, "UgznJ9jPP_p6uIF5Wfp4AaABAg")
        self.assertEqual(self.tree.nodes[3].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYTJqtQ01")
        self.assertEqual(self.tree.nodes[4].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYcfNG7h0")
        self.assertEqual(self.tree.nodes[5].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9Nnv216MjLV")
        self.assertEqual(self.tree.nodes[5].parent_id, "UgznJ9jPP_p6uIF5Wfp4AaABAg")
        self.assertEqual(self.tree.nodes[6].id, "Ugzrk4QCbElug58ycGp4AaABAg")
        self.assertEqual(self.tree.nodes[6].parent_id, "video1")

    def test_create_replie_nodes(self):
        with open("./youtube_discussion_tree_api/tests/comments.json", "r") as f:
            comments = json.load(f)
        item = comments["items"][0]
        self.tree._create_replies_nodes(list(reversed(item["replies"]["comments"])), item["snippet"]["topLevelComment"]["id"])
        self.assertEqual(self.tree.nodes[0].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYLPbgx68")
        self.assertEqual(self.tree.nodes[0].parent_id, "UgznJ9jPP_p6uIF5Wfp4AaABAg")
        self.assertEqual(self.tree.nodes[1].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYRUvooiC")
        self.assertEqual(self.tree.nodes[1].parent_id, "UgznJ9jPP_p6uIF5Wfp4AaABAg")
        self.assertEqual(self.tree.nodes[2].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYTJqtQ01")
        self.assertEqual(self.tree.nodes[3].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYcfNG7h0")
        self.assertEqual(self.tree.nodes[4].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9Nnv216MjLV")
        self.assertEqual(self.tree.nodes[4].parent_id, "UgznJ9jPP_p6uIF5Wfp4AaABAg")

    def test_create_deep_replie_node_no_conflict(self):
        node = self.tree._create_deep_replie_node("Quim Pic?? Mora",    
                                            {
                                                "id" : "comment2",
                                                "snippet" : {
                                                    "authorChannelId" : {
                                                        "value" : "author2"
                                                    },
                                                    "authorDisplayName" : "Miquel Farr??",
                                                    "textOriginal" : "I like Turtles",
                                                    "likeCount" : 100000,
                                                    "publishedAt" : "12-12-2020"
                                                }
                                            }, {
                                                "Quim Pic?? Mora" : [Node(
                                                    id = "comment1",
                                                    author_name = "Quim Pic?? Mora",
                                                    author_id = "author1",
                                                    text = "Comment about turtles",
                                                    like_count = 10000000,
                                                    parent_id = None,
                                                    published_at = "12-12-2012"
                                                )]
                                            })
        self.assertEqual("comment1", node.parent_id)


    def test_create_deep_replie_node_conflict(self):
        node = self.tree._create_deep_replie_node("Quim Pic?? Mora",    
                                            {
                                                "id" : "comment2",
                                                "snippet" : {
                                                    "authorChannelId" : {
                                                        "value" : "author2"
                                                    },
                                                    "authorDisplayName" : "Miquel Farr??",
                                                    "textOriginal" : "I like Turtles, i found them really interesting and cute",
                                                    "likeCount" : 100000,
                                                    "publishedAt" : "12-12-2020"
                                                }
                                            }, {
                                                "Quim Pic?? Mora" : [Node(
                                                    id = "comment1",
                                                    author_name = "Quim Pic?? Mora",
                                                    author_id = "author1",
                                                    text = "Comment about turtles, turtles are really interesting",
                                                    like_count = 10000000,
                                                    parent_id = None,
                                                    published_at = "12-12-2012"
                                                ),Node(
                                                    id = "comment2",
                                                    author_name = "Quim Pic?? Mora",
                                                    author_id = "author1",
                                                    text = "Cats are animals that have 4 legs and are cute",
                                                    like_count = 10000000,
                                                    parent_id = None,
                                                    published_at = "12-12-2012"
                                                )]
                                            })
        self.assertEqual("comment1", node.parent_id)

    def test_actualize_contributions_first_contribution(self):
        contributions = self.tree._actualize_contributions(Node(
                id = "comment1",
                author_name = "Quim Pic?? Mora",
                author_id = "author1",
                text = "Comment about turtles",
                like_count = 10000000,
                parent_id = None,
                published_at = "12-12-2012"
            ), {})
        self.assertEqual("comment1", contributions["Quim Pic?? Mora"][0].id)
    
    def test_actualize_contributions_various_contributions(self):
        contributions= self.tree._actualize_contributions(Node(
                id = "comment1",
                author_name = "Quim Pic?? Mora",
                author_id = "author1",
                text = "Comment about turtles",
                like_count = 10000000,
                parent_id = None,
                published_at = "12-12-2012"
            ), {
                "Quim Pic?? Mora" : [Node(
                    id = "comment2",
                    author_name = "Quim Pic?? Mora",
                    author_id = "author1",
                    text = "Cats are animals",
                    like_count = 10000000,
                    parent_id = None,
                    published_at = "12-12-2012"
                )]
            })
        self.assertEqual(2, len(contributions["Quim Pic?? Mora"]))
        self.assertEqual("comment1", contributions["Quim Pic?? Mora"][1].id)

    def test_new_node(self):
        jsonComment = {
                                                "id" : "comment2",
                                                "snippet" : {
                                                    "authorChannelId" : {
                                                        "value" : "author2"
                                                    },
                                                    "authorDisplayName" : "Miquel Farr??",
                                                    "textOriginal" : "I like Turtles, i found them really interesting and cute",
                                                    "likeCount" : 100000,
                                                    "publishedAt" : "12-12-2020"
                                                }
                                            }
        node = self.tree._new_node(jsonComment, "root")
        self.assertEqual(jsonComment["id"],node.id)
        self.assertEqual(jsonComment["snippet"]["authorDisplayName"], node.author_name)
        self.assertEqual(jsonComment["snippet"]["authorChannelId"]["value"], node.author_id)
        self.assertEqual(jsonComment["snippet"]["textOriginal"], node.text)
        self.assertEqual(jsonComment["snippet"]["likeCount"], node.like_count)
        self.assertEqual(jsonComment["snippet"]["publishedAt"], node.published_at)
        self.assertEqual("root", node.parent_id)
        
    def test_get_possible_names(self):
        self.assertEqual(list(reversed(["Quim", "Quim Pic??", "Quim Pic?? Mora"])), self.tree._get_possible_names("@Quim Pic?? Mora".split()))
        self.assertEqual(list(reversed(["Quim", "Quim Pic??", "Quim Pic?? Mora", "Quim Pic?? Mora aaaaaa", "Quim Pic?? Mora aaaaaa aaaaaa"])), self.tree._get_possible_names("@Quim Pic?? Mora aaaaaa aaaaaa".split()))
        self.assertEqual(["Quim"], self.tree._get_possible_names("@Quim".split()))

    def test_find_name_in_thread(self):
        self.assertEqual("Quim Pic?? Mora", self.tree._find_name_in_thread(["Quim", "Quim Pic??", "Quim Pic?? Mora"], {"Quim Pic?? Mora" : "Tha one and only"}))
        
    def test_tree_equals(self):
        with open("./youtube_discussion_tree_api/tests/comments.json", "r") as f:
            comments = json.load(f)
        tree1 = self.tree.make_tree(
                        {
                            "id" : "video1",
                            "snippet" : {
                                "channelTitle" : "authorOfVideo1",
                                "channelId" : "author1",
                                "publishedAt" : "12-12-2012"
                            },
                            "statistics" : {
                                "likeCount" : 10000000
                            }
                        },
                        "Video of turtles",
                        comments["items"]
                    )
        tree2 = self.tree.make_tree(
                        {
                            "id" : "video1",
                            "snippet" : {
                                "channelTitle" : "authorOfVideo1",
                                "channelId" : "author1",
                                "publishedAt" : "12-12-2012"
                            },
                            "statistics" : {
                                "likeCount" : 10000000
                            }
                        },
                        "Video of turtles",
                        comments["items"]
                    )
        self.assertTrue(tree1==tree2)

    def test_tree_not_equals(self):
        with open("./youtube_discussion_tree_api/tests/comments.json", "r") as f:
            comments = json.load(f)
        tree1 = self.tree.make_tree(
                        {
                            "id" : "video2",
                            "snippet" : {
                                "channelTitle" : "authorOfVideo1",
                                "channelId" : "author1",
                                "publishedAt" : "12-12-2012"
                            },
                            "statistics" : {
                                "likeCount" : 10000000
                            }
                        },
                        "Video of turtles",
                        comments["items"]
                    )
        tree2 = self.tree.make_tree(
                        {
                            "id" : "video1",
                            "snippet" : {
                                "channelTitle" : "authorOfVideo1",
                                "channelId" : "author1",
                                "publishedAt" : "12-12-2012"
                            },
                            "statistics" : {
                                "likeCount" : 10000000
                            }
                        },
                        "Video of turtles",
                        comments["items"]
                    )
        self.assertTrue(tree1==tree2)
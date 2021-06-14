from youtube_discussion_tree_api.utils.video import Video
from youtube_discussion_tree_api import YoutubeDiscusionTreeAPI
from unittest import TestCase
import os
from youtube_discussion_tree_api._errors import SearchBoundsExceded
import pickle
from datetime import datetime

class TestYoutubeDiscusionTreeAPI(TestCase):

    def setUp(self):
        self.api_key = os.getenv('API_KEY')
        self.api = YoutubeDiscusionTreeAPI(self.api_key)

    #Replantejar com fer-ho
    def test_generate_tree(self):
        tree = self.api.generate_tree("9GHmfg54gg8")
        self.assertEqual(8, len(tree.nodes))
        self.assertEqual(tree.nodes[0].id, "9GHmfg54gg8")
        self.assertEqual(tree.nodes[0].parent_id, None)
        self.assertEqual(tree.nodes[1].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg")
        self.assertEqual(tree.nodes[1].parent_id, "9GHmfg54gg8")
        self.assertEqual(tree.nodes[7].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.º-9Nnv216MjLV")
        self.assertEqual(tree.nodes[7].parent_id, "UgznJ9jPP_p6uIF5Wfp4AaABAg")
        self.assertEqual(tree.nodes[6].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYcfNG7h0")
        self.assertEqual(tree.nodes[6].parent_id, "UgznJ9jPP_p6uIF5Wfp4AaABAg")
        self.assertEqual(tree.nodes[5].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYTJqtQ01")
        self.assertEqual(tree.nodes[4].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYRUvooiC")
        self.assertEqual(tree.nodes[3].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYRUvooiC")
        self.assertEqual(tree.nodes[2].id, "UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYLPbgx68")
        self.assertEqual(tree.nodes[8].id, "Ugzrk4QCbElug58ycGp4AaABAg")
        self.assertEqual(tree.nodes[8].parent_id, "9GHmfg54gg8")

    def test_quota_info(self):
        info = self.api.quota_info()
        self.assertIn("limit", info)
        self.assertIn("spent", info)

    def test_search_videos(self):
        videos = self.api.search_videos("Functional Programming", 20)
        self.assertEqual(20, len(videos))
        for video in videos:
            self.assertIs(Video)

    def test_search_video_rise_exception(self):
        self.assertRaises(self.api.search_videos("Functional Programming", 60), SearchBoundsExceded)
    
    def test_create_quota_controller(self):
        if os.path.exists(".quota.pickle"):
            os.remove(".quota.pickle")
        self.api._create_quota_controller()
        self.assertTrue(os.path.exists(".quota.pickle"))
        with open(".quota.pickle", "rb") as f:
            quota_controller = pickle.load(f)
        self.assertEqual(quota_controller.api_key, self.api_key)
        self.assertEqual(quota_controller.curr_date, datetime.now().strftime("%Y-%m-%d"))
        self.assertEqual(quota_controller.curr_quota, 0)
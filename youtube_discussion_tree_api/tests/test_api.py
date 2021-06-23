from youtube_discussion_tree_api.utils.video import Video
from youtube_discussion_tree_api import YoutubeDiscussionTreeAPI
from unittest import TestCase
import os
from youtube_discussion_tree_api._errors import SearchBoundsExceded
import pickle
from datetime import datetime

class TestYoutubeDiscussionTreeAPI(TestCase):

    def setUp(self):
        self.api_key = os.getenv('API_KEY')
        self.api = YoutubeDiscussionTreeAPI(self.api_key)

    def test_generate_tree(self):
        tree = self.api.generate_tree("9GHmfg54gg8")
        self.assertEqual(8, len(tree.nodes))
        nodes = [ (x.id, x.parent_id) for x in tree.nodes]
        self.assertTrue(("9GHmfg54gg8", None) in nodes)
        self.assertTrue(("UgznJ9jPP_p6uIF5Wfp4AaABAg", "9GHmfg54gg8") in nodes)
        self.assertTrue(("UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYLPbgx68", "UgznJ9jPP_p6uIF5Wfp4AaABAg") in nodes)
        self.assertTrue(("UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYRUvooiC", "UgznJ9jPP_p6uIF5Wfp4AaABAg"))
        self.assertTrue("UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYTJqtQ01" in [x[0] for x in nodes])
        self.assertTrue("UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9MvYcfNG7h0" in [x[0] for x in nodes])
        self.assertTrue(("UgznJ9jPP_p6uIF5Wfp4AaABAg.9MvYEeiNOK-9Nnv216MjLV", "UgznJ9jPP_p6uIF5Wfp4AaABAg") in nodes)
        self.assertTrue(("Ugzrk4QCbElug58ycGp4AaABAg", "9GHmfg54gg8") in nodes)

    def test_quota_info(self):
        info = self.api.quota_info()
        self.assertIn("limit", info)
        self.assertIn("spent", info)

    def test_search_videos(self):
        videos = self.api.search_videos("Functional Programming", 20)
        self.assertEqual(20, len(videos))
        for video in videos:
            self.assertIsInstance(video, Video)

    def test_search_video_rise_exception(self):
        with self.assertRaises(SearchBoundsExceded):
            self.api.search_videos("Functional Programming", 60)
    
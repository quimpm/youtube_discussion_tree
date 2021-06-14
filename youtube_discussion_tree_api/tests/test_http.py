from youtube_discussion_tree_api._http import _get_list_search_videos, _get_video_comments, _get_video_transcription, _get_video_info
from unittest import TestCase
import os
from youtube_discussion_tree_api.utils import QuotaController
import pickle

class TestHttpMethods(TestCase):

    def setUp(self):
        self.API_KEY = os.getenv("API_KEY")
        self.quota_controller = QuotaController("apikey", 0, "12-12-2012")
        with open(".quota.pickle", "wb") as f:
            pickle.dump(self.quota_controller, f)

    def test_get_video_comments(self):
        result = _get_video_comments("9GHmfg54gg8", self.API_KEY)
        self.assertIn("kind", result)
        self.assertEqual("youtube#commentThreadListResponse", result["kind"])
    
    def test_get_video_comments_bad_api_key(self):
        result = _get_video_comments("9GHmfg54gg8", "Google, Explode")
        self.assertIn("error", result)
        self.assertEqual(400, result["error"]["code"])

    def test_get_video_comments_no_api_key(self):
        result = _get_video_comments("9GHmfg54gg8", "")
        self.assertIn("error", result)
        self.assertEqual(403, result["error"]["code"])

    def test_get_video_comments_unexisting_video(self):
        result = _get_video_comments("Google, Explode", self.API_KEY)
        self.assertIn("error", result)
        self.assertEqual(404, result["error"]["code"])

    def test_get_video_info(self):
        result = _get_video_info("9GHmfg54gg8", self.API_KEY)
        self.assertIn("kind", result)
        self.assertEqual("youtube#videoListResponse", result["kind"])

    def test_get_video_info_bad_api_key(self):
        result = _get_video_info("9GHmfg54gg8", "Google, Explode")
        self.assertIn("error", result)
        self.assertEqual(400, result["error"]["code"])

    def test_get_video_info_no_api_key(self):
        result = _get_video_info("9GHmfg54gg8", "")
        self.assertIn("error", result)
        self.assertEqual(403, result["error"]["code"])

    def test_get_video_info_unexisting_video(self):
        result = _get_video_info("Google, Explode", self.API_KEY)
        self.assertIn("kind", result)
        self.assertEqual("youtube#videoListResponse", result["kind"])
        self.assertEqual(0, len(result["items"]))

    def test_get_list_search_videos(self):
        result = _get_list_search_videos("Functional Programming", 30, self.API_KEY)
        self.assertIn("kind", result)
        self.assertEqual("youtube#searchListResponse", result["kind"])
        self.assertEqual(30, len(result["items"]))

    def test_get_list_search_videos_bad_pk(self):
        result = _get_list_search_videos("Functional Programming", 30, "Google, Explode")
        self.assertIn("error", result)
        self.assertEqual(400, result["error"]["code"])

    def test_get_list_search_videos_bad_pk(self):
        result = _get_list_search_videos("Functional Programming", 30, "")
        self.assertIn("error", result)
        self.assertEqual(403, result["error"]["code"])
    
    def test_get_list_search_videos_bad_maxresults(self):
        result = _get_list_search_videos("Functional Programming", -1, self.API_KEY)
        self.assertIn("error", result)
        self.assertEqual(400, result["error"]["code"])
import pickle
from unittest import TestCase
from youtube_discussion_tree_api._quota import QuotaManager
import pickle
from youtube_discussion_tree_api.utils import QuotaInfo,YoutubeDataApiOperations
import os



class TestQuotaMethods(TestCase):

    def setUp(self):
        self.API_KEY = os.getenv("API_KEY")
        self.quota_manager = QuotaManager("./youtube_discussion_tree_api/tests/.quota.pickle", self.API_KEY)
        self.quota_controller = QuotaInfo("apikey", 0, "12-12-2012")
        with open("./youtube_discussion_tree_api/tests/.quota.pickle", "wb") as f:
            pickle.dump(self.quota_controller, f)

    def test_actualize_current_quota_list(self):
        self.quota_manager._actualize_current_quota(YoutubeDataApiOperations.LIST)
        with open("./youtube_discussion_tree_api/tests/.quota.pickle", "rb") as f:
            quota_controller_after = pickle.load(f)
        self.assertEqual(self.quota_controller.curr_quota+1, quota_controller_after.curr_quota)

    def test_actualize_current_quota_search(self):
        self.quota_manager._actualize_current_quota(YoutubeDataApiOperations.SEARCH)
        with open("./youtube_discussion_tree_api/tests/.quota.pickle", "rb") as f:
            quota_controller_after = pickle.load(f)
        self.assertEqual(self.quota_controller.curr_quota+100, quota_controller_after.curr_quota)

    def test_get_current_quota(self):
        self.assertEqual(self.quota_controller.curr_quota, self.quota_manager._get_current_quota())
import pickle
from unittest import TestCase
from youtube_discussion_tree_api._quota import _actualize_current_quota, _get_current_quota
import pickle
from youtube_discussion_tree_api.utils import QuotaController,QuotaOperations

class TestQuotaMethods(TestCase):

    def setUp(self):
        self.quota_controller = QuotaController("apikey", 0, "12-12-2012")
        with open(".quota.pickle", "wb") as f:
            pickle.dump(self.quota_controller, f)

    def test_actualize_current_quota_list(self):
        _actualize_current_quota(QuotaOperations.LIST)
        with open(".quota.pickle", "rb") as f:
            quota_controller_after = pickle.load(f)
        self.assertEqual(self.quota_controller.curr_quota+1, quota_controller_after.curr_quota)

    def test_actualize_current_quota_search(self):
        _actualize_current_quota(QuotaOperations.SEARCH)
        with open(".quota.pickle", "rb") as f:
            quota_controller_after = pickle.load(f)
        self.assertEqual(self.quota_controller.curr_quota+100, quota_controller_after.curr_quota)

    def test_get_current_quota(self):
        self.assertEqual(self.quota_controller.curr_quota, _get_current_quota())
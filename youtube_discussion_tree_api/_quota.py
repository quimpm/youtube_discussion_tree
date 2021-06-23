import pickle
from datetime import datetime
import os
from youtube_discussion_tree_api.utils import QuotaInfo

class QuotaManager():

    def __init__(self, filepath, api_key):
        self.api_key = api_key
        self.filepath = filepath
        if(not os.path.isfile(self.filepath)):
            quota_controller = QuotaInfo(self.api_key, 0, datetime.now().strftime("%Y-%m-%d"))
            with open(self.filepath, "wb") as f:
                pickle.dump(quota_controller, f)

    def _get_current_quota(self):
        with open(self.filepath, "rb") as f:
            quota_controler = pickle.load(f)
            return quota_controler.curr_quota

    def _actualize_current_quota(self,quota_operation):
        with open(self.filepath, "rb") as f:
            quota_controler = pickle.load(f)
            curr_date = datetime.now().strftime("%Y-%m-%d")
            if quota_controler.curr_date != curr_date:
                quota_controler.curr_quota = quota_operation
                quota_controler.curr_date = curr_date
            else:
                quota_controler.curr_quota += quota_operation
        with open(self.filepath, "wb") as f:
            pickle.dump(quota_controler, f)

    def _get_api_limit(self):
        return 10000
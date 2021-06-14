import pickle
from datetime import datetime

def _get_current_quota():
    with open(".quota.pickle", "rb") as f:
        quota_controler = pickle.load(f)
        return quota_controler.curr_quota

def _actualize_current_quota(quota_operation):
    with open(".quota.pickle", "rb") as f:
        quota_controler = pickle.load(f)
        curr_date = datetime.now().strftime("%Y-%m-%d")
        if quota_controler.curr_date != curr_date:
            quota_controler.curr_quota = quota_operation
            quota_controler.curr_date = curr_date
        else:
            quota_controler.curr_quota += quota_operation
    with open(".quota.pickle", "wb") as f:
        pickle.dump(quota_controler, f)

def _get_api_limit():
    return 10000
import pickle
from datetime import datetime

def _get_current_quota():
    quota_controler = pickle.load(open(".quota.pickle", "rb"))
    return quota_controler.curr_quota

def _actualize_current_quota(quota_operation):
    quota_controler = pickle.load(open(".quota.pickle", "rb"))
    curr_date = datetime.now().strftime("%Y-%m-%d")
    if quota_controler.curr_date != curr_date:
        quota_controler.curr_quota = quota_operation
        quota_controler.curr_date = curr_date
    else:
        quota_controler.curr_quota += quota_operation
    pickle.dump(quota_controler, open(".quota.pickle", "wb"))

def _get_api_limit():
    return 10000
from .utils import QuotaController
from ._conflicts import *
from .utils import Node
from ._http import *
from ._tree import YoutubeDiscusionTree
import time
import pickle
import os

class YoutubeDiscusionTreeAPI():

    def __init__(self, api_key):
        self.api_key = api_key
        self.__create_quota_controller()

    def generate_tree(self, video_id, summarization = False, conflict_solving_algorithm = tf_idf_automatic_algorithm):
        video_content = get_sumarization_of_video_transcription(video_id, summarization)
        video_info = get_video_info(video_id, self.api_key)
        comments = get_video_comments(video_id, self.api_key)["items"]
        return YoutubeDiscusionTree(video_id, conflict_solving_algorithm).make_tree(Node (
                                                            id = video_info["items"][0]["id"],
                                                            author_name = video_info["items"][0]["snippet"]["channelTitle"],
                                                            author_id = video_info["items"][0]["snippet"]["channelId"],
                                                            text = video_content,
                                                            like_count = video_info["items"][0]["statistics"]["likeCount"],
                                                            parent_id = None
                                                        ),
                                                        comments
                                            )

    def quota_info(self):
        return {
            "limit" : get_api_limit(),
            "spent" : get_current_quota()
        }

    def __create_quota_controller(self):
        if(not os.path.isfile('./.quota.pickle')):
            quota_controller = QuotaController(self.api_key, 0, int(time.time()))
            pickle.dump(quota_controller, open("quota.pickle", "wb"))

    def search_videos(self, query):
        pass
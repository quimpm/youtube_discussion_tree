from ._conflicts import _tf_idf_automatic_algorithm
from .utils import Node, Video
from ._http import _get_video_transcription, _get_video_info, _get_video_comments, _get_list_search_videos
from ._tree import YoutubeDiscusionTree
from ._quota import QuotaManager
from ._errors import SearchBoundsExceded
from transformers import pipeline

class YoutubeDiscusionTreeAPI():

    def __init__(self, api_key):
        self.api_key = api_key
        self.quota_manager = QuotaManager(".quota.pickle")

    def generate_tree(self, video_id, summarization = False, conflict_solving_algorithm = _tf_idf_automatic_algorithm):
        video_content = _get_video_transcription(video_id) if not summarization else self._sumarize_video(_get_video_transcription(video_id))
        video_info = _get_video_info(video_id, self.api_key, self.quota_manager)
        comments = _get_video_comments(video_id, self.api_key, self.quota_manager)["items"]
        return YoutubeDiscusionTree(video_id, conflict_solving_algorithm).make_tree(Node (
                                                            id = video_info["items"][0]["id"],
                                                            author_name = video_info["items"][0]["snippet"]["channelTitle"],
                                                            author_id = video_info["items"][0]["snippet"]["channelId"],
                                                            text = video_content,
                                                            like_count = video_info["items"][0]["statistics"]["likeCount"],
                                                            parent_id = None,
                                                            published_at = video_info["items"][0]["snippet"]["publishedAt"]
                                                        ),
                                                        comments
                                            )

    def quota_info(self):
        return {
            "limit" : self.quota_manager._get_api_limit(),
            "spent" : self.quota_manager._get_current_quota()
        }

    def search_videos(self, query, search_results = 5):
        if search_results < 0 or search_results > 50:
            raise SearchBoundsExceded(search_results, "Search Results parameter out of bounds, you have to set it from 0 to 50")
        videos_json = _get_list_search_videos(query, search_results, self.api_key, self.quota_manager)
        return list(map(lambda x : Video(
                                        id = x["id"]["videoId"],
                                        title = x["snippet"]["title"],
                                        description = x["snippet"]["description"],
                                        channel_name = x["snippet"]["channelTitle"],
                                        channel_id = x["snippet"]["channelId"],
                                        published_at = x["snippet"]["publishedAt"]
                                    ), 
                    videos_json["items"])) 
        

    def _sumarize_video(self, video_transcription):
        summarizer = pipeline("summarization")
        return summarizer(video_transcription, max_length=512, min_length=256, do_sample=False, truncation=True)[0]["summary_text"]
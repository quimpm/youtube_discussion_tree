import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from .utils import YoutubeDataApiOperations
from youtube_discussion_tree_api._errors import NoEnglishTranscription

def _get_video_transcription(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except:
        raise NoEnglishTranscription(video_id, "This video doen't suport a Transcription to english")
    formatter = TextFormatter()
    return formatter.format_transcript(transcript)

def _get_video_info(id_video, api_key, quota_manager):
    quota_manager._actualize_current_quota(YoutubeDataApiOperations.LIST)
    youtube_api_videos = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "key" : api_key,
        "part" : ["snippet", "statistics"],
        "id" : id_video
    }
    return requests.get(youtube_api_videos, params = params).json()

def _get_video_comments(id_video, api_key, quota_manager):
    quota_manager._actualize_current_quota(YoutubeDataApiOperations.LIST)
    youtube_api_comment_threads = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "key" : api_key,
        "part" : ["snippet", "replies"],
        "order" : "relevance",
        "videoId" : id_video,
        "maxResults" : 100
    }
    return requests.get(youtube_api_comment_threads, params = params).json()

def _get_list_search_videos(query, search_results, api_key, quota_manager):
    quota_manager._actualize_current_quota(YoutubeDataApiOperations.SEARCH)
    youtube_api_search = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key" : api_key,
        "part" : ["snippet"],
        "q" : query,
        "maxResults" : search_results,
        "type" : ["video"],
        "order" : "relevance",
        "videoCaption" : "closedCaption"
    }
    return requests.get(youtube_api_search, params).json()
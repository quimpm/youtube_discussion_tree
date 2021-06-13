import requests
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from .utils import QuotaOperations
from ._quota import *
import sys

def sumarize_video(video_transcription):
    summarizer = pipeline("summarization")
    return summarizer(video_transcription, max_length=512, min_length=256, do_sample=False, truncation=True)[0]["summary_text"]

def get_video_transcription(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    formatter = TextFormatter()
    return formatter.format_transcript(transcript)


def get_sumarization_of_video_transcription(video_id, summarizattion):
    video_content = get_video_transcription(video_id)
    if summarizattion:
        video_content = sumarize_video(video_content)
    return video_content

def get_video_info(id_video, api_key):
    actualize_current_quota(QuotaOperations.LIST)
    youtube_api_videos = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "key" : api_key,
        "part" : ["snippet", "statistics"],
        "id" : id_video
    }
    return requests.get(youtube_api_videos, params = params).json()

def get_video_comments(id_video, api_key):
    actualize_current_quota(QuotaOperations.LIST)
    youtube_api_comment_threads = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "key" : api_key,
        "part" : ["snippet", "replies"],
        "order" : "relevance",
        "videoId" : id_video,
        "maxResults" : 100
    }
    return requests.get(youtube_api_comment_threads, params = params).json()

def get_list_search_videos(query, search_results, api_key):
    actualize_current_quota(QuotaOperations.SEARCH)
    youtube_api_search = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key" : api_key,
        "part" : ["snippet"],
        "q" : query,
        "maxResults" : search_results,
        "type" : ["video"]
    }
    return requests.get(youtube_api_search, params).json()
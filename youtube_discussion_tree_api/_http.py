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
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    if not transcript_list :
        sys.exit("No transcriptions found")
    else:
        land_code_list = list(map(lambda x : x.language_code, transcript_list))
        if 'en' in land_code_list:
            english_transcript = transcript_list.find_transcript(['en'])
        else:
            transcriptables_to_english = list(filter( lambda x : x.is_translatable and 'en' in list(map(lambda x : x["language_code"], x.translation_languages)), transcript_list))
            english_transcript = transcriptables_to_english[0].translate('en')
    english_transcript = english_transcript.fetch()
    formatter = TextFormatter()
    return formatter.format_transcript(english_transcript)


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

def search_videos(query):
    pass
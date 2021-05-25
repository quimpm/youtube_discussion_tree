from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

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


def get_sumarization_of_video_transcription(video_id):
    video_transcription = get_video_transcription(video_id)
    video_content = sumarize_video(video_transcription)
    return video_content
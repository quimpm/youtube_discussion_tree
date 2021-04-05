import requests
import sys
from collections import namedtuple

Video = namedtuple("Video", ["id", "comments"])
CommentThread = namedtuple("CommentThread", ["topLevelComment", "replies"])
Comment = namedtuple("Comment", ["author", "likeCount", "id", "text"])

apiurl = "https://www.googleapis.com/youtube/v3/commentThreads"
apikey = "AIzaSyD-UjlHhqsZkhKKrDFp5PNaHyS6JHjLSUg"

def parse_replies(replies_json):
    if "replies" in replies_json["items"][0].keys():
        return list(map(lambda x : Comment(
                                author =  x["snippet"]["authorChannelId"]["value"],
                                likeCount = x["snippet"]["likeCount"],
                                id = x["id"],
                                text = x["snippet"]["textOriginal"]   
        ), replies_json["items"][0]["replies"]["comments"]))
    else:
        return []

def request_comment_replies(id_top_level_comment):
    params = {
        "key" : apikey,
        "part" : "replies",
        "id" : id_top_level_comment,
        "maxResults" : 100
    }
    return requests.get(apiurl, params = params).json()

def get_comment_replies(id_top_level_comment):
    replies_json = request_comment_replies(id_top_level_comment)
    return parse_replies(replies_json)

def construct_comment_threads(api_call_result):
    return list( map( lambda x : CommentThread (
                                        Comment( 
                                        author = x["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"],
                                        likeCount = x["snippet"]["topLevelComment"]["snippet"]["likeCount"],
                                        id = x["snippet"]["topLevelComment"]["id"],
                                        text = x["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                                        ), get_comment_replies(x["snippet"]["topLevelComment"]["id"])),  api_call_result["items"]))


def request_video_top_level_comments(id_video):
    params = {
        "key" : apikey,
        "part" : "snippet",
        "videoId" : id_video,
        "maxResults" : 100
    }
    return requests.get(apiurl, params = params).json()

def get_comment_threads_from_video(id_video):
    result = request_video_top_level_comments(id_video)
    return construct_comment_threads(result)


#Intentar pillar context del video amb alguna eina que pasi el video a text i amb una altra eina fer un sumarize. D'aquesta forma intentant pillar com a top level comment el contingut del video.
#https://github.com/rkomar4815/Video-Speech-to-Text
#https://deepai.org/machine-learning-model/summarization
def main():
    print("Put the id of the videos of which you want to download the comments separated by spaces")
    print("Example: <vid_id> <vid_id> <vid_id> ... <video_id>")
    id_videos = input().split()
    video_comments = list(map(lambda x : Video(id = x, comments=get_comment_threads_from_video(x)), id_videos))
    print(video_comments)

if __name__ == "__main__":
    main()
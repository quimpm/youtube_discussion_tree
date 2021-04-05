#Script prova descarregar comentaris d'un viedo
import requests
from collections import namedtuple

CommentThread = namedtuple("CommentThread", ["topLevelComment", "replies"])
Comment = namedtuple("Comment", ["author", "likeCount", "id", "text"])
url = "https://www.googleapis.com/youtube/v3/commentThreads"
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
    return requests.get(url, params = params).json()

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


def request_video_top_level_comments():
    id_video = "9LAp_1O8jP4"
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    apikey = "AIzaSyD-UjlHhqsZkhKKrDFp5PNaHyS6JHjLSUg"
    params = {
        "key" : apikey,
        "part" : "snippet",
        "videoId" : id_video,
        "maxResults" : 100
    }
    return requests.get(url, params = params).json()

def main():
    result = request_video_top_level_comments()
    commentThreads = construct_comment_threads(result)
    print(commentThreads)

if __name__ == "__main__":
    main()
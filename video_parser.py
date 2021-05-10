import requests
import sys
import re
from collections import namedtuple
from youtube_transcript_api import YouTubeTranscriptApi

Node = namedtuple("Node", ["id", "author_name", "author_id", "text", "likeCount", "parent"])

youtube_api_comment_threads = "https://www.googleapis.com/youtube/v3/commentThreads"
youtube_api_videos = "https://www.googleapis.com/youtube/v3/videos"
youtube_apikey = "AIzaSyD-UjlHhqsZkhKKrDFp5PNaHyS6JHjLSUg"

deepAI_apikey = "034ca4b8-4048-4f97-94f8-799dba1f25dc"
deepAI_url = "https://api.deepai.org/api/summarization"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def get_video_info(id_video):
    params = {
        "key" : youtube_apikey,
        "part" : ["snippet", "statistics"],
        "id" : id_video
    }
    return requests.get(youtube_api_videos, params = params).json()

def get_video_comments(id_video):
    params = {
        "key" : youtube_apikey,
        "part" : ["snippet", "replies"],
        "order" : "relevance",
        "videoId" : id_video,
        "maxResults" : 100
    }
    return requests.get(youtube_api_comment_threads, params = params).json()

def sumarize_video(video_transcription):
    return requests.post(
                            deepAI_url, 
                            data = {
                                "text" : video_transcription
                            },
                            headers={'api-key': deepAI_apikey}
                        ).json()

def get_sumarization_of_video_transcription(video_id):
    video_transcription = ' '.join(list(map(lambda x : x["text"], YouTubeTranscriptApi.get_transcript(video_id, languages=['en']))))
    video_content = sumarize_video(video_transcription)
    return video_content["output"]

def get_possible_names(match_string):
    if not match_string:
        return [" "]
    else:
        return [' '.join(match_string)[1:]] + get_possible_names(match_string[:-1])

def find_name_in_thread(possible_names, contributions):
    for name in possible_names:
        if name in contributions.keys():
            return name
    return []

def conflict_more_than_one_contribution(name, replie, contributions):
    print("\n" + bcolors.WARNING + "A CONFLICT was found:" + bcolors.ENDC)
    print(bcolors.OKGREEN + "To which of this comments:" + bcolors.ENDC)
    for i, comment in enumerate(contributions[name]):
        print(bcolors.OKCYAN + str(i)+" - "+comment.text + bcolors.ENDC)
    print(bcolors.OKGREEN + "Belongs the replie:" + bcolors.ENDC)
    print(bcolors.OKCYAN + "- "+replie["snippet"]["textOriginal"] + bcolors.ENDC)
    number = input(bcolors.OKGREEN + "Enter the number of the comment: " + bcolors.ENDC)
    return Node(
                parent = contributions[name][int(number)],
                id = replie["id"],
                author_id = replie["snippet"]["authorChannelId"]["value"],
                author_name = replie["snippet"]["authorDisplayName"],
                text = replie["snippet"]["textOriginal"],
                likeCount = replie["snippet"]["likeCount"]
            )

def create_deep_replie_node(name, replie, contributions):
    if len(contributions[name]) == 1:
        return Node(
                parent = contributions[name][0],
                id = replie["id"],
                author_id = replie["snippet"]["authorChannelId"]["value"],
                author_name = replie["snippet"]["authorDisplayName"],
                text = replie["snippet"]["textOriginal"],
                likeCount = replie["snippet"]["likeCount"]
            )
    else:
        return conflict_more_than_one_contribution(name, replie, contributions)

def create_normal_replie_node(parent, replie):
    return  Node(
                parent = parent,
                id = replie["id"],
                author_id = replie["snippet"]["authorChannelId"]["value"],
                author_name = replie["snippet"]["authorDisplayName"],
                text = replie["snippet"]["textOriginal"],
                likeCount = replie["snippet"]["likeCount"]
            )

def create_replies_nodes(replies, parent):
    contributions = {}
    nodes = []
    for replie in replies:  
        match = re.match('(@.{0,50} )', replie["snippet"]["textOriginal"])
        if match:
            possible_names = get_possible_names(match[0].split(" "))
            name = find_name_in_thread(possible_names, contributions)
            if not name:
                node = create_normal_replie_node(parent, replie)
            else:
                node = create_deep_replie_node(name, replie, contributions)
        else:
            node =  create_normal_replie_node(parent, replie)
        nodes.append(node)
        if replie["snippet"]["authorDisplayName"] in contributions.keys():
            contributions[replie["snippet"]["authorDisplayName"]].append(node)
        else:
            contributions[replie["snippet"]["authorDisplayName"]] = [node]
    return nodes

def create_top_level_comment_node(top_level_comment, parent):
    return Node(
        id = top_level_comment["id"],
        author_id = top_level_comment["snippet"]["authorChannelId"]["value"],
        author_name = top_level_comment["snippet"]["authorDisplayName"],
        text = top_level_comment["snippet"]["textOriginal"],
        likeCount = top_level_comment["snippet"]["likeCount"],
        parent = parent
    )

def create_comment_nodes(comment_threads, video_node):
    replies = []
    for comment_thread in comment_threads:
        top_level_coment = create_top_level_comment_node(comment_thread["snippet"]["topLevelComment"], video_node)
        if "replies" in comment_thread.keys():
            replies = create_replies_nodes(reversed(comment_thread["replies"]["comments"]), top_level_coment)
    return [top_level_coment] + replies

def create_root_node(video_sumarized, video_info):
    return Node (
            parent = None,
            id = video_info["items"][0]["id"],
            author_name = video_info["items"][0]["snippet"]["channelTitle"],
            author_id = video_info["items"][0]["snippet"]["channelId"],
            text = video_sumarized,
            likeCount = video_info["items"][0]["statistics"]["likeCount"]
        )

def main():
    print("Put the id of the video of which you want to download the comments")
    id_video = input()
    video_sumarized = get_sumarization_of_video_transcription(id_video)
    video_info = get_video_info(id_video)
    comments = get_video_comments(id_video)
    root = create_root_node(video_sumarized, video_info)
    node_list = [root] + create_comment_nodes(comments["items"], root)
    

if __name__ == "__main__":
    main()
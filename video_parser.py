import requests
import sys
import re
import json
from collections import namedtuple
from stanfordcorenlp import StanfordCoreNLP
import xml.etree.ElementTree as ET
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import argparse
from transformers import pipeline

Node = namedtuple("Node", ["id", "author_name", "author_id", "text", "likeCount", "parent"])

youtube_apikey = "AIzaSyD-UjlHhqsZkhKKrDFp5PNaHyS6JHjLSUg"

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
    youtube_api_videos = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "key" : youtube_apikey,
        "part" : ["snippet", "statistics"],
        "id" : id_video
    }
    return requests.get(youtube_api_videos, params = params).json()

def get_video_comments(id_video):
    youtube_api_comment_threads = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "key" : youtube_apikey,
        "part" : ["snippet", "replies"],
        "order" : "relevance",
        "videoId" : id_video,
        "maxResults" : 100
    }
    return requests.get(youtube_api_comment_threads, params = params).json()

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

def conflict_more_than_one_contribution(name, replie, contributions, id_user):
    print("\n" + bcolors.WARNING + "A CONFLICT was found:" + bcolors.ENDC)
    print(bcolors.OKGREEN + "To which of this comments:" + bcolors.ENDC)
    for i, comment in enumerate(contributions[name][id_user]):
        print("\n" + bcolors.BOLD + str(i) + bcolors.ENDC + bcolors.OKCYAN + " - "+comment.text + bcolors.ENDC)
    print("\n" + bcolors.OKGREEN + "Belongs the replie:" + bcolors.ENDC)
    print(bcolors.OKCYAN + "- "+replie["snippet"]["textOriginal"] + bcolors.ENDC)
    number = -1
    while number not in range(len(contributions[name][id_user])):
        try:
            number = int(input("\n" + bcolors.OKGREEN + "Enter the number of the comment: " + bcolors.ENDC))
        except:
            number = -1
    return Node(
                parent = contributions[name][id_user][number].id,
                id = replie["id"],
                author_id = replie["snippet"]["authorChannelId"]["value"],
                author_name = replie["snippet"]["authorDisplayName"],
                text = replie["snippet"]["textOriginal"],
                likeCount = replie["snippet"]["likeCount"]
            )

def conflict_users_with_same_username_in_thread(name, replie, contributions):
    if replie["snippet"]["authorChannelId"]["value"] in contributions[name].keys() and len(contributions[name].keys()) == 2:
        return create_deep_replie_node(name, replie, contributions, list(filter(lambda x : x!=replie["snippet"]["authorChannelId"]["value"], contributions[name].keys()))[0])
    else: 
        print("\n" + bcolors.WARNING + "A CONFLICT was found:" + bcolors.ENDC)
        print(bcolors.OKGREEN + "Found some users with same username in a comment thread: "+ name + bcolors.ENDC)
        print(bcolors.OKGREEN + "To which of this users it belongs the comment that the reply refers to:" + bcolors.ENDC)
        for id_user in contributions[name].keys():
            if id_user != replie["snippet"]["authorChannelId"]["value"]:
                print("\n- "+id_user)
                for i,comment in enumerate(contributions[name][id_user]):
                    print(bcolors.BOLD + str(i) + bcolors.ENDC + bcolors.OKCYAN + " - "+comment.text + bcolors.ENDC + "\n")
        print("\n" + bcolors.OKGREEN + "It belongs the replie:" + bcolors.ENDC)
        print(bcolors.OKCYAN + "- "+replie["snippet"]["textOriginal"] + bcolors.ENDC)
        id_user = ""
        while id_user not in contributions[name].keys():
            id_user = input("\n" + bcolors.OKGREEN + "Enter the id of the user: " + bcolors.ENDC)
        return create_deep_replie_node(name, replie, contributions, id_user)

def create_deep_replie_node(name, replie, contributions, id_user):
        if len(contributions[name][id_user]) == 1:
            return Node(
                    parent = contributions[name][id_user][0].id,
                    id = replie["id"],
                    author_id = replie["snippet"]["authorChannelId"]["value"],
                    author_name = replie["snippet"]["authorDisplayName"],
                    text = replie["snippet"]["textOriginal"],
                    likeCount = replie["snippet"]["likeCount"]
                )
        else:
            return conflict_more_than_one_contribution(name, replie, contributions, id_user)

def create_normal_replie_node(parent, replie):
    return  Node(
                parent = parent.id,
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
                id_users = contributions[name].keys()
                if len(id_users) == 1:
                    node = create_deep_replie_node(name, replie, contributions, list(contributions[name].keys())[0])
                else: 
                    node = conflict_users_with_same_username_in_thread(name, replie, contributions)
        else:
            node =  create_normal_replie_node(parent, replie)
        nodes.append(node)
        if replie["snippet"]["authorDisplayName"] in contributions.keys():
            if replie["snippet"]["authorChannelId"]["value"] in contributions[replie["snippet"]["authorDisplayName"]].keys():
                contributions[replie["snippet"]["authorDisplayName"]][replie["snippet"]["authorChannelId"]["value"]].append(node)
            else: 
                contributions[replie["snippet"]["authorDisplayName"]][replie["snippet"]["authorChannelId"]["value"]] = [node]
        else:
            contributions[replie["snippet"]["authorDisplayName"]] = {replie["snippet"]["authorChannelId"]["value"] : [node]}
    return nodes

def create_top_level_comment_node(top_level_comment, parent):
    return Node(
        id = top_level_comment["id"],
        author_id = top_level_comment["snippet"]["authorChannelId"]["value"],
        author_name = top_level_comment["snippet"]["authorDisplayName"],
        text = top_level_comment["snippet"]["textOriginal"],
        likeCount = top_level_comment["snippet"]["likeCount"],
        parent = parent.id
    )

def create_comment_nodes(comment_threads, video_node):
    replies = []
    for i,comment_thread in enumerate(comment_threads):
        top_level_coment = create_top_level_comment_node(comment_thread["snippet"]["topLevelComment"], video_node)
        if "replies" in comment_thread.keys():
            replies += [top_level_coment] + create_replies_nodes(reversed(comment_thread["replies"]["comments"]), top_level_coment)
        else:
            replies += [top_level_coment]
    return replies

def create_root_node(video_sumarized, video_info):
    return Node (
            parent = None,
            id = video_info["items"][0]["id"],
            author_name = video_info["items"][0]["snippet"]["channelTitle"],
            author_id = video_info["items"][0]["snippet"]["channelId"],
            text = video_sumarized,
            likeCount = video_info["items"][0]["statistics"]["likeCount"]
        )

def do_sentiment_analysis(node):
    sentiment_analysis = pipeline("sentiment-analysis")
    result = sentiment_analysis(node.text)[0]
    return {
        "sentiment" : result["label"],
        "sentiment_prob" : round(result["score"], 4)
    }

def create_argument(argument_list, node, sa_flag):
    arg = ET.SubElement(argument_list, "arg")
    arg.text = node.text
    arg.set("author", node.author_name)
    arg.set("author_id", node.author_id)
    arg.set("id", node.id)
    arg.set("score", str(node.likeCount))
    if sa_flag:
        sentiment_analysis = do_sentiment_analysis(node)
        for key,value in sentiment_analysis.items():
            arg.set(key, str(value))

def create_pair(argument_pair, node, i):
    if node.parent:
        pair = ET.SubElement(argument_pair, "pair")
        pair.set("id", str(i))
        t = ET.SubElement(pair, "t")
        t.set("id", node.id)
        h = ET.SubElement(pair, "h")
        h.set("id", node.parent)

def createXML(node_list, sa_flag):
    root = ET.Element("entailment-corpus")
    root.set("num_edges", str(len(node_list)-1))
    root.set("num_nodes", str(len(node_list)))
    argument_lists = ET.SubElement(root, "argument-list")
    argument_pairs = ET.SubElement(root, "argument-pairs")
    for i,node in enumerate(node_list):
        create_argument(argument_lists, node, sa_flag)
        create_pair(argument_pairs, node, i)
    tree = ET.ElementTree()
    tree._setroot(root)
    tree.write("output.xml")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vid', help="id of the youtube video")
    parser.add_argument('--sa', help="Flag for sentiment analysis", action='store_true')
    args = parser.parse_args()
    print(bcolors.HEADER+"Transcribing and Summarizing the content of the video"+bcolors.ENDC)
    video_sumarized = get_sumarization_of_video_transcription(args.vid)
    print(bcolors.HEADER+"Getting other video Info"+bcolors.ENDC)
    video_info = get_video_info(args.vid)
    print(bcolors.HEADER+"Getting comments of the video"+bcolors.ENDC)
    comments = get_video_comments(args.vid)
    print(bcolors.HEADER+"Creating Comment Tree"+bcolors.ENDC)
    root = create_root_node(video_sumarized, video_info)
    node_list = [root] + create_comment_nodes(comments["items"], root)
    print(bcolors.HEADER+"Parsing Tree to XML"+ ( " with Sentiment Analysis" if args.sa else "") +bcolors.ENDC)
    createXML(node_list, args.sa)

if __name__ == "__main__":
    main()
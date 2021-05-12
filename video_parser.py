import requests
import sys
import re
from collections import namedtuple
from stanfordcorenlp import StanfordCoreNLP
import xml.etree.ElementTree as ET
from youtube_transcript_api import YouTubeTranscriptApi
import argparse

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
    for i, comment in enumerate(contributions[name][list(contributions[name].keys())[0]]):
        print("\n" + bcolors.BOLD + str(i) + bcolors.ENDC + bcolors.OKCYAN + " - "+comment.text + bcolors.ENDC)
    print("\n" + bcolors.OKGREEN + "Belongs the replie:" + bcolors.ENDC)
    print(bcolors.OKCYAN + "- "+replie["snippet"]["textOriginal"] + bcolors.ENDC)
    number = input("\n" + bcolors.OKGREEN + "Enter the number of the comment: " + bcolors.ENDC)
    return Node(
                parent = contributions[name][list(contributions[name].keys())[0]][int(number)].id,
                id = replie["id"],
                author_id = replie["snippet"]["authorChannelId"]["value"],
                author_name = replie["snippet"]["authorDisplayName"],
                text = replie["snippet"]["textOriginal"],
                likeCount = replie["snippet"]["likeCount"]
            )

def conflict_users_with_same_username_in_thread(name, replie, contributions):
    print("\n" + bcolors.WARNING + "A CONFLICT was found:" + bcolors.ENDC)
    print(bcolors.OKGREEN + "Found some users with same username in a comment thread: "+ name + bcolors.ENDC)
    print(bcolors.OKGREEN + "To which of this comments of the users with same username:" + bcolors.ENDC)
    for id_user in contributions[name].keys():
        if id_user != replie["snippet"]["authorChannelId"]["value"]:
            print("\n- "+id_user)
            for i,comment in enumerate(contributions[name][id_user]):
                print(bcolors.BOLD + str(i) + bcolors.ENDC + bcolors.OKCYAN + " - "+comment.text + bcolors.ENDC + "\n")
    print("\n" + bcolors.OKGREEN + "It belongs the replie:" + bcolors.ENDC)
    print(bcolors.OKCYAN + "- "+replie["snippet"]["textOriginal"] + bcolors.ENDC)
    id_user = input("\n" + bcolors.OKGREEN + "Enter the id of the user: " + bcolors.ENDC)
    comment = input("\n" + bcolors.OKGREEN + "Enter the number of the comment: " + bcolors.ENDC)
    return Node(
                parent = contributions[name][id_user][int(comment)].id,
                id = replie["id"],
                author_id = replie["snippet"]["authorChannelId"]["value"],
                author_name = replie["snippet"]["authorDisplayName"],
                text = replie["snippet"]["textOriginal"],
                likeCount = replie["snippet"]["likeCount"]
            )

def create_deep_replie_node(name, replie, contributions):
    id_users = contributions[name].keys()
    if len(id_users) == 1:
        if len(contributions[name][list(contributions[name].keys())[0]]) == 1:
            return Node(
                    parent = contributions[name][list(contributions[name].keys())[0]][0].id,
                    id = replie["id"],
                    author_id = replie["snippet"]["authorChannelId"]["value"],
                    author_name = replie["snippet"]["authorDisplayName"],
                    text = replie["snippet"]["textOriginal"],
                    likeCount = replie["snippet"]["likeCount"]
                )
        else:
            return conflict_more_than_one_contribution(name, replie, contributions)
    else:
            return conflict_users_with_same_username_in_thread(name, replie, contributions)

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
                node = create_deep_replie_node(name, replie, contributions)
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

def create_argument(argument_list, node, nlp_core):
    arg = ET.SubElement(argument_list, "arg")
    arg.text = node.text
    arg.set("author", node.author_name)
    arg.set("author_id", node.author_id)
    arg.set("id", node.id)
    arg.set("score", str(node.likeCount))

def create_pair(argument_pair, node, i):
    if node.parent:
        pair = ET.SubElement(argument_pair, "pair")
        pair.set("id", str(i))
        t = ET.SubElement(pair, "t")
        t.set("id", node.id)
        h = ET.SubElement(pair, "h")
        h.set("id", node.parent)

def createXML(node_list, nlp_core):
    root = ET.Element("entailment-corpus")
    root.set("num_edges", str(len(node_list)-1))
    root.set("num_nodes", str(len(node_list)))
    argument_lists = ET.SubElement(root, "argument-list")
    argument_pairs = ET.SubElement(root, "argument-pairs")
    for i,node in enumerate(node_list):
        create_argument(argument_lists, node, nlp_core)
        create_pair(argument_pairs, node, i)
    tree = ET.ElementTree()
    tree._setroot(root)
    tree.write("output.xml")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vid', help="id of the youtube video")
    parser.add_argument('--nlp_path', help="Path to the CoreNLP folder")
    args = parser.parse_args()
    nlp_core = StanfordCoreNLP(args.nlp_path)
    video_sumarized = get_sumarization_of_video_transcription(args.vid)
    video_info = get_video_info(args.vid)
    comments = get_video_comments(args.vid)
    root = create_root_node(video_sumarized, video_info)
    node_list = [root] + create_comment_nodes(comments["items"], root)
    createXML(node_list, nlp_core)

if __name__ == "__main__":
    main()
import http
import re
from .conflicts import *
from .utils import Node
from .http import *

class YoutubeDiscusionTreeAPI():

    def __init__(self, api_key):
        self.api_key = api_key

    def generate_tree(self, video_id, mode = "iter"):
        video_content = get_sumarization_of_video_transcription(video_id)
        video_info = get_video_info(video_id, self.api_key)
        comments = get_video_comments(video_id, self.api_key)["items"]
        return YoutubeCommentTree(video_id).make_tree(Node (
                                                            id = video_info["items"][0]["id"],
                                                            author_name = video_info["items"][0]["snippet"]["channelTitle"],
                                                            author_id = video_info["items"][0]["snippet"]["channelId"],
                                                            text = video_content,
                                                            likeCount = video_info["items"][0]["statistics"]["likeCount"],
                                                            parent_id = None
                                                        ),
                                                        comments,
                                                        mode
                                            )

class YoutubeCommentTree():

    def __init__(self, video_id):
        self.video_id = video_id
        self.nodes = []
        self.contributions = {}
        self.conflict_same_username = {
            "auto" : automatic_same_username_conflict,
            "inter" : interactive_same_username_conflict
        }
        self.conflict_multiple_contributions = {
            "auto" : automatic_multiple_contributions_conflict,
            "inter" : interactive_multiple_contributions_conflict
        }

    def make_tree(self, root, comments, mode):
        self.nodes.append(root)
        self.__create_comment_nodes(comments, root, mode)
        return self

    def __create_comment_nodes(self, comment_threads, root, mode):
        for i,comment_thread in enumerate(comment_threads):
            self.__new_node(comment_thread["snippet"]["topLevelComment"], root.id)
            if "replies" in comment_thread.keys():
                self.__create_replies_nodes(reversed(comment_thread["replies"]["comments"]), self.nodes[-1].id, mode)

    def __create_replies_nodes(self, replies, top_level_comment_id, mode):
        for replie in replies:  
            match = re.match('(@.{0,50} )', replie["snippet"]["textOriginal"])
            if match:
                possible_names = self.__get_possible_names(match[0].split(" "))
                name = self.__find_name_in_thread(possible_names, self.contributions)
                if not name:
                   curr_node = self.__new_node(replie, top_level_comment_id)
                else:
                    id_users = list(self.contributions[name].keys())
                    if len(id_users) != 1:
                        if replie["snippet"]["authorChannelId"]["value"] in self.contributions[name].keys() and len(self.contributions[name].keys()) == 2:
                            return self.__create_deep_replie_node(name, replie, list(filter(lambda x : x!=replie["snippet"]["authorChannelId"]["value"], self.contributions[name].keys()))[0], mode)
                        else:
                            id_user = self.conflict_same_username[mode](name, replie, self.contributions)
                    else: 
                        id_user = id_users[0]
                    self.__create_deep_replie_node(name, replie, id_user, mode)
            else:
                curr_node = self.__new_node(replie, top_level_comment_id)
            self.nodes.append(curr_node)
            self.__actualize_contributions(replie, curr_node)

    def __create_deep_replie_node(self, name, replie, id_user, mode):
        if len(self.contributions[name][id_user]) == 1:
            return Node(
                    id = replie["id"],
                    author_id = replie["snippet"]["authorChannelId"]["value"],
                    author_name = replie["snippet"]["authorDisplayName"],
                    text = replie["snippet"]["textOriginal"],
                    likeCount = replie["snippet"]["likeCount"],
                    parent_id = self.contributions[name][id_user][0].id
                )
        else:
            coment_index = self.conflict_multiple_contributions[mode](name, replie, self.contributions, id_user)
            return Node(
                id = replie["id"],
                author_id = replie["snippet"]["authorChannelId"]["value"],
                author_name = replie["snippet"]["authorDisplayName"],
                text = replie["snippet"]["textOriginal"],
                likeCount = replie["snippet"]["likeCount"],
                parent_id = self.contributions[name][id_user][coment_index].id
            )

    def __actualize_contributions(self, replie, curr_node):
        if replie["snippet"]["authorDisplayName"] in self.contributions.keys():
            if replie["snippet"]["authorChannelId"]["value"] in self.contributions[replie["snippet"]["authorDisplayName"]].keys():
                self.contributions[replie["snippet"]["authorDisplayName"]][replie["snippet"]["authorChannelId"]["value"]].append(curr_node)
            else: 
                self.contributions[replie["snippet"]["authorDisplayName"]][replie["snippet"]["authorChannelId"]["value"]] = [curr_node]
        else:
            self.contributions[replie["snippet"]["authorDisplayName"]] = {replie["snippet"]["authorChannelId"]["value"] : [curr_node]}

    def __new_node(self, top_level_comment, parent_id):
            return Node(
                id = top_level_comment["id"],
                author_id = top_level_comment["snippet"]["authorChannelId"]["value"],
                author_name = top_level_comment["snippet"]["authorDisplayName"],
                text = top_level_comment["snippet"]["textOriginal"],
                likeCount = top_level_comment["snippet"]["likeCount"],
                parent_id = parent_id
            )
    
    def __get_possible_names(self, match_string):
        if not match_string:
            return [" "]
        else:
            return [' '.join(match_string)[1:]] + self.__get_possible_names(match_string[:-1])

    def __find_name_in_thread(self, possible_names, contributions):
        for name in possible_names:
            if name in contributions.keys():
                return name
        return []
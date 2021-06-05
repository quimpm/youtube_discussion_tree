import re
from youtube_discussion_tree.serializer.xml import serialize_tree
from .conflicts import *
from .utils import Node
from .http import *
from .serializer import serialize_tree
from .tree_viz import print_graph

class YoutubeDiscusionTreeAPI():

    def __init__(self, api_key):
        self.api_key = api_key

    def generate_tree(self, video_id, summarization = False, conflict_solving_algorithm = tf_idf_automatic_algorithm):
        video_content = get_sumarization_of_video_transcription(video_id, summarization)
        video_info = get_video_info(video_id, self.api_key)
        comments = get_video_comments(video_id, self.api_key)["items"]
        return YoutubeCommentTree(video_id, conflict_solving_algorithm).make_tree(Node (
                                                            id = video_info["items"][0]["id"],
                                                            author_name = video_info["items"][0]["snippet"]["channelTitle"],
                                                            author_id = video_info["items"][0]["snippet"]["channelId"],
                                                            text = video_content,
                                                            like_count = video_info["items"][0]["statistics"]["likeCount"],
                                                            parent_id = None
                                                        ),
                                                        comments
                                            )

class YoutubeCommentTree():

    def __init__(self, video_id, conflict_solving_algorithm):
        self.video_id = video_id
        self.conflict_solving_algorithm = conflict_solving_algorithm
        self.nodes = []
        self.contributions = {}

    def make_tree(self, root, comments):
        self.nodes.append(root)
        self.__create_comment_nodes(comments, root)
        return self

    def serialize(self, filename, aditional_atributes = None):
        serialize_tree(filename, self.nodes, aditional_atributes)

    def show(self):
        print_graph(self.nodes)

    def __create_comment_nodes(self, comment_threads, root):
        for i,comment_thread in enumerate(comment_threads):
            self.nodes.append(self.__new_node(comment_thread["snippet"]["topLevelComment"], root.id))
            if "replies" in comment_thread.keys():
                self.__create_replies_nodes(list(reversed(comment_thread["replies"]["comments"])), self.nodes[-1].id)

    def __create_replies_nodes(self, replies, top_level_comment_id):
        for reply in replies:  
            match = re.match('(@.{0,50} )', reply["snippet"]["textOriginal"])
            if match:
                possible_names = self.__get_possible_names(match[0].split(" "))
                name = self.__find_name_in_thread(possible_names, self.contributions)
                if not name:
                   curr_node = self.__new_node(reply, top_level_comment_id)
                else:
                    curr_node = self.__create_deep_replie_node(name, reply)
            else:
                curr_node = self.__new_node(reply, top_level_comment_id)
            self.nodes.append(curr_node)
            self.__actualize_contributions(reply, curr_node)

    def __create_deep_replie_node(self, name, reply):
        if len(self.contributions[name]) == 1:
            return Node(
                    id = reply["id"],
                    author_id = reply["snippet"]["authorChannelId"]["value"],
                    author_name = reply["snippet"]["authorDisplayName"],
                    text = reply["snippet"]["textOriginal"],
                    like_count = reply["snippet"]["likeCount"],
                    parent_id = self.contributions[name][0].id
                )
        else:
            parent_id = self.conflict_solving_algorithm(Node(
                                                            id = reply["id"],
                                                            author_id = reply["snippet"]["authorChannelId"]["value"],
                                                            author_name = reply["snippet"]["authorDisplayName"],
                                                            text = reply["snippet"]["textOriginal"],
                                                            like_count = reply["snippet"]["likeCount"],
                                                            parent_id = None
                                                        ), self.contributions[name])
            return Node(
                id = reply["id"],
                author_id = reply["snippet"]["authorChannelId"]["value"],
                author_name = reply["snippet"]["authorDisplayName"],
                text = reply["snippet"]["textOriginal"],
                like_count = reply["snippet"]["likeCount"],
                parent_id = parent_id
            )

    def __actualize_contributions(self, reply, curr_node):
        if reply["snippet"]["authorDisplayName"] in self.contributions.keys():
            self.contributions[reply["snippet"]["authorDisplayName"]].append(curr_node)
        else:
            self.contributions[reply["snippet"]["authorDisplayName"]] = [curr_node]

    def __new_node(self, top_level_comment, parent_id):
            return Node(
                id = top_level_comment["id"],
                author_id = top_level_comment["snippet"]["authorChannelId"]["value"],
                author_name = top_level_comment["snippet"]["authorDisplayName"],
                text = top_level_comment["snippet"]["textOriginal"],
                like_count = top_level_comment["snippet"]["likeCount"],
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
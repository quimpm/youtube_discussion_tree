from ._xml import _serialize_tree
from ._viz import _print_graph
from .utils import Node
import re

class YoutubeDiscussionTree():

    def __init__(self, video_id, conflict_solving_algorithm):
        self.video_id = video_id
        self.conflict_solving_algorithm = conflict_solving_algorithm
        self.nodes = []
        self.contributions = {}

    def make_tree(self, video_info, video_content, comments):
        root = Node (
                        id = video_info["id"],
                        author_name = video_info["snippet"]["channelTitle"],
                        author_id = video_info["snippet"]["channelId"],
                        text = video_content,
                        like_count = video_info["statistics"]["likeCount"],
                        parent_id = None,
                        published_at = video_info["snippet"]["publishedAt"]
                    )
        self.nodes.append(root)
        self._create_comment_nodes(comments, root.id)
        return self

    def serialize(self, filename, aditional_atributes=None):
        _serialize_tree(filename, self.nodes, aditional_atributes)

    def show(self):
        _print_graph(self.nodes)

    def get_nodes(self):
        return self.nodes

    def _create_comment_nodes(self, comment_threads, root_id):
        for i, comment_thread in enumerate(comment_threads):
            self.nodes.append(self._new_node(comment_thread["snippet"]["topLevelComment"], root_id))
            if "replies" in comment_thread.keys():
                self._create_replies_nodes(list(reversed(comment_thread["replies"]["comments"])), self.nodes[-1].id)

    def _create_replies_nodes(self, replies, top_level_comment_id):
        for reply in replies:
            match = re.match('(@.{0,50} )', reply["snippet"]["textOriginal"])
            if match:
                possible_names = self._get_possible_names(match[0].split(" "))
                name = self._find_name_in_thread(possible_names)
                if not name:
                    curr_node = self._new_node(reply, top_level_comment_id)
                else:
                    curr_node = self._create_deep_replie_node(name, reply)
            else:
                curr_node = self._new_node(reply, top_level_comment_id)
            self.nodes.append(curr_node)
            self._actualize_contributions(curr_node)

    def _create_deep_replie_node(self, name, reply):
        if len(self.contributions[name]) == 1:
            return self._new_node(reply, self.contributions[name][0].id)
        else:
            parent_id = self.conflict_solving_algorithm(self._new_node(reply, None), self.contributions[name])
            return self._new_node(reply, parent_id)

    def _actualize_contributions(self, curr_node):
        if curr_node.author_name in self.contributions.keys():
            self.contributions[curr_node.author_name].append(curr_node)
        else:
            self.contributions[curr_node.author_name] = [curr_node]

    def _new_node(self, comment, parent_id):
        return Node(
            id=comment["id"],
            author_id=comment["snippet"]["authorChannelId"]["value"],
            author_name=comment["snippet"]["authorDisplayName"],
            text=comment["snippet"]["textOriginal"],
            like_count=comment["snippet"]["likeCount"],
            parent_id=parent_id,
            published_at = comment["snippet"]["publishedAt"]
        )

    def _get_possible_names(self, tokenized_match_string):
        if not tokenized_match_string:
            return []
        else:
            return [' '.join(tokenized_match_string)[1:]] + self._get_possible_names(tokenized_match_string[:-1])

    def _find_name_in_thread(self, possible_names):
        for name in possible_names:
            if name in self.contributions.keys():
                return name
        return []

    def __eq__(self, o: object) -> bool:
        if self.video_id != o.video_id:
            return False
        for i, node in enumerate(self.nodes):
            if node != o.nodes[i]:
                return False
        return True
        
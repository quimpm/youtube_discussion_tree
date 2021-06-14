from ._xml import _serialize_tree
from ._viz import _print_graph
from .utils import Node
import re

class YoutubeDiscusionTree():

    def __init__(self, video_id, conflict_solving_algorithm):
        self.video_id = video_id
        self.conflict_solving_algorithm = conflict_solving_algorithm
        self.nodes = []
        self.contributions = {}

    def make_tree(self, root, comments):
        self.nodes.append(root)
        self._create_comment_nodes(comments, root)
        return self

    def serialize(self, filename, aditional_atributes=None):
        _serialize_tree(filename, self.nodes, aditional_atributes)

    def show(self):
        _print_graph(self.nodes)

    def _create_comment_nodes(self, comment_threads, root):
        for i, comment_thread in enumerate(comment_threads):
            self.nodes.append(self._new_node(comment_thread["snippet"]["topLevelComment"], root.id))
            if "replies" in comment_thread.keys():
                self._create_replies_nodes(list(reversed(comment_thread["replies"]["comments"])), self.nodes[-1].id)

    def _create_replies_nodes(self, replies, top_level_comment_id):
        for reply in replies:
            match = re.match('(@.{0,50} )', reply["snippet"]["textOriginal"])
            if match:
                possible_names = self._get_possible_names(match[0].split(" "))
                name = self._find_name_in_thread(possible_names, self.contributions)
                if not name:
                    curr_node = self._new_node(reply, top_level_comment_id)
                else:
                    curr_node = self._create_deep_replie_node(name, reply)
            else:
                curr_node = self._new_node(reply, top_level_comment_id)
            self.nodes.append(curr_node)
            self._actualize_contributions(reply, curr_node)

    def _create_deep_replie_node(self, name, reply):
        if len(self.contributions[name]) == 1:
            return Node(
                id=reply["id"],
                author_id=reply["snippet"]["authorChannelId"]["value"],
                author_name=reply["snippet"]["authorDisplayName"],
                text=reply["snippet"]["textOriginal"],
                like_count=reply["snippet"]["likeCount"],
                parent_id=self.contributions[name][0].id,
                published_at = reply["snippet"]["publishedAt"]
            )
        else:
            parent_id = self.conflict_solving_algorithm(Node(
                id=reply["id"],
                author_id=reply["snippet"]["authorChannelId"]["value"],
                author_name=reply["snippet"]["authorDisplayName"],
                text=reply["snippet"]["textOriginal"],
                like_count=reply["snippet"]["likeCount"],
                parent_id=None,
                published_at = reply["snippet"]["publishedAt"]
            ), self.contributions[name])
            return Node(
                id=reply["id"],
                author_id=reply["snippet"]["authorChannelId"]["value"],
                author_name=reply["snippet"]["authorDisplayName"],
                text=reply["snippet"]["textOriginal"],
                like_count=reply["snippet"]["likeCount"],
                parent_id=parent_id,
                published_at = reply["snippet"]["publishedAt"]
            )

    def _actualize_contributions(self, reply, curr_node):
        if reply["snippet"]["authorDisplayName"] in self.contributions.keys():
            self.contributions[reply["snippet"]["authorDisplayName"]].append(curr_node)
        else:
            self.contributions[reply["snippet"]["authorDisplayName"]] = [curr_node]

    def _new_node(self, top_level_comment, parent_id):
        return Node(
            id=top_level_comment["id"],
            author_id=top_level_comment["snippet"]["authorChannelId"]["value"],
            author_name=top_level_comment["snippet"]["authorDisplayName"],
            text=top_level_comment["snippet"]["textOriginal"],
            like_count=top_level_comment["snippet"]["likeCount"],
            parent_id=parent_id,
            published_at = top_level_comment["snippet"]["publishedAt"]
        )

    def _get_possible_names(self, match_string):
        if not match_string:
            return [" "]
        else:
            return [' '.join(match_string)[1:]] + self._get_possible_names(match_string[:-1])

    def _find_name_in_thread(self, possible_names, contributions):
        for name in possible_names:
            if name in contributions.keys():
                return name
        return []

    def __eq__(self, o: object) -> bool:
        if self.video_id != o.video_id:
            return False
        for i, node in self.nodes:
            if node != o.nodes[i]:
                return False
        return True
        
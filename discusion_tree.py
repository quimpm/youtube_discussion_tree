from youtube_discussion_tree import YoutubeDiscusionTreeAPI, YoutubeCommentTree
from youtube_discussion_tree import interactive_conflict_resolution

if __name__ == "__main__":
    api = YoutubeDiscusionTreeAPI("AIzaSyD-UjlHhqsZkhKKrDFp5PNaHyS6JHjLSUg")
    #tree = api.generate_tree("LnX3B9oaKzw", summarization=True)
    tree = api.generate_tree("9GHmfg54gg8", summarization=True, algorithm=interactive_conflict_resolution)
    #tree = api.generate_tree("Os0EBHBeciM", summarization=True)
    tree.serialize("output.xml")
    tree.show()
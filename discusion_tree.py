from youtube_discussion_tree import YoutubeDiscusionTreeAPI, YoutubeCommentTree
from youtube_discussion_tree import XMLSerializer

if __name__ == "__main__":
    api = YoutubeDiscusionTreeAPI("AIzaSyD-UjlHhqsZkhKKrDFp5PNaHyS6JHjLSUg")
    tree = api.generate_tree("9GHmfg54gg8")
    parser = XMLSerializer(tree, True)
    parser.serialize("output.xml")
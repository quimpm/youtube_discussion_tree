from youtube_discussion_tree import YoutubeDiscusionTreeAPI, YoutubeCommentTree

if __name__ == "__main__":
    api = YoutubeDiscusionTreeAPI("AIzaSyD-UjlHhqsZkhKKrDFp5PNaHyS6JHjLSUg")
    tree = api.generate_tree("LnX3B9oaKzw", summarization=True)
    tree.serialize("output.xml")
    tree.show()
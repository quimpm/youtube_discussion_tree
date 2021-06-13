from youtube_discussion_tree_api.utils import video
from youtube_discussion_tree_api import YoutubeDiscusionTreeAPI
from transformers import pipeline

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

def interactive_conflict_resolution(reply, contributions):
    print("\n" + bcolors.WARNING + "A CONFLICT was found:" + bcolors.ENDC)
    print(bcolors.OKGREEN + "To which of this comments:" + bcolors.ENDC)
    for i, comment in enumerate(contributions):
        print("\n" + bcolors.BOLD + str(i)+ " - " + bcolors.ENDC + bcolors.HEADER + "Author name: "+comment.author_name+", Author id: "+comment.author_id +" - Published at: "+ comment.published_at + bcolors.ENDC)
        print(bcolors.OKCYAN + comment.text + bcolors.ENDC)
    print("\n" + bcolors.OKGREEN + "Belongs the reply:" + bcolors.ENDC)
    print(bcolors.OKCYAN + "- "+reply.text + bcolors.ENDC)
    number = -1
    while number not in range(len(contributions)):
        try:
            number = int(input("\n" + bcolors.OKGREEN + "Enter the number of the comment: " + bcolors.ENDC))
        except:
            number = -1
    return contributions[number].id

def sentiment_analysis(node):
    sentiment_analysis = pipeline("sentiment-analysis")
    result = sentiment_analysis(node.text)[0]
    return {
        "sentiment" : result["label"],
        "sentiment_prob" : str(round(result["score"], 4))
    }

def additional_atributes(node):
    atributes = sentiment_analysis(node)
    atributes["hola"] = "que tal"
    return atributes

if __name__ == "__main__":
    api = YoutubeDiscusionTreeAPI("AIzaSyD-UjlHhqsZkhKKrDFp5PNaHyS6JHjLSUg")
    tree = api.generate_tree("LnX3B9oaKzw", summarization=True) #Aditionally, conflict solving algorithm can be passed
    tree.serialize("output.xml") #Aditional atributes can be added with a function that returns a dict key:value
    #print(api.quota_info())
    #videos = api.search_videos("Functional programming", 30)
    #print(videos[0])
    #print(len(videos))
    #print(api.quota_info())
    tree.show()
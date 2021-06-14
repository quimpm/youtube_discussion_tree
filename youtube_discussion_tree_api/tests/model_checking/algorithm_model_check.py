from youtube_discussion_tree_api import YoutubeDiscusionTreeAPI
from dotenv import dotenv_values
import pickle

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

def main():
    print("This is a supervised Model Correctness Algorithm for the automatic conflict solving algorithm.")
    MATCH_TREES = 0
    TOTAL_TREES = 50
    config = dotenv_values("../../.env")
    api = YoutubeDiscusionTreeAPI(config["API_KEY"])
    videos = api.search_videos("Functional programming", TOTAL_TREES)
    for i,video in enumerate(videos):
        auto_tree = api.generate_tree(video.id)
        inter_tree = api.generate_tree(video.id, conflict_solving_algorithm = interactive_conflict_resolution)
        if auto_tree == inter_tree:
            MATCH_TREES += 1
    print("Matching trees: "+str(MATCH_TREES)+"/"+str(TOTAL_TREES))
    print("Correctness percentage: "+str(MATCH_TREES/TOTAL_TREES*100))


if __name__ == "__main__":
    main()
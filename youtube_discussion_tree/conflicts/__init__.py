from ..utils import bcolors, Node
from ..text_similarity import guess_parent

def interactive_conflict_resolution(replie, contributions):
    print("\n" + bcolors.WARNING + "A CONFLICT was found:" + bcolors.ENDC)
    print(bcolors.OKGREEN + "To which of this comments:" + bcolors.ENDC)
    for i, comment in enumerate(contributions):
        print("\n" + bcolors.BOLD + str(i)+ " - " + bcolors.ENDC + bcolors.HEADER + "Author name: "+comment.author_name+", Author id: "+comment.author_id + bcolors.ENDC)
        print(bcolors.OKCYAN + comment.text + bcolors.ENDC)
    print("\n" + bcolors.OKGREEN + "Belongs the replie:" + bcolors.ENDC)
    print(bcolors.OKCYAN + "- "+replie["snippet"]["textOriginal"] + bcolors.ENDC)
    number = -1
    while number not in range(len(contributions)):
        try:
            number = int(input("\n" + bcolors.OKGREEN + "Enter the number of the comment: " + bcolors.ENDC))
        except:
            number = -1
    return contributions[number].id

def tf_itf_automatic_algorithm(replie, contributions):
    return guess_parent(Node(
        id = replie["id"],
        author_id = replie["snippet"]["authorChannelId"]["value"],
        author_name = replie["snippet"]["authorDisplayName"],
        text = replie["snippet"]["textOriginal"],
        likeCount = replie["snippet"]["likeCount"],
        parent_id = None
    ), contributions)
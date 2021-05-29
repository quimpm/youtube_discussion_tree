from youtube_discussion_tree import YoutubeDiscusionTreeAPI, YoutubeCommentTree

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

def interactive_conflict_resolution(replie, contributions):
    print("\n" + bcolors.WARNING + "A CONFLICT was found:" + bcolors.ENDC)
    print(bcolors.OKGREEN + "To which of this comments:" + bcolors.ENDC)
    for i, comment in enumerate(contributions):
        print("\n" + bcolors.BOLD + str(i)+ " - " + bcolors.ENDC + bcolors.HEADER + "Author name: "+comment.author_name+", Author id: "+comment.author_id + bcolors.ENDC)
        print(bcolors.OKCYAN + comment.text + bcolors.ENDC)
    print("\n" + bcolors.OKGREEN + "Belongs the replie:" + bcolors.ENDC)
    print(bcolors.OKCYAN + "- "+replie.text + bcolors.ENDC)
    number = -1
    while number not in range(len(contributions)):
        try:
            number = int(input("\n" + bcolors.OKGREEN + "Enter the number of the comment: " + bcolors.ENDC))
        except:
            number = -1
    return contributions[number].id

if __name__ == "__main__":
    api = YoutubeDiscusionTreeAPI("AIzaSyD-UjlHhqsZkhKKrDFp5PNaHyS6JHjLSUg")
    """
        Opcións de Generació:
            * Summarització del contingut del video
            * Triar algoritme (Pot ser pròpi o el per defecte de la llibreria)
    """
    tree = api.generate_tree("LnX3B9oaKzw", summarization=True)
    #tree = api.generate_tree("9GHmfg54gg8", summarization=True, conflict_solving_algorithm=interactive_conflict_resolution)
    #tree = api.generate_tree("Os0EBHBeciM", summarization=True)
    """
        Hi ha l'opció de fer l'anàlisi de sentiment i afegir-ho al arbre al serialitzar (Intentar liftejaro a una HOF per a que puguin ficar els valors que vulguin)
    """
    #tree.serialize("output.xml", True)
    tree.serialize("output.xml", True)
    tree.show()
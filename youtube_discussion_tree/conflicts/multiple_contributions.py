from ..utils import bcolors

def interactive_multiple_contributions_conflict(name, replie, contributions, id_user):
    print("\n" + bcolors.WARNING + "A CONFLICT was found:" + bcolors.ENDC)
    print(bcolors.OKGREEN + "To which of this comments:" + bcolors.ENDC)
    for i, comment in enumerate(contributions[name][id_user]):
        print("\n" + bcolors.BOLD + str(i) + bcolors.ENDC + bcolors.OKCYAN + " - "+comment.text + bcolors.ENDC)
    print("\n" + bcolors.OKGREEN + "Belongs the replie:" + bcolors.ENDC)
    print(bcolors.OKCYAN + "- "+replie["snippet"]["textOriginal"] + bcolors.ENDC)
    number = -1
    while number not in range(len(contributions[name][id_user])):
        try:
            number = int(input("\n" + bcolors.OKGREEN + "Enter the number of the comment: " + bcolors.ENDC))
        except:
            number = -1
    return number

def automatic_multiple_contributions_conflict():
    pass
from ..utils import bcolors

def interactive_same_username_conflict(name, replie, contributions):
    print("\n" + bcolors.WARNING + "A CONFLICT was found:" + bcolors.ENDC)
    print(bcolors.OKGREEN + "Found some users with same username in a comment thread: "+ name + bcolors.ENDC)
    print(bcolors.OKGREEN + "To which of this users it belongs the comment that the reply refers to:" + bcolors.ENDC)
    for id_user in contributions[name].keys():
        if id_user != replie["snippet"]["authorChannelId"]["value"]:
            print("\n- "+id_user)
            for i,comment in enumerate(contributions[name][id_user]):
                print(bcolors.BOLD + str(i) + bcolors.ENDC + bcolors.OKCYAN + " - "+comment.text + bcolors.ENDC + "\n")
    print("\n" + bcolors.OKGREEN + "It belongs the replie:" + bcolors.ENDC)
    print(bcolors.OKCYAN + "- "+replie["snippet"]["textOriginal"] + bcolors.ENDC)
    id_user = ""
    while id_user not in contributions[name].keys():
        id_user = input("\n" + bcolors.OKGREEN + "Enter the id of the user: " + bcolors.ENDC)
    return id_user

def automatic_same_username_conflict(name, replie, contributions):
    pass

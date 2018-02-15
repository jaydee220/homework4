import networkx as nwx
import progressbar
import json
import os

bar = progressbar.ProgressBar()

def load_words(filename):
    #Function is loading the data from a JSON Formatted file into the application in the examples case the output will be a dictionary.
    # the format of the output will be given by the input file.
    try:
        with open(filename,"r") as english_dictionary:
            valid_words = json.load(english_dictionary)
            return valid_words
    except Exception as e:
        return str(e)

def map_network(dict_file):
    #this is the function responsible for the whole network, while giving as an attribute the length of each node (important for ex. 1)
    # it is comparing the previous list of neighbors (generated in the gen_possible_neighbors) checking which words are in the same "neighborhood" and according to it making all the edges[connections] in the network
    #the output of this function is the completed network.
    network = nwx.Graph()
    used_dict = load_words(dict_file)
    city = {}
    for word in bar(used_dict):
        network.add_node(word, length=len(word))
        for neighbors in gen_possible_neighbors(word):
            if neighbors in city:
                e=[]
                for neighbor in city[neighbors]:
                    e.append(tuple((word,neighbor)))
                    e.append(tuple((neighbor,word)))
                network.add_edges_from(e)
                city[neighbors].append(word)
            else:
                city[neighbors] = [word]
    print("Network created, export to file begins (might take a few minutes...)")
    return network



def gen_possible_neighbors(word):
    #this function generates a list of all possible subwords that could be connected with the entered word (i.E.:
    #input word is test --> [*test, t*est, te*st, tes*t, test*, *est, t*st, te*t, tes*]
    #this function is essential to assign the right "neighbors" to a word and add the edges from one node to another correctly
    possible_neighbors = []
    possible_neighbors.append("*"+word)
    for b in range(len(word)):
        possible_neighbors.append(word[:b] + "*" + word[b + 1:])
        possible_neighbors.append(word[:b + 1] + "*" + word[b + 1:])
    return possible_neighbors


def yes_no(answer):
    #simple yes/no answer function for user with default set to Y
    yes = set(['yes', 'y', 'ye', '','aye'])
    no = set(['no', 'n','nay', 'nah'])

    while True:
        selection = input(answer).lower()
        if selection in yes:
            return True
        elif selection in no:
            return False
        else:
            print
            "Please respond with 'yes' or 'no'\n"

def export_gexf():
    words = input("Enter name of dictionary to export (E.g. words_dictionary):")
    if os.path.isfile(os.getcwd()+"/"+words+".gexf") == True:
        ovrwrite = yes_no("file already exists, overwrite Y/N (Default Y):")
        if ovrwrite == False:
            return print("Existing file will be used")
    print("Wordnetwork is being being created...")
    nwx.write_gexf(map_network(words+".json"), words+".gexf")

def export_pickle():
    words = input("Enter filename of dictionary to export (E.g. words_dictionary):")
    if os.path.isfile(os.getcwd() + "/" + words + ".pickle") == True:
        ovrwrite = yes_no("file already exists, overwrite Y/N (Default Y):")
        if ovrwrite == False:
            return print("Existing file will be used")
    print("Wordnetwork is being being created...")
    nwx.write_gpickle(map_network(words + ".json"), words + ".pickle")

def run_trail(start, end, method="ex2"):
    #Part1: Load the words into the network
    network = None
    use_existing = yes_no("Do you want to load an existing network out of a pickle?")
    if use_existing == True:
        fname = input("enter the name of the .pickle file you want to use (whole filename):")
        try:
            network = nwx.read_gpickle(fname)
            print ("Network successfully loaded!")
        except Exception as e:
            print ("Load of network failed")
    if network == None:
        fname = input("Enter filename of dictionary (E.g. words_dictionary):")
        network = map_network(fname + ".json")
    if method == "ex1":
        #for exercise one we filter the network for only values that have the same lenght attribute. it is done with a subgraph
        if len(start)==len(end):
            network = network.subgraph([n for n, attrdict in network.node.items() if ("length", len(start)) in attrdict.items()])
        else:
            return print("Words are not in the same length, please select method 'ex2' for comparing words of unequal length")
        #Part2: getting the shortest path between the source word and the end word and saving it into a list
    try:
        outlst = nwx.shortest_path(network,source=start,target=end)
    except nwx.NetworkXNoPath :
        return print("No path between '"+start+"' and '"+end+"' found :'-(")
    except nwx.NodeNotFound:
        return print ("One of the words selected can not be found in the dictionary, please try something else")
    #Part3: formatting the output to be as given in the exercise description
    print("Transformation from "+start+" to "+end+" can be made with following path:")
    print(" --> ".join(outlst))


if __name__ == '__main__':
    run_trail("elephant","animalic")
    # export_gexf()
    # g = nwx.read_gpickle("words_dictionary.pickle")
    # #g = map_network("words_dictionary_ger.json")
    # sg = g.subgraph([n for n, attrdict in g.node.items() if ("length", 4) in attrdict.items()])
    # print (nwx.shortest_path(sg,source="head", target="tail"))


#

import sys
import pprint
from visualization import *
from help_calculate import *
from total_possibilities import *
from moves_FS import *

def comparevalues(nmax, kmax):
    """
    print all possibility values for bruteforceadjustedUpsilon and adjustedUpsilon with 0<disks<nmax+1 and 2<pegs<kmax+1
    """
    print("bruteforceadjustedpossibilities:adjustedpossibilities")
    for k in range(4,kmax+1):
        print(k,end=" ")
        for n in range(1,nmax+1):
            print(bruteforceadjustedUpsilon(n,k), end = ":")
            print(adjustedUpsilon(n,k), end = "|")
        print("")

if __name__ == "__main__":
    disks = int(sys.argv[1])
    pegs = int(sys.argv[2])
    ##compare bruteforceadjustedUpsilon and adjustedUpsilon
    #comparevalues(disks, pegs)


    ###visualize function
    ##visualize one configuration given as configurationdict
    #configurationdict = {0:[5], 1:[2,3,4], 2:[0,1], 3:[]}
    #visualize({"config":configurationdict})

    ##visualize a movelist in the form movelist = [move1, move2, ...] where one move is a list [disk, start, end]
    #movelist = movessequence_ui(disks, pegs)[0]
    #visualize({"movelist":[disks, pegs, movelist]})

    ##visualize and compare different movelists in the form movelists = [movelist1, movelist2, ...]
    #movelists = movessequence_ui(disks, pegs)
    #visualize({"movelists":[disks, pegs, movelists]})

    ##visualize a list of configurations
    #listofconfigs = [{0:[5], 1:[2,3,4], 2:[0,1], 3:[]}, {0:[], 1:[2,3,4], 2:[0,1], 3:[5]}]
    #visualize({"list":listofconfigs})

    ##visualize a dict of configurations in the form configurationsdict = {1:[config1,...], 2:[config2,...],...}
    #configurationsdict =  {1:[{0:[5], 1:[2,3,4], 2:[0,1], 3:[]}, {0:[5], 1:[3,4], 2:[0,1,2], 3:[]}], 2:[{0:[], 1:[2,3,4], 2:[0,1], 3:[5]}, {0:[], 1:[3,4], 2:[0,1,2], 3:[5]}]}
    #visualize({"configurations":configurationsdict})

    ##get a pdf with a table of n and k containing the number of moves, the increment, the number of total possibilities, the number of possibilities with the FS-algorithm according to our adjusted recursive function or the number of possibilities with the FS-algorithm according to our bruteforceadjustedUpsilon function.
    ##Look up the suiting description in the docstring of visualization.visualize
    #visualize("description":[disks,pegs])

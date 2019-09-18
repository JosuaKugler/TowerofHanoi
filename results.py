import sys
import pprint
from visualization import *
from help_calculate import *
from total_possibilities import *
from moves_FS import *

def comparevalues(nmax, kmax):
    """
    print all possibility values for totalpossibilities and adjustedUpsilon with 0<disks<nmax+1 and 2<pegs<kmax+1
    """
    print("bruteforceadjustedpossibilities:adjustedpossibilities")
    for k in range(4,kmax+1):
        print(k,end=" ")
        for n in range(1,nmax+1):
            print(bruteforceadjustedUpsilon(n,k), end = ":")
            print(adjustedUpsilon(n,k), end = "|")
        print("")

def function1(disks, pegs):
    success_instances = bruteforce(disks, pegs)
    moves = []
    for instance in success_instances:
        moves.append(createmoves(instance))
    #moves = movessequence_ui(disks, pegs)
    visualize({'movelists': [disks, pegs, moves]})

def function2(disks, pegs):
    moves = movessequence_ui(disks, pegs)
    visualize({'movelists': [disks, pegs, moves]})

if __name__ == "__main__":
    disks = int(sys.argv[1])
    pegs = int(sys.argv[2])
    function2(disks, pegs)
    #comparevalues(disks, pegs)

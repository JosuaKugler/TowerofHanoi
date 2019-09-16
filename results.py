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
    print("totalpossibilities:adjustedpossibilities")
    for k in range(3,kmax+1):
        print(k,end=" ")
        for n in range(1,nmax+1):
            print(totalpossibilities(n,k), end = ":")
            print(adjustedUpsilon(n,k), end = "|")
        print("")


if __name__ == "__main__":
    disks = int(sys.argv[1])
    pegs = int(sys.argv[2])
    moves = movessequence_ui(disks, pegs)
    ST = TH(disks, pegs)
    print(moves)
    for movelist in moves:
        ST.move(movelist)
    #print(ST.history)
    #visualize(('list', ST.history))
    #success_instances = bruteforce(disks, pegs)
    #visualize(('list', success_instances[0].history))
    #print(success_instances[0])

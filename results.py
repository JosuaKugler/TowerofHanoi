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

def comparehs(THs, show = True):
    """
    compare the history of a list of THobjects
    !important: only pass THobject with same length of history
    """
    M = len(THs[0].history)
    if show:
        historylist = []
        movedict = {}
        for m in range(0,M):
            movedict[m] = []
        for th in THs:
            movecounter = -1
            for config in th.history:
                movecounter += 1
                movedict[movecounter].append(normalize(th.disks, th.pegs, config))
        #movedict[n] contains the normalizedconfigurations of all THobjects in THs after n moves
        pprint.pprint(movedict)
    different = {}
    for th1 in THs:
        for th2 in THs:
            if th1 != th2:
                for movenumber in range(M):
                    th1config = normalize(th1.disks, th1.pegs, th1.history[movenumber])
                    th2config = normalize(th2.disks, th2.pegs, th2.history[movenumber])
                    try:
                        value = different[th1][th2]
                    except:
                        #only the first time
                        different[th1] = {}
                        different[th1][th2] = 0
                    if th1config != th2config:
                        different[th1][th2] = 1
    return different

if __name__ == "__main__":
    disks = int(sys.argv[1])
    pegs = int(sys.argv[2])
    movepossibilities = movessequence_ui(disks, pegs)
    #print(moves)
    thlist = []
    for movelist in movepossibilities:
        ST = TH(disks, pegs)
        thlist.append(ST)
        for move1 in movelist:
            ST.move(move1)
    different = comparehs(thlist, show = True)
    print(different)
    #print(ST.history)
    #visualize(('list', ST.history))
    #success_instances = bruteforce(disks, pegs)
    #visualize(('list', success_instances[0].history))
    #print(success_instances[0])

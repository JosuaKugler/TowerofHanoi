from help_calculate import bk
from total_possibilities import *
import copy

configurations = {}# a dict with the number of moves as key and a list of interesting configurations that can be reached within the number of moves
success_instances = [] # a list with all instances that reached the finished state

def movessequence(startpeg, endpeg, disklist, peglist):
    """
    returns a list of possible movessequences
    that lead to the solution of the problem within the minimum number of moves
    sometimes there are still equal movessequences
    """
    #rint("The disks {} have to be moved from {} to {}, using pegs {}".format(disklist,startpeg,endpeg,peglist))
    #if there is only one disk left, there is only one possible move
    if len(disklist)==1:
        move = [disklist[0],startpeg,endpeg]
        movelist = [move]
        return [movelist]

    else:
        #compute all possible pegheights for the intermediate towers
        pegheights = calculatemiddletower(startpeg,endpeg,disklist,peglist)
        resultlist = []
        for pegheight in pegheights:
            #rint("use", pegheight)
            #compute movesequencelist for building the intermediate towers
            movesequencedict = {}
            peglist2 = peglist.copy()
            disklist2 = disklist.copy()
            #build one intermediate tower after the other
            for peg in peglist:
                height = pegheight[peg]
                if height!=0:
                    movingdisks = disklist2[:height]
                    #contains all possible movessequences to move movingdisks from startpeg to peg
                    movesequencedict[peg] = movessequence(startpeg,peg,movingdisks,peglist2)
                    peglist2.remove(peg)
                    disklist2 = disklist2[height:]

            #construct individual movessequences from movesequencedict
            np = 0
            movesequenceleveldict = {} #contains all possible movessequences until this peg
            level = 0
            for peg in movesequencedict:
                level += 1
                movesequenceleveldict[level] = []
                for addmovessequence in movesequencedict[peg]:#addmovessequence builds the intermediate tower on peg
                    if level > 1:
                        #lowerlevellist is a list of all movessequences that have been created before
                        lowerlevellist = movesequenceleveldict[level-1]
                        for oldmovessequence in lowerlevellist:#oldmovessequence is one of the movessequences that create everything before the peg
                            newmovessequence = oldmovessequence + addmovessequence
                            movesequenceleveldict[level].append(newmovessequence)
                    else:#first peg, level 1
                        movesequenceleveldict[level].append(addmovessequence)
            finalmovessequences = movesequenceleveldict[level]#level has the max value

            #construct the rest of the movessequences

            for movesequence in finalmovessequences:
                lastmoves = []
                for i in range(1,len(movesequence)+1):
                    #iterates from len(firstmoves)-1 to 0
                    currentmove = movesequence[len(movesequence)-i]
                    #tauschen von start und endpeg
                    if currentmove[1]==startpeg:
                        peg2 = endpeg
                    elif currentmove[1]==endpeg:
                        peg2 = startpeg
                    else:
                        peg2 = currentmove[1]
                    if currentmove[2]==startpeg:
                        peg1 = endpeg
                    elif currentmove[2]==endpeg:
                        peg1 = startpeg
                    else:
                        peg1 = currentmove[2]
                    newcurrentmove = [currentmove[0],peg1,peg2]
                    lastmoves.append(newcurrentmove)
                result = movesequence[:]+[[disklist[-1],startpeg,endpeg]]+lastmoves[:]
                resultlist.append(result)
        return resultlist


def calculatemiddletower(startpeg,endpeg,disklist,peglist):
    """
    returns all possible dicts with pegs as keys and the height this peg is supposed to have as item.
    discussion: what does 'all possible' mean?
    basically, dicts with the same heights in a different order should lead to the same moves.
    But, as the movesequence function places the first disks on the first peg it encounters in the dict,
    the order can indeed matter.
    Fact: There are equal movesequences if the order is allowed to matter.
    There are no equal movessequences if pegheightdicts with the same heights
    in a different order are not allowed to matter.
    However, there are more different possibilities with the first method if the equal possibilities are removed afterwards.
    """
    #rint("calculatemiddletower startpeg =", startpeg, ", endpeg =", endpeg, "\nuse disks", disklist, "\nuse pegs", peglist)
    m = len(peglist); As = len(disklist); mmpegdict = {}
    n = 0
    x = 1
    while As > x:
        n+=1
        x = bk(n+m-2,m-2)
    #rint(As,n)
    #berechnen der minimalen und maximalen Hoehe eines Zwischenturms
    i = 0
    for peg in peglist:
        if peg == startpeg or peg == endpeg:
            mmpegdict[peg]=[0,0]
        else:
            mmpegdict[peg]=[int(bk(n+m-i-4,m-i-2)),int(bk(n+m-i-3,m-i-2))]
            i+=1

    #im Fall von einer Scheibe stimmt die minimale Hoehe nicht
    for peg in mmpegdict:
        if mmpegdict[peg][1]==1:
            mmpegdict[peg][0]=0

    #berechnen der abzueglichen Scheibenzahl fuer nicht-inkrementgrenzfaelle
    knowndisks = int(bk(n+m-2,m-2))
    toomuchdisks = knowndisks-As
    pegheightdict = {}
    if False:
        takenallaway = False #true if all unnecessary disks are removed
        #find one variant
        for peg in peglist:
            min_value = mmpegdict[peg][0]
            max_value = mmpegdict[peg][1]
            difference = max_value-min_value
            toomuchdisks -= difference
            if takenallaway:
                pegheightdict[peg]=max_value
            elif toomuchdisks >= 0:
                pegheightdict[peg]=min_value
            else:
                pegheightdict[peg] = max_value-toomuchdisks-difference
                takenallaway = True
        differentpegheights = [pegheightdict]
    else:
        notassigned = peglist.copy()
        notassigned.reverse()
        #rint("assignpegheights(", notassigned, pegheightdict, As, mmpegdict, ")")
        pegheights = assignpegheights(notassigned, pegheightdict, As, mmpegdict)
        if False:
            #two pegheights are different if two pegs are switched.
            differentpegheights = []
            differentheights = []
            for pegheight in pegheights:#pegheight is a dict with pegs and number coding for the heigths
                new = True
                thisheight = []
                for height in pegheight:
                    thisheight.append(pegheight[height])
                thisheight.sort()
                for height in differentheights:
                    if height == thisheight:
                        new = False
                        break
                if new:
                    differentpegheights.append(pegheight)
                    differentheights.append(thisheight)
        else:
            differentpegheights = pegheights
    return differentpegheights

def assignpegheights(notassigned, pegheightdict, totaldisks, mmpegdict):
    """
    find all pegheightdicts recursively

    notassigned is a list of pegs without assigned height
    pegheightdict is the dict where the current heights are saved
    remaining is the number of disks that are not assigned to a peg by now
    mmpegdict is the dict with the minimum and maximum height that can be assigned to a peg
    """
    disknumber = 0
    for peg in pegheightdict:
        disknumber += pegheightdict[peg]
    remaining = totaldisks - disknumber -1
    #rint(remaining, "=", totaldisks, "-", disknumber)

    if len(notassigned) == 0 and remaining == 0:
        #all disks are assigned to a peg
        space = "   "*(len(pegheightdict)+1)
        #rint(space, "done:", pegheightdict)
        return [pegheightdict]
    else:
        #there is a peg that needs to get a number of disks assigned
        peg = notassigned.pop()
        space = "   "*peg
        minimum = mmpegdict[peg][0]
        maximum = mmpegdict[peg][1]
        #sum of all possibly storable disks for all not yet assigned pegs
        maxsum = 0
        minsum = 0
        for ipeg in notassigned:
            maxsum += mmpegdict[ipeg][1]
            minsum += mmpegdict[ipeg][0]
        pegheights = []
        lower = max(minimum, remaining-maxsum)
        upper = min(maximum, remaining-minsum)
        #rint(space, "peg", peg, "remaining", remaining, pegheightdict)
        #rint(space, "range:", lower, upper)
        for pegheight in range(lower, upper+1):
            #rint(space, peg, " has pegheight", pegheight, "while remaining is", remaining)
            if remaining-pegheight >= 0:
                pegheightdict[peg] = pegheight
                a = assignpegheights(notassigned.copy(), copy.deepcopy(pegheightdict), totaldisks, mmpegdict)
                for i in a:
                    pegheights.append(i)
        return pegheights

def isequal(th1, th2):
    """
    returns True if the history of th1 and th2 is equivalent
    """
    equal = True
    for config1, config2 in zip(th1.history, th2.history):
        if normalize(th1.disks, th1.pegs, config1) != normalize(th2.disks, th2.pegs, config2):
            equal = False
    return equal


def removeequals(disks, pegs, movepossibilities, show = False):
    """
    removes all equal movessequences from movepossibilities
    and returns a list without the equal movessequences
    """
    thlist = []
    for movelist in movepossibilities:
        ST = TH(disks, pegs)
        thlist.append(ST)
        for move1 in movelist:
            ST.move(move1)
    equallists = []
    for n,th1 in enumerate(thlist):
        for th2 in thlist[n:]:
            if th1 != th2:
                if isequal(th1, th2):
                    exists = False
                    for equallist in equallists:
                        if th1 in equallist:
                            exists = True
                            if th2 not in equallist:
                                equallist.append(th2)
                        elif th2 in equallist:
                            exists = True
                            if th1 not in equallist:
                                equallist.append(th1)
                    if not exists:
                        equallists.append([th1, th2])
    if show:
        for equallist in equallists:
            string = str(equallist[0].id)
            for th in equallist[1:]:
                string += "=" + str(th.id)
            print(string)
    for th in thlist:
        unique = True
        for equallist in equallists:
            if th in equallist:
                unique = False
        if unique:
            equallists.append([th])
    newmovepossibilities = []
    for equallist in equallists:
        newmovepossibilities.append(equallist[0])
    return newmovepossibilities

def movessequence_ui(n,k):
    peglist=[];disklist=[]
    for i in range(k):
        peglist.append(i)
    for i in range(n):
        disklist.append(i)
    ST = TH(n,k)
    configurations[0] = [ST]
    moves = movessequence(peglist[0],peglist[-1],disklist,peglist)
    thmoves = removeequals(n, k, moves)
    moves = []
    for th in thmoves:
        moves.append(createmoves(th))
    return moves

def bruteforceadjustedUpsilon(n, k):
    moves = movessequence_ui(n,k)
    return len(moves)

# IDEA: write a calculatemiddletower function that returns all possible pegheightdicts.
#Then use movessequence method on each of them.
#Somehow use structure from totalpossibilities with TH objects.
# NOTE: bigger number, bigger disk
from help_calculate import bk
from total_possibilities import *
import copy

configurations = {}# a dict with the number of moves as key and a list of interesting configurations that can be reached within the number of moves
success_instances = [] # a list with all instances that reached the finished state

def movessequence(startpeg, endpeg, disklist, peglist):
    """gibt alle benoetigten Zuege zurueck"""
    print("Die Scheiben {} sollen unter Benutzung der Felder {} von {} nach {} bewegt werden".format(disklist,peglist,startpeg,endpeg))
    #print(disklist)
    #spezialfaelle
    if len(disklist)==1:
        #print("es bleibt nur eine Scheibe zum bewegen",disklist[0],startpeg,endpeg)
        return [[disklist[0],startpeg,endpeg]]

    else:
        #zwischenturmhoehe berechnen
        pegheights = calculatemiddletower(startpeg,endpeg,disklist,peglist)
        pegheight = pegheights[0]
        print("use", pegheight)
        #dann die movessequencelist fuer die Zwischentuerme berechnen
        movesequencelist = []
        #bewege einen Zwischenturm nach dem anderen
        peglist2 = peglist.copy()
        disklist2 = disklist.copy()
        for peg in peglist:
            height = pegheight[peg]
            if height!=0:
                movingdisks = disklist2[:height]
                movesequencelist += movessequence(startpeg,peg,movingdisks,peglist2)
                peglist2.remove(peg)
                disklist2 = disklist2[height:]

        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        lastmoves = []
        for i in range(1,len(movesequencelist)+1):
            #iterates from len(firstmoves)-1 to 0
            currentmove = movesequencelist[len(movesequencelist)-i]
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

        return movesequencelist[:]+[[disklist[-1],startpeg,endpeg]]+lastmoves[:]

def calculatemiddletower(startpeg,endpeg,disklist,peglist):
    """berechnet die Hoehe der Zwischentuerme und gibt ein dict mit dem Zwischenturm als key und der hoehe als wert aus"""
    print("calculatemiddletower startpeg =", startpeg, ", endpeg =", endpeg, "\nuse disks", disklist, "\nuse pegs", peglist)
    m = len(peglist); As = len(disklist); mmpegdict = {}
    n = 0
    x = 1
    while As > x:
        n+=1
        x = bk(n+m-2,m-2)
    #print(As,n)
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
        pegheights = [pegheightdict]
    else:
        notassigned = peglist.copy()
        notassigned.reverse()
        #print("assignpegheights(", notassigned, pegheightdict, As, mmpegdict, ")")
        pegheights = assignpegheights(notassigned, pegheightdict, As, mmpegdict)
    return pegheights

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
    #print(remaining, "=", totaldisks, "-", disknumber)

    if len(notassigned) == 0 and remaining == 0:
        #all disks are assigned to a peg
        space = "   "*(len(pegheightdict)+1)
        print(space, "done:", pegheightdict)
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
        #print(space, "peg", peg, "remaining", remaining, pegheightdict)
        #print(space, "range:", lower, upper)
        for pegheight in range(lower, upper+1):
            #print(space, peg, " has pegheight", pegheight, "while remaining is", remaining)
            if remaining-pegheight >= 0:
                pegheightdict[peg] = pegheight
                a = assignpegheights(notassigned.copy(), copy.deepcopy(pegheightdict), totaldisks, mmpegdict)
                for i in a:
                    pegheights.append(i)
        return pegheights

def movessequence_ui(n,k):
    peglist=[];disklist=[]
    for i in range(k):
        peglist.append(i)
    for i in range(n):
        disklist.append(i)
    ST = TH(n,k)
    configurations[0] = [ST]
    moves = movessequence(peglist[0],peglist[-1],disklist,peglist)
    #print(moves, len(moves))
    return moves



print(movessequence_ui(5,5))

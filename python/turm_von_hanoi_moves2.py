# -*- coding: utf-8 -*-
def fak(x):
    """berechnet die Fakultaet von x"""
    if x == 0:
        return 1
    Ende = x
    x -= 1
    while x > 0:
        Ende = Ende * x
        x -= 1
    return Ende

def BK(n,k):
    """berechnet den Binomialkoeffizienten n ueber k"""
    x = (fak(n))/(fak(k)*fak(n-k))
    return x
    
def movessequence(startpeg, endpeg, disklist, peglist):
    """gibt alle benoetigten Zuege zurueck"""
    #print("Die Scheiben {} sollen unter Benutzung der Felder {} von {} nach {} bewegt werden".format(disklist,peglist,startpeg,endpeg))
    #print(disklist)
    #spezialfaelle
    if len(disklist)==1:
        #print("es bleibt nur eine Scheibe zum bewegen",disklist[0],startpeg,endpeg)
        return [[disklist[0],startpeg,endpeg]]

    else:
        #zwischenturmhoehe berechnen
        pegheight = calculatemiddletower(startpeg,endpeg,disklist,peglist)
        #dann die movessequencelist fuer die Zwischentuerme berechnen
        movesequencelist = []
        #bewege einen Zwischenturm nach dem anderen
        peglist2 = peglist.copy() 
        disklist2 = disklist.copy()
        for peg in peglist:
            height = pegheight[peg]
            if height!=0:
                #print("aktuell bearbeiteter Zwischenturmpeg:",peg,"in Rekursionstiefe",n_recursion)
                movingdisks = disklist2[-height:]
                #print(movingdisks)
                movesequencelist += movessequence(startpeg,peg,movingdisks,peglist2)
                peglist2.remove(peg)
                disklist2 = disklist2[:-height]

        
        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        
        #danach die groesste Scheibe
        #print("groesste Scheibe:",[disklist[0],startpeg,endpeg])
        #dann rueckwaerts
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
            
        return movesequencelist[:]+[[disklist[0],startpeg,endpeg]]+lastmoves[:]
        
def calculatemiddletower(startpeg,endpeg,disklist,peglist):
    """berechnet die Hoehe der Zwischentuerme und gibt ein dict mit dem Zwischenturm als key und der hoehe als wert aus"""
    m = len(peglist); As = len(disklist); mmpegdict = {}
    n = 0
    x = 1
    while As > x:
        n+=1
        x = BK(n+m-2,m-2)
    
    #print(As,n)
    #berechnen der minimalen und maximalen Hoehe eines Zwischenturms
    i = 0
    for peg in peglist:
        if peg == startpeg or peg == endpeg:
            mmpegdict[peg]=[0,0]
        else:
            mmpegdict[peg]=[int(BK(n+m-i-4,m-i-2)),int(BK(n+m-i-3,m-i-2))]
            i+=1
            
    #im Fall von einer Scheibe stimmt die minimale Hoehe nicht
    for peg in mmpegdict:
        if mmpegdict[peg][1]==1:
            mmpegdict[peg][0]=0

    #berechnen der abzueglichen Scheibenzahl fuer nicht-inkrementgrenzfaelle
    knowndisks = int(BK(n+m-2,m-2))
    toomuchdisks = knowndisks-As
    pegheightdict = {}
    #wegnehmen von der pegheigthdisklist
    takenallaway = False #true wenn alle ueberfluessigen Scheiben weggenommen sind
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
    return pegheightdict

def movessequence_ui(n,k):
    peglist=[];disklist=[]
    for i in range(k):
        peglist.append(i)
    for i in range(n):
        disklist.append(i)
    moves = movessequence(peglist[0],peglist[-1],disklist,peglist)
    #print(moves, len(moves))
    return moves

#print(calculatemiddletower(0,4,[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4]))
print(movessequence_ui(2,3))
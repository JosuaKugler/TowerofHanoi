# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:35:05 2019

@author: DELL
"""
from turm_von_hanoi_modul import n_moves

class Configuration():
    def __init__(self,n_pegs,n_disks):
        self.peglist = []
        for peg in range(n_pegs):
            self.peglist.append(peg)
        self.disklist = []
        for disk in range(n_disks):
            self.disklist.append(disk)
        self.pegdict = {}
        for peg in self.peglist:
            if peg == self.peglist[0]:
                disklist2=[]
                for i in self.disklist:
                    disklist2.append(i)
                self.pegdict[peg] = disklist2
            else:
                self.pegdict[peg]=[]
                
    def move(self, move):
        disk = move[0]; startpeg = move[1]; endpeg = move[2]
        self.pegdict[startpeg].remove(disk)
        self.pegdict[endpeg].append(disk)  
        print("aktueller Zustand:",self.pegdict)
    
    def data(self):
        self.n_pegs = len(self.peglist)
        self.n_disks = len(self.disklist)
        self.n_moves = n_moves(self.n_pegs,self.n_disks)
        self.moves = self.movessequence()
        self.n_moves2 = len(self.moves)
    
    def printoutdata(self):
        self.data()
        print("""Die Konfiguration besitzt {} Felder und {} Scheiben. 
              Laut unserer Formel benötigt sie {} Züge, um gelöst zu werden.
              Das Programm benötigt {} Züge und zwar folgende:
              {}""".format(self.n_pegs,self.n_disks,int(self.n_moves),self.n_moves2,self.moves))

    def threemovessequence(self, startpeg, endpeg, disklist, peglist):
        """gibt eine Liste mit allen benötigten moves zurück
        dabei ist disklist eine Liste aller scheiben mit der größten zuerst,
        peglist eine Liste der Felder
        startpeg das Feld auf dem alle Scheiben zu Beginn sind und
        endpeg das Feld auf das alle Scheiben sollen"""
        if len(peglist)<3:
            #print("weniger als 3 Plätze")
            return []
        if len(disklist)==1:
            self.move([disklist[0],startpeg,endpeg])
            return [[disklist[0],startpeg,endpeg]]
        else:
            for peg in peglist:
                if peg!=startpeg and peg!=endpeg:
                    notendpeg = peg
                    break
            firstmoves = self.threemovessequence(startpeg,notendpeg,disklist[1:],peglist)
            lastmoves = self.threemovessequence(notendpeg,endpeg,disklist[1:],peglist)
            #print("züge durch 3 Felder",firstmoves[:]+[[disklist[0],startpeg,endpeg]]+lastmoves[:])
            self.move([disklist[0],startpeg,endpeg])
            return firstmoves[:]+[[disklist[0],startpeg,endpeg]]+lastmoves[:]
    
    def halfmovessequence(self, startpeg,endpeg, disklist=None, peglist=None,n_recursion=0):
        """gibt die Züge bis zum Umschichten der größten Scheibe zurück"""
        if disklist == None:
            disklist = self.disklist
        if peglist == None:
            peglist = self.peglist
        #print("halfmovessequence",n_recursion,disklist,peglist,"startpeg",startpeg,"endpeg",endpeg)
        n_disks = len(disklist)
        n_pegs = len(peglist)
        if n_disks == 1:
            return []
        elif n_pegs==3:
            #print("problem für 3 Felder")
            for peg in peglist:
                if peg != startpeg and peg != endpeg:
                    middlepeg = peg
                    break
            return self.threemovessequence(startpeg,middlepeg, disklist[1:],peglist)
        else:
            #höhe des ersten Zwischenturms ist x1
            for i in range(int((n_disks-1)/(n_pegs-2)),n_disks):
                if 2*n_moves(n_pegs,i)+n_moves(n_pegs-1,n_disks-i) == n_moves(n_pegs, n_disks):
                    x1 = i
            #print("höhe des ersten Zwischenturms",x1)
            #peg für den ersten Zwischenturm
            for peg in peglist:
                if peg != startpeg and peg != endpeg:
                    middlepeg = peg
                    break
            #print("scheiben im ersten zwischenturm",disklist[n_disks-x1:])
            firstmoves = self.movessequence(startpeg, middlepeg, disklist[n_disks-x1:], peglist, n_recursion+1)
            #print("firstmoves half, also der erste Zwischenturm",firstmoves)
            #peglist ohne den middlepeg
            newpeglist=[]
            for peg in self.pegdict:
                newpeglist.append(peg)
                if len(self.pegdict[peg])!=0 and peg != startpeg:
                    newpeglist.remove(peg)
            secondmoves = self.halfmovessequence(startpeg, endpeg, disklist[:(n_disks-x1)], newpeglist, n_recursion+1)
            #print("secondmoves, also die restlichen Zwischentürme",secondmoves)
            return firstmoves[:]+secondmoves[:]
            
    
    def movessequence(self,startpeg=None,endpeg=None, disklist=None, peglist=None, n_recursion = 0):
        """gibt alle benötigten Züge zurück"""
        if startpeg == None:
            startpeg = self.peglist[0]
        if endpeg == None:
            endpeg = self.peglist[-1]
        if disklist == None:
            disklist=[]
            for i in self.disklist:
                disklist.append(i)
        if peglist == None:
            peglist=[]
            for i in self.peglist:
                peglist.append(i)
        #print("movessequence:",n_recursion,disklist,peglist,"startpeg",startpeg,"endpeg",endpeg)
        if len(disklist)==1:
            #print("es bleibt nur eine scheibe zum bewegen",disklist[0],startpeg,endpeg)
            self.move([disklist[0],startpeg,endpeg])
            return [[disklist[0],startpeg,endpeg]]
        elif len(peglist)==3:
            return self.threemovessequence(startpeg,endpeg,disklist, peglist)
        else:
            firstmoves = self.halfmovessequence(startpeg,endpeg, disklist,peglist,n_recursion)
            #print("firstmoves ganz",firstmoves)
            self.move([disklist[0],startpeg,endpeg])
            lastmoves = []
            for i in range(1,len(firstmoves)+1):
                #iterates from len(firstmoves)-1 to 0
                currentmove = firstmoves[len(firstmoves)-i]
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
                self.move(newcurrentmove)
                lastmoves.append(newcurrentmove)
            
            #print("Hier kommt die Bewegung einer größten Scheibe:",disklist[0],startpeg,endpeg)
            return firstmoves[:]+[[disklist[0],startpeg,endpeg]]+lastmoves[:]

Trial = Configuration(4,7)
Trial.printoutdata()

# =============================================================================
# for n_pegs in range(3,10):
#     for n_disks in range(1,15):
#         print(n_pegs,n_disks)
#         Configuration(n_pegs,n_disks).movessequence()
# =============================================================================
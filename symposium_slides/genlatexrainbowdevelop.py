import turm_von_hanoi_moves2
import os

def disksizefactor(n, disk):
    return str(0.49 - disk * 0.4/n)

def genframe_cryptography(configlist, maxnumber, text):
    n = configlist[0]
    k = configlist[1]
    diskdict = configlist[2]
    movenumber = configlist[3]
    if movenumber == 0:
        lineslist = [r"\begin{frame}{Anfangskonfiguration}"]
    elif movenumber == maxnumber:
        lineslist = [r"\begin{frame}{Nach Zug "+str(movenumber)+r" - Endkonfiguration}"]
    elif movenumber == int(maxnumber/2+1):
        lineslist = [r"\begin{frame}{Nach Zug "+str(movenumber)+r" - Zwischenturmkonfiguration}"]
    else:
        lineslist = [r"\begin{frame}{Nach Zug "+str(movenumber)+r"}"]
    lineslist += [r"\begin{figure}", r"\centering", r"\begin{tikzpicture}"]
    diskheight = min(10, 130/n)
    lineslist.append(
        r"\pgfmathsetlengthmacro\diskheight{" + str(diskheight)+r"};")
    lineslist.append(r"\pgfmathsetmacro\k{"+str(k)+r"};")
    lineslist.append(r"\pgfmathsetlengthmacro\step{\textwidth/\k};")
    lineslist.append(
        r"\draw[color = white] (\step/2,0) -- (\textwidth+\step,0);")
    lineslist.append(
        r"\foreach \n in {1,...,\k} \draw [fill = brown, draw = black, rounded corners = \step/20] (\step*\n,0) rectangle (\step*\n+\step/10,5);")
    for peg in diskdict:
        peglineslist = []
        disklist = diskdict[peg]
        for number, disk in enumerate(disklist):
            try:
                letter = text[disk]
            except:
                letter = ""
            diskline = [r"\definecolor{mycolor}{rgb:hsb}{" + str("%.2f" % round((disk/n)*0.8,3)) +
                        r",1,0.8}",
                        r"\draw [fill = mycolor, draw = black, rounded corners = \diskheight/2] (\step*"+str(peg) +
                        r"+\step/20-\step*"+disksizefactor(n, disk) +
                        r",\diskheight*"+str(number) +
                        r") rectangle (\step*"+str(peg) +
                        r"+\step/20+\step*"+disksizefactor(n, disk) +
                        r",\diskheight*"+str(number+1)+
                        r") node[pos=.5, font = \small] {"+letter+r"};"]
            peglineslist += diskline
        lineslist += peglineslist

    lineslist += [r"\end{tikzpicture}", r"\end{figure}", r"\end{frame}"]
    return lineslist


def genconfiglists(n, k):
    moveslist = turm_von_hanoi_moves2.movessequence_ui(n, k)
    liste = []
    for i in range(n):
        liste.append(i)
    startdict = {1: liste}
    for peg in range(2, k+1):
        startdict[peg] = []
    startconfig = [n, k, startdict, 0]
    configlists = [startconfig]
    newconfig = startconfig.copy()
    for movenumber, move in enumerate(moveslist):
        currentconfig = newconfig.copy()
        currentdict = currentconfig[2].copy()
        disk = move[0]
        removepeg = move[1]+1
        addpeg = move[2]+1
        removepeglist = currentdict[removepeg].copy()
        addpeglist = currentdict[addpeg].copy()
        removepeglist.remove(disk)
        addpeglist.append(disk)
        newdict = currentdict.copy()
        newdict[removepeg] = removepeglist
        newdict[addpeg] = addpeglist
        newconfig = [n, k, newdict, movenumber+1]
        configlists.append(newconfig)
    #maxnumber = len(moveslist)-1
    return configlists

def frames(n, k, begin = 0, end = -1, text = ""):
    configlists = genconfiglists(n, k)
    maxnumber = len(configlists)-1
    configlists = configlists[begin:]
    if end !=-1:
        configlists = configlists[:end-begin+1]
    totallines = []
    for configlist in configlists:
        lineslist = genframe(configlist, maxnumber, text)
        totallines += lineslist
    for line in totallines:
        print(line)
import os
import pprint
from PIL import Image


def faculty(x):
    if x == 0:
        return 1
    value = 1
    for i in range(1, x+1):
        value *= i
    return int(value)

def bk(n, k):
    if n == k:
        return 1
    if k < 0 or k > n:
        return 0
    value = faculty(n) / (faculty(k) * faculty(n - k))
    return int(value)

def t_(n, k):
    t = -1
    x = 0
    while n > x:
        t += 1
        x = bk(k-2+t, k-2)
    return t

def formula(n, k, t):
    """berechnet die Mindestzugzahl bei "n" Knickpunkten, "m" Feldern und "AS" Scheiben"""
    if k == 3:
        return 2**(n)-1
    x = 0
    for i in range(0, t+1):
        x = x + 2**i*bk(i+k-3, k-3)
    correction = 2**t*(n-bk(t+k-2, k-2))
    return x + correction

def M(n, k):
    """berechnet die Mindestanzahl von Zügen, die für "As" Scheiben bei "m" Feldern benötigt werden"""
    t = t_(n, k)
    x = formula(n, k, t)
    return x

def f_4(As):
    a = -3/2+math.sqrt(2*As+0.25)
    return a*2**(a+1)+1

def upsilon(n,k):
    s = t_(n,k)
    above = bk(s+k-3,k-3)
    below = bk(s+k-2,k-2)-n
    result = bk(above,below)
    return result


def movessequence(startpeg, endpeg, disklist, peglist):
    """gibt alle benoetigten Zuege zurueck"""
    #print("Die Scheiben {} sollen unter Benutzung der Felder {} von {} nach {} bewegt werden".format(disklist,peglist,startpeg,endpeg))
    #print(disklist)
    #spezialfaelle
    if len(disklist) == 1:
        #print("es bleibt nur eine Scheibe zum bewegen",disklist[0],startpeg,endpeg)
        return [[disklist[0], startpeg, endpeg]]

    else:
        #zwischenturmhoehe berechnen
        pegheight = calculatemiddletower(startpeg, endpeg, disklist, peglist)
        #dann die movessequencelist fuer die Zwischentuerme berechnen
        movesequencelist = []
        #bewege einen Zwischenturm nach dem anderen
        peglist2 = peglist.copy()
        disklist2 = disklist.copy()
        for peg in peglist:
            height = pegheight[peg]
            if height != 0:
                #print("aktuell bearbeiteter Zwischenturmpeg:",peg,"in Rekursionstiefe",n_recursion)
                movingdisks = disklist2[-height:]
                #print(movingdisks)
                movesequencelist += movessequence(startpeg,
                                                  peg, movingdisks, peglist2)
                peglist2.remove(peg)
                disklist2 = disklist2[:-height]

        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        #danach die groesste Scheibe
        #print("groesste Scheibe:",[disklist[0],startpeg,endpeg])
        #dann rueckwaerts
        lastmoves = []
        for i in range(1, len(movesequencelist)+1):
            #iterates from len(firstmoves)-1 to 0
            currentmove = movesequencelist[len(movesequencelist)-i]
            #tauschen von start und endpeg
            if currentmove[1] == startpeg:
                peg2 = endpeg
            elif currentmove[1] == endpeg:
                peg2 = startpeg
            else:
                peg2 = currentmove[1]
            if currentmove[2] == startpeg:
                peg1 = endpeg
            elif currentmove[2] == endpeg:
                peg1 = startpeg
            else:
                peg1 = currentmove[2]
            newcurrentmove = [currentmove[0], peg1, peg2]
            lastmoves.append(newcurrentmove)

        return movesequencelist[:]+[[disklist[0], startpeg, endpeg]]+lastmoves[:]

def calculatemiddletower(startpeg, endpeg, disklist, peglist):
    """berechnet die Hoehe der Zwischentuerme und gibt ein dict mit dem Zwischenturm als key und der hoehe als wert aus"""
    m = len(peglist)
    As = len(disklist)
    mmpegdict = {}
    n = 0
    x = 1
    while As > x:
        n += 1
        x = bk(n+m-2, m-2)

    #print(As,n)
    #berechnen der minimalen und maximalen Hoehe eines Zwischenturms
    i = 0
    for peg in peglist:
        if peg == startpeg or peg == endpeg:
            mmpegdict[peg] = [0, 0]
        else:
            mmpegdict[peg] = [int(bk(n+m-i-4, m-i-2)), int(bk(n+m-i-3, m-i-2))]
            i += 1

    #im Fall von einer Scheibe stimmt die minimale Hoehe nicht
    for peg in mmpegdict:
        if mmpegdict[peg][1] == 1:
            mmpegdict[peg][0] = 0

    #berechnen der abzueglichen Scheibenzahl fuer nicht-inkrementgrenzfaelle
    knowndisks = int(bk(n+m-2, m-2))
    toomuchdisks = knowndisks-As
    pegheightdict = {}
    #wegnehmen von der pegheigthdisklist
    takenallaway = False  # true wenn alle ueberfluessigen Scheiben weggenommen sind
    for peg in peglist:
        min_value = mmpegdict[peg][0]
        max_value = mmpegdict[peg][1]
        difference = max_value-min_value
        toomuchdisks -= difference
        if takenallaway:
            pegheightdict[peg] = max_value
        elif toomuchdisks >= 0:
            pegheightdict[peg] = min_value
        else:
            pegheightdict[peg] = max_value-toomuchdisks-difference
            takenallaway = True
    return pegheightdict

def movessequence_ui(n, k):
    peglist = []
    disklist = []
    for i in range(k):
        peglist.append(i)
    for i in range(n):
        disklist.append(i)
    moves = movessequence(peglist[0], peglist[-1], disklist, peglist)
    #print(moves, len(moves))
    return moves


def disksizefactor(n, disk):
    return 0.49 - disk * 0.4/n

def gentikz(configlist):
    """erstellt den tikz-code für eine configuration aus configlist[2],
    wobei es sich hier um ein dict folgenden Aufbaus handelt:
    {peg:[liste mit scheiben],  etc.}
    """
    n = configlist[0]
    k = configlist[1]
    diskdict = configlist[2]
    lineslist = [r"\begin{tikzpicture}"]
    diskheight = min(10, 130/n)
    lineslist.append(
        r"\pgfmathsetlengthmacro\diskheight{" + str(diskheight)+r"};")
    lineslist.append(r"\pgfmathsetmacro\k{"+str(k)+r"};")
    lineslist.append(r"\pgfmathsetlengthmacro\step{\textwidth/\k};")
    lineslist.append(
        r"\draw[color = white] (\step/2,0) -- (\textwidth+\step,0);")
    lineslist.append(
        r"\foreach \n in {1,...,\k} \draw [fill = brown, draw = black, rounded corners = \step/20] (\step*\n,0) rectangle (\step*\n+\step/10,3);")
    usable_pegs = k+1
    for peg in diskdict:
        disklist = diskdict[peg]
        if peg != 1 and peg != k:
            usable_pegs -= 1
            pegheight = len(disklist)
            lineslist.append(r"\node ("+str(peg)+r") at (\step*"+str(peg+1/20)+r",-0.5){M("+str(pegheight)+","+str(usable_pegs)+")="+str(M(pegheight, usable_pegs))+r"};")
            lineslist.append(r"\node ("+str(peg)+r") at (\step*"+str(peg+1/20)+r",-1){I("+str(pegheight)+","+str(usable_pegs)+")="+str(2**t_(pegheight, usable_pegs))+r"};")
    for peg in diskdict:
        if diskdict[peg] != []:
            peglineslist = []
            disklist = diskdict[peg]
            for number, disk in enumerate(disklist):
                diskline = [r"\definecolor{mycolor}{rgb:hsb}{" + str("%.2f" % round((disk/n)*0.8, 3)) +
                            r",1,0.8}",
                            r"\draw [fill = mycolor, draw = black, rounded corners = \diskheight/2] (\step*"+str(peg) +
                            r"+\step/20-\step*"+str(disksizefactor(n, disk)) +
                            r",\diskheight*"+str(number) +
                            r") rectangle (\step*"+str(peg) +
                            r"+\step/20+\step*"+str(disksizefactor(n, disk)) +
                            r",\diskheight*"+str(number+1)+r");"]
                peglineslist += diskline
            lineslist += peglineslist

    lineslist += [r"\end{tikzpicture}"]
    return lineslist

def genbasictikz(configlist, maxnumber, movenumber, height = 1, shownumber = False):
    n = configlist[0]
    k = configlist[1]
    diskdict = configlist[2]
    #movenumber = configlist[3]
    lineslist = [r"\begin{tikzpicture}"]
    diskheight = min(10, 130/n)
    lineslist.append(
        r"\pgfmathsetlengthmacro\diskheight{" + str(diskheight)+r"};")
    lineslist.append(r"\pgfmathsetmacro\k{"+str(k)+r"};")
    lineslist.append(r"\pgfmathsetlengthmacro\step{\textwidth/\k};")
    if shownumber:
        lineslist.append(r"\node[opacity = 1] at (1.5,4) {\LARGE "+str(movenumber)+r"};")
    lineslist.append(
        r"\draw[color = white] (\step/2,0) -- (\textwidth+\step,0);")
    lineslist.append(
        r"\foreach \n in {1,...,\k} \draw [fill = brown, draw = black, rounded corners = \step/20] (\step*\n,0) rectangle (\step*\n+\step/10,"+str(5*height)+");")
    for peg in diskdict:
        peglineslist = []
        disklist = diskdict[peg]
        for number, disk in enumerate(disklist):
            diskline = [r"\definecolor{mycolor}{rgb:hsb}{" + str("%.2f" % round((disk/n)*0.8,3)) +
                        r",1,0.8}",
                        r"\draw [fill = mycolor, draw = black, rounded corners = \diskheight/2] (\step*"+str(peg) +
                        r"+\step/20-\step*"+str(disksizefactor(n, disk)) +
                        r",\diskheight*"+str(number) +
                        r") rectangle (\step*"+str(peg) +
                        r"+\step/20+\step*"+str(disksizefactor(n, disk)) +
                        r",\diskheight*"+str(number+1)+r");"]
            peglineslist += diskline
        lineslist += peglineslist

    lineslist += [r"\end{tikzpicture}"]
    return lineslist

def gentikzincrement(configlist):
    """erstellt den tikz-code für eine configuration aus configlist[2] mit grünem streifen für inkrementbereich,
    wobei es sich hier um ein dict folgenden Aufbaus handelt:
    {peg:[liste mit scheiben],  etc.}
    """
    n = configlist[0]
    k = configlist[1]
    diskdict = configlist[2]
    lineslist = [r"\begin{tikzpicture}"]
    diskheight = min(10, 130/n)
    lineslist.append(
        r"\pgfmathsetlengthmacro\diskheight{" + str(diskheight)+r"};")
    lineslist.append(r"\pgfmathsetmacro\k{"+str(k)+r"};")
    lineslist.append(r"\pgfmathsetlengthmacro\step{\textwidth/\k};")
    lineslist.append(
        r"\draw[color = white] (\step/2,0) -- (\textwidth+\step,0);")
    lineslist.append(
        r"\foreach \n in {1,...,\k} \draw [fill = brown, draw = black, rounded corners = \step/20] (\step*\n,0) rectangle (\step*\n+\step/10,2.5);")
    usable_pegs = k+1
    pegheightlist = []
    usable_peglist = []
    for peg in diskdict:
        disklist = diskdict[peg]
        peglineslist = []
        if diskdict[peg] != []:
            disklist = diskdict[peg]
            for number, disk in enumerate(disklist):
                diskline = [r"\definecolor{mycolor}{rgb:hsb}{" + str("%.2f" % round((disk/n)*0.8, 3)) +
                            r",1,0.8}",
                            r"\draw [fill = mycolor, draw = black, rounded corners = \diskheight/2] (\step*"+str(peg) +
                            r"+\step/20-\step*"+str(disksizefactor(n, disk)) +
                            r",\diskheight*"+str(number) +
                            r") rectangle (\step*"+str(peg) +
                            r"+\step/20+\step*"+str(disksizefactor(n, disk)) +
                            r",\diskheight*"+str(number+1)+r");"]
                peglineslist += diskline
        if peg!=k and peg !=1:
            usable_pegs -= 1
            incrementblock_min = bk(t_(n,k)-1+usable_pegs-3,usable_pegs-2)
            incrementblock_max = bk(t_(n,k)-1+usable_pegs-2,usable_pegs-2)
            greenrectanglelines = [r"\draw[draw = green!45!yellow, thick, rounded corners = \diskheight/4, fill = green!50!yellow,fill opacity = .3] ("
                +r"\step*"+str(peg+1/20-0.48)
                +r",\diskheight*"+str(incrementblock_min)
                +r") rectangle (\step*"+str(peg+1/20+0.48)
                +r",\diskheight*"+str(incrementblock_max)+r");",
                r"\node[above right] at (\step*"+str(peg+1/20-0.48-0.04)
                +r",\diskheight*"+str(incrementblock_min-0.2)
                +r"){"+str(incrementblock_max-incrementblock_min)+r"};"
                ]
            peglineslist += greenrectanglelines
            pegheight = len(disklist)
            peglineslist.append(r"\node at (\step*"+str(peg+1/20)+r",-1){$M("+str(pegheight)+","+str(usable_pegs)+")="+str(M(pegheight, usable_pegs))+r"$};")
            peglineslist.append(r"\node at (\step*"+str(peg+1/20)+r",-0.5){$I("+str(pegheight)+","+str(usable_pegs)+")="+str(2**t_(pegheight, usable_pegs))+r"$};")
            pegheightlist.append(pegheight)
            usable_peglist.append(usable_pegs)
        if peg == k:
            for pegheight, usable_pegs in zip(pegheightlist, usable_peglist):
                peg = k+2-usable_pegs
                if peg > 2 and peg < k:
                    peglineslist.append(r"\node at (\step*"
                        +str(peg+1/20)
                        +r",-1.5){$+"
                        +str(M(pegheight, usable_pegs))
                        +r"$};")
            string = r"\node[right] at (\step*"+str(1+1/20-0.5)+r",-1.5){$\to M("+str(n)+","+str(k)+")=2*("+str(M(pegheightlist[0],usable_peglist[0]))+r"$};"
            peglineslist.append(string)
            string = r"\node[right] at (\step*"+str(k+1/20-0.5)+r",-1.5){$)+1 ="+str(M(n,k))+r"$};"
            peglineslist.append(string)
            string = r"\node[right] at (\step*"+str(peg+1/20+0.5)+r",-0.5){$\to I("+str(n)+","+str(k)+")="+str(2**t_(n,k))+"$};"
            peglineslist.append(string)
        lineslist += peglineslist
    lineslist += [r"\end{tikzpicture}"]
    for line in lineslist:
        print(line)

def gencryptographytikz(configlist, movenumber, text):
    n = configlist[0]
    k = configlist[1]
    diskdict = configlist[2]
    lineslist = [r"\begin{tikzpicture}"]
    diskheight = min(10, 130/n)
    lineslist.append(
        r"\pgfmathsetlengthmacro\diskheight{" + str(diskheight)+r"};")
    lineslist.append(r"\pgfmathsetmacro\k{"+str(k)+r"};")
    lineslist.append(r"\pgfmathsetlengthmacro\step{\textwidth/\k};")
    lineslist.append(r"\node[opacity = 1] at (1.5,4) {\LARGE "+str(movenumber)+r"};")
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
                        r"+\step/20-\step*"+str(disksizefactor(n, disk))+
                        r",\diskheight*"+str(number) +
                        r") rectangle (\step*"+str(peg) +
                        r"+\step/20+\step*"+str(disksizefactor(n, disk))+
                        r",\diskheight*"+str(number+1)+
                        r") node[pos=.5, font = \small] {"+letter+r"};"]
            peglineslist += diskline
        lineslist += peglineslist

    lineslist += [r"\end{tikzpicture}"]
    return lineslist

def genconfiglists(n, k):
    moveslist = movessequence_ui(n, k)
    liste = []
    for i in range(n):
        liste.append(i)
    startdict = {1: liste}
    for peg in range(2, k+1):
        startdict[peg] = []
    startconfig = [n, k, startdict]
    configlists = [startconfig]
    newconfig = startconfig.copy()
    for move in moveslist:
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
        newconfig = [n, k, newdict]
        configlists.append(newconfig)
    return configlists


def configlists_function(n,k):
    configlists = genconfiglists(n,k)
    return configlists

def frame(n,k,begin = 0, end = -1,frame = True,start = 1,height = 1,shownumber = False):
    """
    n number of disks
    k number of fields
    begin smallest movenumber
    end biggest movenumber
    frame nur tikzpictureoverlays oder ganze Folie
    start overlay, bei dem es anfängt
    höhe bruchteil der eigentlichen höhe
    shownumber Zugzahl wird angezeigt
    """
    #os.chdir(r"~/Dokumente/python_files/toh/bsnt_vortrag/zugfolge_slides")
    titleline = r"\begin{frame}{Zugfolge für $n=" + str(n) + r"$ und $k=" + str(k) + r"$}"
    f = open("zugfolge_{}_{}.tex".format(n,k),"w")
    if frame:
        print(titleline)
        f.write(titleline+"\n")
    configlists = genconfiglists(n,k)
    maxnumber = len(configlists)-1
    configlists = configlists[begin:]
    if end !=-1:
        configlists = configlists[:end-begin+1]
    for movenumber, configlist in enumerate(configlists):
        tikzlist = genbasictikz(configlist,maxnumber,movenumber+begin, height, shownumber)
        overlaylist = [r"\only<" + str(movenumber+start) + r">{"]
        overlaylist += tikzlist
        overlaylist += [r"}"]
        for line in overlaylist:
            print(line)
            f.write(line+"\n")
    finishline = r"\end{frame}"
    if frame:
        f.write(finishline)
        print(finishline)
    f.close()

def show(n, k, text, move):
    os.chdir(r"C:\Users\DELL\Documents\python_files\toh\posters\images3")
    configlists = configlists_function(n, k)
    #configlist = configlists[int((len(configlists)-1)/2+1)]
    #configlist = [11, 5, {1: [], 2: [7, 8, 9, 10], 3: [4, 5, 6], 4: [1, 2, 3], 5: [0]}]
    configlist = configlists[move]
    lineslist = gencryptographytikz(configlist, move, text)
    name = "{}_{}_cryptography_{}".format(configlist[0], configlist[1], move)
    filename = name + ".tex"
    with open(filename, "w") as f:
        totallines = [r"\documentclass[tikz]{standalone}",
                      r"\usepackage{xcolor}", r"\usepackage{tikz,pgf}", r"\begin{document}"]
        totallines += lineslist
        totallines.append(r"\end{document}")
        for line in totallines:
            f.write(line+"\n")
    os.system("pdflatex -quiet {}".format(filename))
    #os.system("start {}.pdf".format(name))
    fileslist = os.listdir()
    for f in fileslist:
        if name in f:
            if f != name +".tex" and f != name +".pdf":
                os.remove(f)

def graphic(n,k):
    configlists = genconfiglists(n, k)
    configlist = configlists[int((len(configlists)-1)/2+1)]
    lineslist = gentikz(configlist)
    with open("hello.txt","w") as f:
        for line in lineslist:
            f.write(line+"\n")
    for line in lineslist:
        print(line)

def nktable(nmax, kmax, caption = "", sort = "value", relsize = 0.3):
    number_of_columns = nmax
    linelist = []
    firstline = r"\begin{tabular}{"
    secondline = r"&\multicolumn{"+str(nmax)+ r"}{|c}{Scheibenzahl $n$}\\"
    i = 0
    while i < number_of_columns:
        i += 1
        if i == 1:
            firstline += "c|"
        firstline += "c"
    firstline += "}"
    hline = r"\hline"
    linelist.append(firstline)
    linelist.append(secondline)
    line = r"$k\downarrow$"
    for n in range(1,nmax+1):
        line += "&"+str(n)

    for k in range(3,kmax+1):
        line += r"\\"
        linelist.append(line)
        if k == 3:
            linelist.append(hline)
        line = str(k)
        for n in range(1,nmax+1):
            if sort == "value":
                line += "&"+str(M(n,k))
            elif sort == "increment":
                line += "&"+str(2**t_(n,k))
            elif sort == "possibilities":
                line += "&"+str(upsilon(n,k))
    linelist.append(line)
    linelist.append(r"\end{tabular}")
    for line in linelist:
        print(line)

def tktable(tmax,kmax):
    os.chdir(r"C:\Users\DELL\Documents\python_files\toh\posters\images1")
    number_of_columns = tmax
    #linelist = [r"\begin{table}[h]",r"\resizebox{0.3\textwidth}{!}{"]
    linelist = []
    firstline = r"\begin{tabular}{"
    secondline = r"&\multicolumn{"+str(number_of_columns)+ r"}{|c}{Inkrementblocklängen}\\"
    i = 0
    while i < number_of_columns:
        i += 1
        if i == 1:
            firstline += "c|"
        firstline += "c"
    firstline += "}"
    hline = r"\hline"
    linelist.append(firstline)
    linelist.append(secondline)
    line = r"$k\downarrow$"
    for n in range(0,tmax):
        line += "&"+str(2**n)

    for k in range(3,kmax+1):
        line += r"\\"
        linelist.append(line)
        if k == 3:
            linelist.append(hline)
        line = str(k)
        for t in range(0,tmax):
            line += "&"+str(bk(t+k-3,k-3))
    linelist.append(line)
    linelist.append(r"\end{tabular}")
    #linelist.append(r"\caption{"+caption+r"}")
    #linelist.append(r"}")
    #linelist.append(r"\end{table}")
    name = str(n)+"_"+str(k)+"incrementnumbers_table"
    dateiname=name+".tex"
    f=open(dateiname,"w")
    for line in linelist:
        f.write(line+"\n")
    f.close()

def frame(n,k,begin = 0, end = -1,frame = True,start = 1,height = 1,shownumber = False):
    """
    n number of disks
    k number of fields
    begin smallest movenumber
    end biggest movenumber
    frame nur tikzpictureoverlays oder ganze Folie
    start overlay, bei dem es anfängt
    höhe bruchteil der eigentlichen höhe
    shownumber Zugzahl wird angezeigt
    """
    #os.chdir(r"~/Dokumente/python_files/toh/bsnt_vortrag/zugfolge_slides")
    lines = [r"\documentclass{beamer}", r"\usepackage{tikz}", r"\usepackage[utf8]{inputenc}", r"\usepackage[T1]{fontenc}", r"\begin{document}", r"\begin{frame}{Zugfolge für $n=" + str(n) + r"$ und $k=" + str(k) + r"$}"]
    configlists = genconfiglists(n,k)
    maxnumber = len(configlists)-1
    configlists = configlists[begin:]
    if end !=-1:
        configlists = configlists[:end-begin+1]
    for movenumber, configlist in enumerate(configlists):
        tikzlist = genbasictikz(configlist,maxnumber,movenumber+begin, height, shownumber)
        overlaylist = [r"\only<" + str(movenumber+start) + r">{"]
        overlaylist += tikzlist
        overlaylist += [r"}"]
        for line in overlaylist:
            lines.append(line)
    lines.append(r"\end{frame}")
    lines.append(r"\end{document}")
    #print(lines)
    compile(lines, "trash")

def compile(lines, name):
    """
    compile lines and use a file with name as tex-file
    """
    try:
        f = open("{}.tex")
        f.close()
    except:
        os.system("touch {}.tex".format(name))

    with open("{}.tex".format(name), "w") as f:
        for line in lines:
            f.write(line+"\n")
    os.system("pdflatex {}.tex".format(name))
    os.system("xdg-open {}.pdf".format(name))
    os.system("rm {}.log".format(name))
    os.system("rm {}.aux".format(name))

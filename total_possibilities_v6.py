## TODO: get all FS algorithm possibilities and count them (compare with adjustedUpsilon)

############################################################

import pprint
import os
#from Anzahl_Zugfolgen import adjustedUpsilon

def faculty(x):
    """
    returns 'x!'
    """
    if x == 0:
        return 1
    value = 1
    for i in range(1, x+1):
        value *= i
    return int(value)


def bk(n, k):
    """
    returns 'n over k'
    """
    if n == k:
        return 1
    if k < 0 or k > n:
        return 0
    value = faculty(n) / (faculty(k) * faculty(n - k))
    return int(value)


def t_(n, k):
    """
    returns the exponent of the increment of a configuration with n disks and k pegs
    """
    t = -1
    x = 0
    while n > x:
        t += 1
        x = bk(k-2+t, k-2)
    return t


def formula(n, k, t):
    """
    returns the minimum number of moves for increment 2^t, k pegs and n disks
    """
    if k == 3:
        return 2**(n)-1
    x = 0
    for i in range(0, t+1):
        x = x + 2**i*bk(i+k-3, k-3)
    correction = 2**t*(n-bk(t+k-2, k-2))
    return x + correction


def M(n, k):
    """
    returns the minimum number of moves for k pegs and n disks
    """
    t = t_(n, k)
    x = formula(n, k, t)
    return x

def b_(p,t,k):
    """
    helper function for adjustedUpsilon
    """
    if t == 0:
        return 0
    return bk(k-p+t-3,t-1)

def h_(p,t,k):
    """
    helper function for adjustedUpsilon
    """
    return bk(k-p+t-2,t-1)

def A_(n,t,k):
    """
    helper function for adjustedUpsilon
    """
    if t == 0:
        return 0
    return n - bk(t-1+k-2,t-1)

def lowerbound(A,t,k):
    """
    helper function for adjustedUpsilon
    """
    summe = 0
    for p in range(2,k-1):
        summe += b_(p,t,k)
    return int(max([0,A-summe]))

def upperbound(A,t,k):
    """
    helper function for adjustedUpsilon
    """
    return int(min([A,b_(1,t,k)]))


def upsilon(n,k):
    """
    our first conjecture for the number of possibilities, proven to be wrong
    """
    s = t_(n,k)
    above = bk(s+k-3,k-3)
    below = bk(s+k-2,k-2)-n
    result = bk(above,below)
    return result

def adjustedUpsilon(n, k):
    """
    computes the number of possibilities according to the Frame-Stewart algorithm
    """
    if n==0 or k==3 or n<k:
        return 1
    t = t_(n,k)
    A = A_(n,t,k)
    lower = lowerbound(A,t,k)
    upper = upperbound(A,t,k)
    summe = 0
    for a in range(lower, upper + 1):
        value1 = adjustedUpsilon(n - h_(1, t-1, k) - a, k - 1)
        value2 = adjustedUpsilon(h_(1, t - 1, k) + a, k)
        summe += value1*value2
    return summe

#visualization functions ###################################################################################

def disksizefactor(n, disk):
    """
    a helper function for gentikz
    """
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
    if False:
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

def showhistory(THobject):
    """
    creates a pdf with all steps of creating the current configuration of THobject
    """
    history = THobject.history
    tikzlist = []
    for configuration in history:
        newconfiguration = {}
        for peg in configuration:
            newconfiguration[peg+1] = []
        for peg in newconfiguration:
            for disk in configuration[peg-1]:
                newconfiguration[peg].append(THobject.disks-disk)
        for peg in newconfiguration:
            newconfiguration[peg].reverse()
        configlist = [THobject.disks, THobject.pegs,newconfiguration]
        tikzlist.append(gentikz(configlist))
    with open("some_text_file.tex", "w") as f:
        totallines = [r"\documentclass[tikz]{standalone}",
                      r"\usepackage{xcolor}", r"\usepackage{tikz,pgf}", r"\begin{document}"]
        for tikzpicture in tikzlist:
            for line in tikzpicture:
                totallines.append(line)
            totallines.append(r"\newpage")
        totallines.append(r"\end{document}")
        for line in totallines:
            f.write(line+"\n")
    os.system("pdflatex some_text_file.tex")
    os.system("xdg-open some_text_file.pdf")

def showconfigurations(configurations):
    """
    visualizes configurations
    where configurations = {1:[list of configurations], 2:[list of configurations], ...}
    """
    totallines = [r"\documentclass[tikz]{standalone}",
                  r"\usepackage{xcolor}", r"\usepackage{tikz,pgf}", r"\begin{document}"]
    for movenumber in configurations:
        totallines.append(str(movenumber))
        for configuration in configurations[movenumber]:
            peglist = []
            disklist = []
            for peg in configuration:
                peglist.append(peg)
                for disk in configuration[peg]:
                    disklist.append(disk)
            disks = len(disklist)
            pegs = len(peglist)
            newconfiguration = {}
            for peg in configuration:
                newconfiguration[peg+1] = []
            for peg in newconfiguration:
                for disk in configuration[peg-1]:
                    newconfiguration[peg].append(disks-disk)
            for peg in newconfiguration:
                newconfiguration[peg].reverse()
            configlist = [disks, pegs,newconfiguration]
            tikzcode = gentikz(configlist)
            for line in tikzcode:
                totallines.append(line)
    totallines.append(r"\end{document}")
    with open("some_text_file.txt", "w") as f:
        for line in totallines:
            f.write(line+"\n")
    os.system("pdflatex some_text_file.txt")
    os.system("xdg-open some_text_file.pdf")

def nktable(nmax, kmax, sort = "value"):
    """
    create a latex table with the disks as columns and pegs as rows
    the entries of the table are specified by the parameter 'sort'
    sort value: the minimum number of moves to solve a configuration with n disks and k pegs
    sort increment: the increment of a configuration with n disks and k pegs
    sort possibilities/adjustedpossibilities/totalpossibilities:
    the number of possibilities to get to the finished state of a configuration with n disks and k pegs according to
    our first (wrong) conjecture with the FS-algorithm/our adjusted conjecture for the FS-algorithm/the bruteforce method
    """
    number_of_columns = nmax
    linelist = [r"\documentclass{article}", r"\usepackage[left = 0 cm, top = 0cm]{geometry}", r"\begin{document}"]
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
            elif sort == "totalpossibilities":
                line += "&"+str(totalpossibilities(n,k))
            elif sort == "adjustedpossibilities":
                line += "&"+str(adjustedUpsilon(n,k))

    linelist.append(line)
    linelist.append(r"\end{tabular}")
    linelist.append(r"\end{document}")
    name = str(n)+"_"+str(k)+sort+"_table"
    dateiname=name+".tex"
    f=open(dateiname,"w")
    for line in linelist:
        f.write(line+"\n")
    f.close()
    os.system("pdflatex -quiet {}".format(dateiname))
    os.system("xdg-open {}.pdf".format(name))

#bruteforce find all possibilities########################################################################################

configurations = {}# a dict with the number of moves as key and a list of interesting configurations that can be reached within the number of moves
success_instances = [] # a list with all instances that reached the finished state

def start_configuration(disks, pegs):
    """
    creates a basic configurationdict without any moves for a given number of disks and pegs
    """
    configurationdict = {}
    for peg in range(pegs):
        configurationdict[peg] = []
    for disk in range(disks):
        configurationdict[0].append(disk)

    return configurationdict

class TH():
    """
    a Tower of Hanoi instance with the following properties
    - self.disks: the number of disks
    - self.pegs: the number of pegs
    - self.configurationdict: a dict {0:[list with disks on peg 0], 1:[list with disks on peg 1], ...}
    - self.history: a list with the configurationdicts of previous THs leading to this instance
    - self.movenumber: the number of moves that is needed to get to this configuration
    - self.normalizedconfiguration: a configuration where the pegs are sorted according to their biggest disk
    """
    def __init__(self, disks, pegs, configurationdict = None, history = []):
        """
        initializes a TH
        """
        self.disks = disks
        self.pegs = pegs
        if not configurationdict:
            self.configurationdict = start_configuration(self.disks, self.pegs)
        else:
            self.configurationdict = configurationdict
        self.history = history.copy()
        self.history.append(self.configurationdict)
        self.movenumber = len(self.history)-1
        self.normalizedconfiguration = normalize(self.disks, self.pegs, self.configurationdict)

    def __repr__(self):
        string =  "TH"+ str(self.disks) + " "+ str(self.pegs) + " "+ str(self.normalizedconfiguration) + "\n"
        return string

    def __str__(self):
        string =  """{} disks, {} pegs, configuration: {}
        history:
        """.format(self.disks, self.pegs, self.configurationdict)
        for element in self.history:
            string += str(element) + "\n        "
        return string

def process(THobject):
    """
    either save or delete a TH instance
    save: it passes the 'check'-function
    delete: otherwise
    """
    global configurations
    if check(THobject):
        save(THobject)
        return True
    else:
        del THobject

def check(object):
    """
    this method checks whether the configuration is possibly going to lead to the minimum number of moves
    Let the finished state be the state when 'object' has freed its biggest disk and there is another free field
    """
    #first criterium: can it be reached with less moves? = is it already in the configurations-dict?
    global configurations
    global success_instances
    for movenumber in configurations:
        if movenumber < object.movenumber:
            for THobject in configurations[movenumber]:
                if object.normalizedconfiguration == THobject.normalizedconfiguration:
                    return False
    #second criterium: has 'object' already neeeded more than the minimum number of moves needed to reach the finished state
    if object.movenumber > (M(object.disks, object.pegs)-1)/2:
        return False

    #determine if 'object' has reached finished state
    bigdisk = object.disks-1
    oneempty = False#at least one empty peg
    bigalone = False#bigdisk is alone
    for peg in object.configurationdict:
        if bigdisk in object.configurationdict[peg]:
            if len(object.configurationdict[peg]) == 1:
                bigalone = True
        if len(object.configurationdict[peg]) == 0:
            oneempty = True

    if bigalone and oneempty:
        success_instances.append(object)
    else:
        if object.movenumber == (M(object.disks, object.pegs)-1)/2:
            return False
    return True

def possiblemoves(object,disk):
    """
    returns a list with all pegs this disk can be moved to.
    if the disk can't be moved to any other peg, it returns an empty list.
    """
    diskposition = getdiskposition(object, disk)
    smallest = getminimaldisk(object, diskposition)
    #if the disk is not the smallest on its peg, it can't be moved
    if disk != smallest:
        return []
    else:
        possiblepegs = []
        cero = False
        for peg in object.configurationdict:
            smallest = getminimaldisk(object, peg)
            #if the smallest disk of a peg is bigger than the disk, the disk can be moved on that peg
            if smallest > disk:
                possiblepegs.append(peg)
            #if this is the first peg without disks, our disk can be moved on it, if there have been other pegs without disks, we don't want the disk to be moved there.
            elif smallest == -1 and not cero:
                cero = True
                possiblepegs.append(peg)
        return possiblepegs

def getdiskposition(object,disk):
    """
    returns current peg of disk
    """
    for peg in object.configurationdict:
        if disk in object.configurationdict[peg]:
            return peg
    print("getdiskposition error: disk to big")
    return -1

def getminimaldisk(object,peg):
    """
    returns the smallest disk on the addressed peg
    """
    disks = object.configurationdict[peg]
    if len(disks) == 0:
        return -1
    else:
        return min(disks)

def normalize(disks, pegs, configurationdict):
    """
    returns a normalized configuration
    """
    maxvalues = {}#contains the biggest disk of each peg
    maxvaluelist = []#list with the biggest disks sorted
    for peg in configurationdict:
        disks = configurationdict[peg]
        if len(disks) == 0:
            maxvalues[peg] =  -1
            maxvaluelist.append(-1)
        else:
            maxvalues[peg] = max(disks)
            maxvaluelist.append(max(disks))
    maxvaluelist.sort()

    sortedpegdict = {}
    for peg in maxvalues:
        maxdisk = maxvalues[peg]
        if maxdisk != -1:
            index = maxvaluelist.index(maxdisk)
            sortedpegdict[index] = peg
    normalizedconfiguration = {}
    for peg in range(pegs):
        normalizedconfiguration[peg] = []

    for index in sortedpegdict:
        peg = sortedpegdict[index]
        normalizedconfiguration[index] = configurationdict[peg]
    for peg in normalizedconfiguration:
        normalizedconfiguration[peg].sort()

    return normalizedconfiguration

def save(THobject):
    """
    saves the instance in configurations
    """
    global configurations
    try:
        configurations[THobject.movenumber].append(THobject)
    except:
        configurations[THobject.movenumber] = [THobject]
    #print(THobject.movenumber, ":", THobject.normalizedconfiguration)

def allpossiblemoves(object):
    """
    returns a dict with disks as keys and all possible pegs in a list
    """
    possiblemovesdict = {}
    for disk in range(object.disks):
        possiblemovesdict[disk] = possiblemoves(object, disk)
    return possiblemovesdict

def tryallpossibilities(object):
    """
    tries all possibilities by calling the allpossiblemoves method and then executing the trypossibility method on each of them
    """
    allpossiblemovesdict = allpossiblemoves(object)
    for disk in allpossiblemovesdict:
        for peg in allpossiblemovesdict[disk]:
            trypossibility(object, disk, peg)

def trypossibility(object, disk, peg):
    #print("called: trypossibility from", object, "with disk:", disk, "and peg:", peg)
    """
    tries a possibility that is created from object.configurationdict by moving disk on peg
    creates a new THobject and then processes it
    """
    newconfiguration = {}
    #copy like this because it doesn't work otherwise
    for key in object.configurationdict:
        newconfiguration[key] = object.configurationdict[key].copy()
    diskposition = getdiskposition(object, disk)
    newconfiguration[diskposition].remove(disk)
    newconfiguration[peg].append(disk)

    newTH = TH(object.disks, object.pegs, newconfiguration, object.history)
    process(newTH)

def bruteforce(disks, pegs):
    """
    create TH(disks, pegs) and find out all possibilities to reach the finished state within the minimum number of moves
    """
    global configurations
    configurations = {}
    global success_instances
    success_instances = []
    ST = TH(disks,pegs)
    configurations[0] = [ST]
    process(ST)
    tryallpossibilities(ST)
    #now all possibilities for mv = 1 are created and saved if valid.
    #We can therefore iterate over all of them to create the possibilities of mv = 2 and so on
    maxmv = int((M(disks, pegs)-1)/2) ## NOTE: at maxmv the biggest disk has to be free and there has to be an empty peg
    for mv in range(1,maxmv+1):
        thismvconfigs = configurations[mv]
        for THobject in thismvconfigs:
            tryallpossibilities(THobject)

def totalpossibilities(disks, pegs):
    """
    return the number of possibilities that is computed by the bruteforce method
    """
    bruteforce(disks, pegs)
    return len(success_instances)

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

if True:
    import sys
    disks = int(sys.argv[1])
    pegs = int(sys.argv[2])
    #comparevalues(disks, pegs)
    nktable(disks,pegs, sort = "totalpossibilities")

    #print(success_instances)

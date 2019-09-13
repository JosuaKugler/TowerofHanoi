import os
from total_possibilities import *
from help_calculate import *

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

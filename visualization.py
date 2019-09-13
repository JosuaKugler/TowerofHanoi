import os
from total_possibilities import *
from help_calculate import *

def gentikz(configurationdict):
    """
    returns the code for a tikzpicture as a list, where each element is one line
    the compiled tikzpicture shows a tower of Hanoi with a configuration as in configurationdict
    """
    #compute n and k
    peglist = []
    disklist = []
    for peg in configurationdict:
        peglist.append(peg)
        for disk in configurationdict[peg]:
            disklist.append(disk)
    n = len(disklist)
    k = len(peglist)

    lineslist = [r"\begin{tikzpicture}",
    r"\pgfmathsetlengthmacro\diskheight{" + str(min(10, 130/n))+r"};",
    r"\pgfmathsetmacro\k{"+str(k)+r"};", #define k in latex so it is easier to read
    r"\pgfmathsetlengthmacro\step{\textwidth/\k};",#define step which is simply the width divided by k
    r"\draw[color = white] (\step/2,0) -- (\textwidth+\step,0);",#make some space at the sides
    r"\foreach \n in {1,...,\k} \draw [fill = brown, draw = black, rounded corners = \step/20] (\step*\n,0) rectangle (\step*\n+\step/10,3);"#draw the pegs
    ]
    if False:
        usable_pegs = k+1
        for peg in configurationdict:
            disklist = configurationdict[peg]
            if peg != 0 and peg != k-1:
                usable_pegs -= 1
                pegheight = len(disklist)
                lineslist.append(r"\node ("+str(peg)+r") at (\step*"+str(peg+1/20)+r",-0.5){M("+str(pegheight)+","+str(usable_pegs)+")="+str(M(pegheight, usable_pegs))+r"};")
                lineslist.append(r"\node ("+str(peg)+r") at (\step*"+str(peg+1/20)+r",-1){I("+str(pegheight)+","+str(usable_pegs)+")="+str(2**t_(pegheight, usable_pegs))+r"};")
    for peg in configurationdict:
        if configurationdict[peg] != []:
            peglineslist = []
            disklist = configurationdict[peg]
            disklist.reverse()
            for number, disk in enumerate(disklist):
                diskline = [r"\definecolor{mycolor}{rgb:hsb}{" + str("%.2f" % round((disk/n)*0.8, 3)) +
                            r",1,0.8}",
                            r"\draw [fill = mycolor, draw = black, rounded corners = \diskheight/2] (\step*"+str(peg+1) +
                            r"+\step/20-\step*"+str((disk+1)*0.4/n) +
                            r",\diskheight*"+str(number) +
                            r") rectangle (\step*"+str(peg+1) +
                            r"+\step/20+\step*"+str((disk+1)*0.4/n) +
                            r",\diskheight*"+str(number+1)+r");"]
                peglineslist += diskline
            lineslist += peglineslist

    lineslist += [r"\end{tikzpicture}"]
    return lineslist

def compile(lines, name):
    with open("{}.tex".format(name), "w") as f:
        for line in lines:
            f.write(line+"\n")
    os.system("pdflatex {}.tex".format(name))
    os.system("xdg-open {}.pdf".format(name))


def showhistory(THobject):
    """
    creates a pdf with all steps of creating the current configuration of THobject
    """
    history = THobject.history
    tikzlist = []
    for configuration in history:
        tikzlist.append(gentikz(configuration.copy()))
    lines = [r"\documentclass[tikz]{standalone}",
                  r"\usepackage{xcolor}", r"\usepackage{tikz,pgf}", r"\begin{document}"]
    for tikzpicture in tikzlist:
        for line in tikzpicture:
            lines.append(line)
        lines.append(r"\newpage")
    lines.append(r"\end{document}")
    compile(lines, "some_text_file")

def showconfigurations(configurations):
    """
    visualizes configurations
    where configurations = {1:[list of configurations], 2:[list of configurations], ...}
    """
    lines = [r"\documentclass[tikz]{standalone}",
                  r"\usepackage{xcolor}", r"\usepackage{tikz,pgf}", r"\begin{document}"]
    for movenumber in configurations:
        lines.append(str(movenumber))
        for configuration in configurations[movenumber]:
            tikzcode = gentikz(configuration.copy())
            for line in tikzcode:
                lines.append(line)
    lines.append(r"\end{document}")
    compile(lines, "some_text_file")


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
    lines = [r"\documentclass{article}", r"\usepackage[left = 0 cm, top = 0cm]{geometry}", r"\begin{document}"]
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
    lines.append(firstline)
    lines.append(secondline)
    line = r"$k\downarrow$"
    for n in range(1,nmax+1):
        line += "&"+str(n)

    for k in range(3,kmax+1):
        line += r"\\"
        lines.append(line)
        if k == 3:
            lines.append(hline)
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

    lines.append(line)
    lines.append(r"\end{tabular}")
    lines.append(r"\end{document}")
    name = str(n)+"_"+str(k)+sort+"_table"
    compile(lines, name)

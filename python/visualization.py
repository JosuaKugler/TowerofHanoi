import os
from total_possibilities import *
from moves_FS import *
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

    lineslist = [r"\vspace*{5cm}",
    r"\begin{tikzpicture}",
    r"\pgfmathsetlengthmacro\diskheight{" + str(min(10, 130/n))+r"};",
    r"\pgfmathsetmacro\k{"+str(k)+r"};", #define k in latex so it is easier to read
    r"\pgfmathsetlengthmacro\step{\textwidth/\k};",#define step which is simply the width divided by k
    r"\draw[color = white] (\step/2,0) -- (\textwidth+\step,0);",#make some space at the sides
    r"\foreach \n in {1,...,\k} \draw [fill = brown, draw = black, rounded corners = \step/20] (\step*\n,0) rectangle (\step*\n+\step/10,4.5);"#draw the pegs
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
    """
    compile lines and use a file with name as tex-file
    """
    with open("{}.tex".format(name), "w") as f:
        for line in lines:
            f.write(line+"\n")
    os.system("pdflatex {}.tex".format(name))
    os.system("xdg-open {}.pdf".format(name))
    os.system("rm {}.log".format(name))
    os.system("rm {}.aux".format(name))

def showlist(liste):
    """
    helper function for visualize
    """
    lines = []
    for configuration in liste:
        for line in gentikz(configuration.copy()):
            lines.append(line)
        lines.append(r"\newpage")
    return lines

def showconfigurations(configurations):
    """
    helper function for visualize
    """
    lines = []
    for movenumber in configurations:
        lines.append(str(movenumber) + r"\newline\par\noindent")
        for configuration in configurations[movenumber]:
            tikzcode = gentikz(configuration.copy())
            for line in tikzcode:
                lines.append(line)
        lines.append(r"\newpage")
    return lines

def showconfig(config):
    """
    visualizes one configuration given by configurationdict
    """
    lines = [r"\documentclass[tikz]{standalone}",
                  r"\usepackage{xcolor}", r"\usepackage{tikz,pgf}", r"\begin{document}"]
    newlines = gentikz(config)
    for line in newlines:
        lines.append(line)
    lines.append(r"\end{document}")
    return lines

def showmoveslist(disks, pegs, movelist):
    ST = TH(disks, pegs)
    for onemove in movelist:
        ST.move(onemove)
    lines = showlist(ST.history)
    return lines

def showmoveslists(disks, pegs, moveslists):
    lines = []
    for moveslist in moveslists:
        for line in showmoveslist(disks, pegs, moveslist):
            lines.append(line)
        lines.append(r"\newpage")
    return lines

def compareshowmoveslists(disks, pegs, movelists):
    """
    put all configurations after the same number of moves on the same page
    """
    movesdict = {}
    for n in range(len(movelists[0])+1):
        movesdict[n] = []
    for moveslist in movelists:
        ST = TH(disks, pegs)
        movesdict[0].append(ST.history[0])
        for n,onemove in enumerate(moveslist):
            ST.move(onemove)
            movesdict[n+1].append(ST.history[-1])
    lines = showconfigurations(movesdict)
    return lines

def nktable(nmax, kmax, sort = "value"):
    """
    create a latex table with the disks as columns and pegs as rows
    the entries of the table are specified by the parameter 'sort'
    sort value: the minimum number of moves to solve a configuration with n disks and k pegs
    sort increment: the increment of a configuration with n disks and k pegs
    sort possibilities/adjustedpossibilities/bfadjustedpossibilities/totalpossibilities:
    the number of possibilities to get to the finished state of a configuration with n disks and k pegs according to
    our first (wrong) conjecture with the FS-algorithm/our adjusted conjecture for the FS-algorithm/
    the bruteforce method for the number of possibilities with the FS-algorithm/the bruteforce method
    """
    number_of_columns = nmax
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
    lines = [firstline]
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
            elif sort == "bfadjustedpossibilities":
                line += "&"+str(bruteforceadjustedUpsilon(n,k))

    lines.append(line)
    lines.append(r"\end{tabular}")
    return lines

def checkdataformat(description, data):
    correct = True
    if description == "config":
        if type(data) != dict:
            correct = False
        else:
            for key in data:
                if type(key) != int:
                    correct = False
                dictelement = data[key]
                if type(dictelement) != list:
                    correct = False
                else:
                    for listelement in dictelement:
                        if type(listelement) != int:
                            correct = False
    elif description == "list":
        if type(data) != list:
            correct = False
        else:
            for listelement in data:
                if not checkdataformat('config', listelement):
                    correct = False
    elif description == "movelist":
        if type(data) != list:
            print("data = {} is type {} but should be type list".format(data, type(data)))
            correct = False
        else:
            if type(data[0]) != int:
                print("data[0] = {} is type {} but should be type int".format(data[0], type(data[0])))
                correct = False
            elif type(data[1]) != int:
                print("data[1] = {} is type {} but should be type int".format(data[1], type(data[1])))
                correct = False
            elif type(data[2]) != list:
                print("data[2] = {} is type {} but should be type list".format(data[2], type(data[2])))
                correct = False
            else:
                for n, onemove in enumerate(data[2]):
                    if type(onemove) != list:
                        print("data[2][{}] = {} is type {} but should be list".format(n, onemove, type(onemove)))
                        correct = False
                    else:
                        for k, number in enumerate(onemove):
                            if type(number) != int:
                                print("data[2][{}][{}] = {} is type {} but should be int".format(n, k, number, type(number)))
                                correct = False
    elif description == "configurations":
        if type(data) != dict:
            print("data = {} is type {} but should be dict".format(data, type(data)))
            correct = False
        else:
            for key in data:
                if type(key) != int:
                    correct = False
                dictelement = data[key]
                if not checkdataformat('list', dictelement):
                    correct = False
    elif description == "ptable" or description == "totalptable" or description == "incrementtable" or description == "movetable" or description == "bfptable":
        if type(data) != list:
            correct = False
        elif len(data) != 2:
            correct = False
        elif type(data[0])!= int or type(data[1])!= int:
            correct = False
    else:
        print("unknown description, can't check")
    return correct

def visualize(stuff, **options):
    """
    the visualize function aims to be the general function to visualize everything.
    pass a dictionary {description: data, nextdescription: nextdata) to it.

    ##################################################################
    #descriptions for the  'description: data' dictionary entry

    description='config':
        visualize a single configurationdict
        configurationdict := {peg1:[disk1, disk2],peg2:[disk3,disk4], ...} where disks and pegs are ints

    description='list':
        visualize a list of multiple configurationdict, useful for TH.history

    description='movelist':
        visualize a list of moves
        data: [disks, pegs, movelist]

    description='movelists':
    visualize a list of moveslists
    data: [disks, pegs, movelists]

    description='configurations':
        visualize a dict with integers as keys and lists containing configurations as objects

    description='movetable':
        table with M(n,k) where data[0] is the maximal 'n' and data[1] is the maximal 'k'

    description='incrementtable':
        table with I(n,k) where data[0] is the maximal 'n' and data[1] is the maximal 'k'

    description='totalptable':
        table with totalpossibilities(n,k) where data[0] is the maximal 'n' and data[1] is the maximal 'k'

    description='ptable':
        table with adjustedpossibilities(n,k) where data[0] is the maximal 'n' and data[1] is the maximal 'k'

    description="bfptable":
        table with bruteforceadjustedUpsilon(n,k) where data[0] is the maximal 'n' and data[1] is the maximal 'k'

    ##############################################################################################
    #keywords:
    separate: pass a latex command as string to this argument. It is called after each (description, data)-tupel.
        default r"\\newpage"

    name: file basename to write tex-code on it.
        default "some_text_file"

    ##############################################################################################
    example:
        visualize(('config', {0:[1,2,3],1:[4,5],2:[6],3:[]}),('movetable',[5,5]),('totalptable',[5,5]), separate = r"\par")
    """
    separate = r"\newpage" #by default, a new tupel is put on a new page
    name = "some_text_file" #by default this file is used
    for key in options:
        if key == "separate":
            separate = options[key]
        if key == "name":
            name = options[key]
    works = True
    totallines = [r"\documentclass{article}", r"\usepackage{xcolor}", r"\usepackage{tikz,pgf}", r"\usepackage[left = 0 cm, top = 0cm, bottom = 0cm, right = 2cm]{geometry}", r"\begin{document}", r"\pagestyle{empty}"]
    for description in stuff:
        data = stuff[description]
        if checkdataformat(description, data):
            if description == "config":
                lines = gentikz(data)
            elif description == "movelist":
                lines = showmoveslist(data[0], data[1], data[2])
            elif description == "movelists":
                lines = compareshowmoveslists(data[0], data[1], data[2])
            elif description == "list":
                lines = showlist(data)
            elif description == "configurations":
                lines = showconfigurations(data)
            elif description == "movetable":
                lines = nktable(data[0], data[1], sort = 'value')
            elif description == "incrementtable":
                lines = nktable(data[0], data[1], sort = 'increment')
            elif description == "totalptable":
                lines = nktable(data[0], data[1], sort = 'totalpossibilities')
            elif description == "ptable":
                lines = nktable(data[0], data[1], sort = 'adjustedpossibilities')
            elif description == "bfptable":
                lines = nktable(data[0], data[1], sort = 'bfadjustedpossibilities')
            else:
                print("unknown description")
                lines = []
            for line in lines:
                totallines.append(line)
            totallines.append(separate)
        else:
            print(description, ":", data, "don't match, please read help(visualization)")
            works = False
    totallines.append(r"\end{document}")
    if works:
        compile(totallines, name)
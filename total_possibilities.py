from help_calculate import M
import copy

configurations = {}# a dict with the number of moves as key and a list of interesting configurations that can be reached within the number of moves
success_instances = [] # a list with all instances that reached the finished state
idlist = []#a list of all THids

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
    - self.id: the id of this TH
    - self.disks: the number of disks
    - self.pegs: the number of pegs
    - self.configurationdict: a dict {0:[list with disks on peg 0], 1:[list with disks on peg 1], ...}
    - self.history: a list with the configurationdicts of previous THs leading to this instance
    - self.movenumber: the number of moves that is needed to get to this configuration
    - self.normalizedconfiguration: a configuration where the pegs are sorted according to their biggest disk
    and the function move to realize manual moving
    """

    def __init__(self, disks, pegs, configurationdict = None, history = []):
        """
        initializes a TH
        """
        self.id = self.__getid__()
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
        string =  str(self.id) + "TH"+ str(self.disks) + " "+ str(self.pegs) + " "+ str(self.normalizedconfiguration)
        return string

    def __str__(self):
        string =  """id: {}, {} disks, {} pegs, configuration: {}
        history:
        """.format(self.id, self.disks, self.pegs, self.configurationdict)
        for element in self.history:
            string += str(element) + "\n        "
        return string

    def __getid__(self):
        global idlist
        id = len(idlist)
        idlist.append(id)
        return id

    def move(self, movelist):
        """
        pass this function a move in the following format: [disk, startpeg, endpeg]
        """

        disk = movelist[0]
        startpeg = movelist[1]
        endpeg = movelist[2]
        #print("move", disk, "from", startpeg, "to", endpeg)
        newconfiguration = copy.deepcopy(self.configurationdict)
        newconfiguration[startpeg].remove(disk)
        newconfiguration[endpeg] = [disk]+newconfiguration[endpeg]
        self.history.append(newconfiguration)
        self.configurationdict = newconfiguration

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
    #process(ST)
    tryallpossibilities(ST)
    #now all possibilities for mv = 1 are created and saved if valid.
    #We can therefore iterate over all of them to create the possibilities of mv = 2 and so on
    maxmv = int((M(disks, pegs)-1)/2) ## NOTE: at maxmv the biggest disk has to be free and there has to be an empty peg
    for mv in range(1,maxmv+1):
        thismvconfigs = configurations[mv]
        for THobject in thismvconfigs:
            tryallpossibilities(THobject)
    return success_instances

def totalpossibilities(disks, pegs):
    """
    return the number of possibilities that is computed by the bruteforce method
    """
    bruteforce(disks, pegs)
    return len(success_instances)

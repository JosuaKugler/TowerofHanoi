#include <iostream>
#include <vector>
#include "help_calculate.h"

#include "config.h"

typedef std::vector<Move> Movevec;

//some DiskList stuff that might be useful
DiskListElem* find_disk(DiskList l, int disk)
{
    for (DiskListElem* p = l.first; p != 0; p = p->next)
    {
        if (p->value == disk)
        {
            return p;
        }
    }
    return 0;
}

int get_index(DiskList* l, int disk)
{
    int count = 0;
    for (DiskListElem* p = l->first; p != 0; p = p->next)
    {
        if (p->value == disk)
        {
            return count;
        }
        ++count;
    }
    return -1;
}

int mindisk(DiskList* disks)
{
    //list is not empty
    if (disks->first != 0)
    {
        int min = disks->first->value;
        for (DiskListElem* disk = disks->first->next; disk != 0; disk = disk->next)
        {
            if (disk->value < min)
            {
                min = disk->value;
            }            
        }
        return min;
    }
    else
    {
        return -1;
    }
}

int maxdisk(DiskList* disks)
{
    //list is not empty
    if (disks->first != 0)
    {
        int max = disks->first->value;
        for (DiskListElem* disk = disks->first->next; disk != 0; disk = disk->next)
        {
            if (disk->value > max)
            {
                max = disk->value;
            }            
        }
        return max;
    }
    else
    {
        return -1;
    }
}

void add_disk_ordered(DiskList* enddisks, int disknumber)
{
    //DiskListElem we want to insert
    DiskListElem* ins = new DiskListElem;
    ins->value = disknumber;
    //enddisks is not empty
    if (enddisks->first != 0)
    {
        for (DiskListElem* disk = enddisks->first; disk != 0; disk = disk->next)
        {
            //the appended disk doesn't have the biggest number
            if (disk->next != 0)
            {
                //disknumber is bigger than the current disk, but smaller than the next disk
                if (disk->value < disknumber and disk->next->value > disknumber)
                {
                    ins->next = disk->next;
                    disk->next = ins;
                    break;
                }
                //disknumber is smaller than all the other disks in this list
                else if (disk->value > disknumber)
                {
                    ins->next = enddisks->first;
                    enddisks->first = ins;
                    break;
                }
            }
            else
            {
                disk->next = ins;
                ins->next = 0;
            }
        }
    }
    else
    {
        enddisks->first = ins;
    }
    ++enddisks->count;
}

void pushdisk(DiskList* enddisks, int disknumber, int position)
{
    //DiskListElem we want to insert
    DiskListElem* ins = new DiskListElem;
    ins->value = disknumber;
    if (position != 0)
    {
        DiskListElem* disk = enddisks->first;
        for (size_t i = 1; i < position; ++i)
        {
            disk = disk->next;
        }
        disk->next = ins;
    }
    else
    {
        enddisks->first = ins;
    }
    ++enddisks->count;
}

int getdisk(DiskList* disks, int position)
{
    DiskListElem* disk = disks->first;
    for (size_t i = 0; i < position; ++i)
    {
        disk = disk->next;
    }
    return disk->value;
}

void removedisk(DiskList* startdisks, int disknumber)
{
    DiskListElem* previousdisk = 0;
    for (DiskListElem* disk = startdisks->first; disk != 0; disk = disk->next)
    {
        if (disk->value == disknumber)
        {
            if (previousdisk == 0)
            {
                startdisks->first = disk->next;
            }
            else
            {
                previousdisk->next = disk->next;
            }
            break;
        }
        previousdisk = disk;
    }
    --startdisks->count;
}

DiskList deepcopy(DiskList* disks)
{
    DiskList retlist;
    retlist.count = 0;
    for (int i = 0; i < disks->count; i++)
    {
        pushdisk(&retlist, getdisk(disks, i), i);
    }
    return retlist;
}

void printlist(DiskList* list)
{
    std::cout << "[ ";
    for (DiskListElem* i = list->first; i!=0; i = i->next)
    {
        std::cout << i->value << " ";
    }
    std::cout << "]" << std::endl;
}

bool is_equal_list(DiskList* firstlist, DiskList* secondlist)
{
    if (firstlist->count != secondlist->count)
    {
        return false;
    }
    else
    {
        DiskListElem* firstp = firstlist->first;
        DiskListElem* secondp = secondlist->first;
        for (size_t i = 0; i < firstlist->count; i++)
        {
            if (firstp->value != secondp->value)
            {
                return false;
            }
            firstp = firstp->next;
            secondp = secondp->next;
        }
    }
    return true;
}

Move newmove(int disk, int startpeg, int destinationpeg)
{
    Move move;
    move.disk = disk;
    move.startpeg = startpeg;
    move.destinationpeg = destinationpeg;
    return move;
}

void printmoves(Movevec moves)
{
    Movevec::const_iterator i;
    for (i = moves.begin(); i != moves.end(); i++)
    {
        std::cout << i->disk << ": " << i->startpeg << "->" << i->destinationpeg << ", ";
    }
    std::cout << std::endl;
}

Config::Config()
{
    _pegs = 0;
    _disks = 0;
    _firstpeg = 0;
}

Config::Config(int pegnumber, int disknumber)
{
    _pegs = pegnumber;
    _disks = disknumber;
    _firstpeg = new ConfigElem;
    _firstpeg->disks = new DiskList;
    _firstpeg->disks->count = _disks;
    _firstpeg->disks->first = new DiskListElem;
    DiskListElem* lastdisk = _firstpeg->disks->first;
    for (size_t i = 0; i < _disks-1; i++)
    {
        lastdisk->value = i;
        lastdisk->next = new DiskListElem;
        lastdisk = lastdisk->next;
    }
    lastdisk->value = _disks-1;
    
    ConfigElem* lastpeg = _firstpeg;
    for (size_t i = 1; i < _pegs; i++)
    {
        lastpeg->nextpeg = new ConfigElem;
        lastpeg = lastpeg->nextpeg;
        lastpeg->disks = new DiskList;
        lastpeg->disks->count = 0;
        lastpeg->disks->first = 0;
    }
}

Config::Config(int pegnumber, int disknumber, ConfigElem* firstpeg)
{
    _pegs = pegnumber;
    _disks = disknumber;
    _firstpeg = firstpeg;
}

Config::~Config()
{
    ConfigElem* current;
    ConfigElem* old;
    current = _firstpeg;
    for (size_t i = 0; i < _pegs; i++)
    {
        old = current;
        current = current->nextpeg;
        delete old->disks;
    }
}

int Config::pegnumber(){return _pegs;}

int Config::disknumber(){return _disks;}

int Config::diskposition(int diskvalue)
{
    if (diskvalue > _disks or diskvalue < 0)
    {
        std::cout << "disk value not in configuration range"<< std::endl;
        return -1;
    }
    else
    {
        ConfigElem* peg = _firstpeg;
        //iterate over all pegs
        for (size_t i = 0; i < _pegs; ++i)
        {
            //iterate over all disks on the current peg
            for (DiskListElem* disk = peg->disks->first; disk != 0; disk = disk->next)
            {
                if (disk->value == diskvalue)
                {
                    return i;
                };
            }
            peg = peg->nextpeg;
        }
    }
}

DiskList* Config::get_disks(int pegnumber)
{
    ConfigElem* peg = _firstpeg;
    //iterate until we get to pegnumber
    for (size_t i = 0; i < pegnumber; ++i)
    {
        peg = peg->nextpeg;
    }
    return peg->disks;
}

void Config::remove_disk(int disknumber, int pegnumber)
{
    DiskList* startdisks = get_disks(pegnumber);
    removedisk(startdisks, disknumber);
}

void Config::insert_disk(int disknumber, int pegnumber)
{
    DiskList* enddisks = get_disks(pegnumber);
    add_disk_ordered(enddisks, disknumber);
}

void Config::move_config(Move move)
{
    remove_disk(move.disk, move.startpeg);
    insert_disk(move.disk, move.destinationpeg);
}

void Config::print()
{
    for (size_t i = 0; i < _pegs; i++)
    {
        DiskList* disklist = get_disks(i);
        std::cout << "peg " << i << ": [";
        for (DiskListElem* disk = disklist->first; disk != 0; disk = disk->next)
        {
            std::cout << " " << disk->value;
        }
        std::cout << " ], ";
    }
    std::cout << std::endl;
}

Movevec Config::possiblemoves(int disk)
{
    int pegnumber = diskposition(disk);
    DiskList* disks = get_disks(pegnumber);
    Movevec moves;
    for (int peg = 0; peg < _pegs; peg++)
    {
        int currentmindisk = mindisk(get_disks(peg));
        if (disk < currentmindisk or currentmindisk == -1)
        {
            moves.push_back(newmove(disk, pegnumber, peg));
        }
    }
    return moves;
}

Movevec Config::allpossiblemoves()
{
    DiskList* mindisks = new DiskList;
    for (int peg = 0; peg < _pegs; peg++)
    {
        int currentmindisk = mindisk(get_disks(peg));
        pushdisk(mindisks, currentmindisk, peg);
    }

    Movevec moves;
    for (int startpeg = 0; startpeg < _pegs; startpeg++)
    {
        int currentdisk = getdisk(mindisks, startpeg);
        if (currentdisk != -1)
        {
            for (int destinationpeg = 0; destinationpeg < _pegs; destinationpeg++)
            {
                int destinationpegsize = getdisk(mindisks, destinationpeg);
                if (currentdisk < destinationpegsize or destinationpegsize == -1)
                {
                    moves.push_back(newmove(currentdisk, startpeg, destinationpeg));
                }
            }
        }
    }
    return moves;
}

Config Config::normalize()
{
    //get the maximum disk of each peg
    DiskList* maxdisks = new DiskList;
    for (int peg = 0; peg < _pegs; peg++)
    {
        int currentmaxdisk = maxdisk(get_disks(peg));
        pushdisk(maxdisks, currentmaxdisk, peg);
    }
    //get indices in order of ascending size
    //abuse of Disklist xD
    DiskList copymaxdisks = deepcopy(maxdisks);
    DiskList* basedisks = &copymaxdisks;
    DiskList* indices = new DiskList;
    for (int i = 0; i < _pegs; i++)
    {
        //get the biggest disk
        int currentmaxdisk = maxdisk(maxdisks);
        //problem: index in maxdisks shifts as we remove entrys
        int currentmaxindex = get_index(basedisks, currentmaxdisk);
        pushdisk(indices, currentmaxindex, i);
        removedisk(maxdisks, currentmaxdisk);
    }
    //create new Config with sorted pegs
    ConfigElem* firstpeg = new ConfigElem;
    ConfigElem* last = firstpeg;
    for (int i = 0; i < _pegs-1; i++)
    {
        //set p to the peg that is added next
        ConfigElem* p = _firstpeg;
        for (int j = 0; j < getdisk(indices, i); j++)
        {
            p = p->nextpeg;
        }
        last->disks = p->disks;
        last->nextpeg = new ConfigElem;
        last = last->nextpeg;
    }
    ConfigElem* p = _firstpeg;
    for (int j = 0; j < getdisk(indices, _pegs-1); j++)
    {
        p = p->nextpeg;
    }
    last->disks = p->disks;
    last->nextpeg = 0;
    return Config(_pegs, _disks, firstpeg);
}

bool Config::isequal(Config* compareconfig)
{
    if (this == compareconfig)
    {
        return true;
    }
    else if (_pegs != compareconfig->pegnumber() or _disks != compareconfig->disknumber())
    {
        return false;
    }
    else
    {
        for (int pegnumber = 0; pegnumber < _pegs; pegnumber++)
        {
            if (not is_equal_list(get_disks(pegnumber), compareconfig->get_disks(pegnumber)))
            {
                return false;
            }
        }
        return true;
    }
}

bool Config::normequal(Config* compareconfig)
{
    if (isequal(compareconfig))
    {
        return true;
    }
    else
    {
        Config firstconfig = normalize();
        Config secondconfig = compareconfig->normalize();
        bool ret = firstconfig.isequal(&secondconfig);
        return ret;
    }
}

int main()
{
    Config testconfig = Config(3,5);
    testconfig.print();
    testconfig.move_config(newmove(0,0,2));
    testconfig.print();
    Config newconfig = testconfig.normalize();
    newconfig.print();
    std::cout << newconfig.normequal(&testconfig);
    return 0;
}
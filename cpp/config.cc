#include <iostream>
#include "config.h"
#include "help_calculate.h"

//some IntList stuff that might be useful
IntListElem* find_first_x(IntList l, int x)
{
    for (IntListElem* p = l.first; p != 0; p = p->next)
    {
        if (p->value == x)
        {
            return p;
        }
    }
    return 0;
}

void insert_in_list(IntList* list, IntListElem* where, IntListElem* ins)
{
    if (where == 0)
    {
        ins->next = list->first;
        list->first = ins;
        ++list->count;
    }
    else
    {
        ins->next = where->next;
        where->next = ins;
        list->count = list->count + 1;
    }
}

IntListElem* remove_from_list(IntList* list, IntListElem* where)
{
    IntListElem* p;

    if (where == 0)
    {
        p = list->first;
        if (p != 0)
        {
            list->first = p->next;
            list->count = list->count - 1;
        }
        return p;
    }

    p = where->next;
    if(p != 0)
    {
        where->next = p->next;
        list->count = list->count - 1;
    }
    return p;
}

Move newmove(int disk, int startpeg, int destinationpeg)
{
    Move move;
    move.disk = disk;
    move.startpeg = startpeg;
    move.destinationpeg = destinationpeg;
    return move;
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
    _firstpeg->disks = new IntList;
    _firstpeg->disks->count = _disks;
    _firstpeg->disks->first = new IntListElem;
    IntListElem* lastdisk = _firstpeg->disks->first;
    for (size_t i = 0; i < _disks-1; i++)
    {
        lastdisk->value = i;
        lastdisk->next = new IntListElem;
        lastdisk = lastdisk->next;
    }
    lastdisk->value = _disks-1;
    
    ConfigElem* lastpeg = _firstpeg;
    for (size_t i = 1; i < _pegs; i++)
    {
        lastpeg->nextpeg = new ConfigElem;
        lastpeg = lastpeg->nextpeg;
        lastpeg->disks = new IntList;
        lastpeg->disks->count = 0;
        lastpeg->disks->first = 0;
    }
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
            for (IntListElem* disk = peg->disks->first; disk != 0; disk = disk->next)
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

IntList* Config::get_disks(int pegnumber)
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
    IntList* startdisks = get_disks(pegnumber);
    IntListElem* previousdisk = 0;
    for (IntListElem* disk = startdisks->first; disk != 0; disk = disk->next)
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

void Config::insert_disk(int disknumber, int pegnumber)
{
    //IntListElem we want to insert
    IntListElem* ins = new IntListElem;
    ins->value = disknumber;
    //List where it has to be inserted
    IntList* enddisks = get_disks(pegnumber);
    if (enddisks->first != 0)
    {
        for (IntListElem* disk = enddisks->first; disk != 0; disk = disk->next)
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

void Config::move_config(Move move)
{
    remove_disk(move.disk, move.startpeg);
    insert_disk(move.disk, move.destinationpeg);
}

void Config::print()
{
    for (size_t i = 0; i < _pegs; i++)
    {
        IntList* disklist = get_disks(i);
        std::cout << "peg " << i << ": [";
        for (IntListElem* disk = disklist->first; disk != 0; disk = disk->next)
        {
            std::cout << " " << disk->value;
        }
        std::cout << " ], ";
    }
    std::cout << std::endl;
}

int main()
{
    Config testconfig = Config(3,5);
    testconfig.print();
    testconfig.move_config(newmove(0,0,2));
    testconfig.print();
    return 0;
}
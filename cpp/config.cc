#include <iostream>
#include <vector>
#include "config.h"

Move newmove(int disk, int startpeg, int destinationpeg)
{
    Move move;
    move.disk = disk;
    move.startpeg = startpeg;
    move.destinationpeg = destinationpeg;
    return move;
}

void printmoves(std::vector<Move> moves)
{
    std::vector<Move>::const_iterator i;
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
    _firstpeg->disks = new MyList(disknumber);
    ConfigElem* lastpeg = _firstpeg;
    for (size_t i = 1; i < _pegs; i++)
    {
        lastpeg->nextpeg = new ConfigElem;
        lastpeg = lastpeg->nextpeg;
        lastpeg->disks = new MyList;
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
            if (peg->disks->get_index(diskvalue) != -1)
            {
                return i;
            }
            peg = peg->nextpeg;
        }
    }
}

MyList* Config::get_disks(int pegnumber)
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
    MyList* startdisks = get_disks(pegnumber);
    startdisks->remove_val(disknumber);
}

void Config::insert_disk(int disknumber, int pegnumber)
{
    MyList* enddisks = get_disks(pegnumber);
    enddisks->append_ordered(disknumber);
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
        MyList* disklist = get_disks(i);
        std::cout << "peg " << i << ": [";
        for (int i = 0; i < disklist->len(); ++i)
        {
            std::cout << " " <<disklist->get_val(i);
        }
        std::cout << " ], ";
    }
    std::cout << std::endl;
}

std::vector<Move> Config::possiblemoves(int disk)
{
    int pegnumber = diskposition(disk);
    MyList* disks = get_disks(pegnumber);
    std::vector<Move> moves;
    for (int peg = 0; peg < _pegs; peg++)
    {
        int currentmindisk = get_disks(peg)->min_val();
        if (disk < currentmindisk or currentmindisk == -1)
        {
            moves.push_back(newmove(disk, pegnumber, peg));
        }
    }
    return moves;
}

std::vector<Move> Config::allpossiblemoves()
{
    MyList* mindisks = new MyList;
    for (int peg = 0; peg < _pegs; peg++)
    {
        int currentmindisk = get_disks(peg)->min_val();
        //pushdisk(mindisks, currentmindisk, peg);
        mindisks->append(currentmindisk);
    }

    std::vector<Move> moves;
    for (int startpeg = 0; startpeg < _pegs; startpeg++)
    {
        int currentdisk = mindisks->get_val(startpeg);
        if (currentdisk != -1)
        {
            for (int destinationpeg = 0; destinationpeg < _pegs; destinationpeg++)
            {
                int destinationpegsize = mindisks->get_val(destinationpeg); //getdisk(mindisks, destinationpeg);
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
    MyList* maxdisks = new MyList;
    for (int peg = 0; peg < _pegs; peg++)
    {
        int currentmaxdisk = get_disks(peg)->max_val();
        //pushdisk(maxdisks, currentmaxdisk, peg);
        maxdisks->insert_at_index(currentmaxdisk, peg);
    }
    //get indices in order of ascending size
    //DiskList copymaxdisks = deepcopy(maxdisks);
    //DiskList* basedisks = &copymaxdisks;

    MyList* basedisks = new MyList(*maxdisks);
    MyList* indices = new MyList;
    for (int i = 0; i < _pegs; i++)
    {
        //get the biggest disk
        int currentmaxdisk = maxdisks->max_val();
        //problem: index in maxdisks shifts as we remove entrys
        int currentmaxindex = basedisks->get_index(currentmaxdisk);//get_index(basedisks, currentmaxdisk);
        //pushdisk(indices, currentmaxindex, i);
        indices->insert_at_index(currentmaxindex, i);
        //removedisk(maxdisks, currentmaxdisk);
        maxdisks->remove_val(currentmaxdisk);
    }
    //create new Config with sorted pegs
    ConfigElem* firstpeg = new ConfigElem;
    ConfigElem* last = firstpeg;
    for (int i = 0; i < _pegs-1; i++)
    {
        //set p to the peg that is added next
        ConfigElem* p = _firstpeg;
        for (int j = 0; j < indices->get_val(i); j++)
        {
            p = p->nextpeg;
        }
        last->disks = p->disks;
        last->nextpeg = new ConfigElem;
        last = last->nextpeg;
    }
    ConfigElem* p = _firstpeg;
    for (int j = 0; j < indices->get_val(_pegs-1); j++)
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
            if (not get_disks(pegnumber)->is_equal(*(compareconfig->get_disks(pegnumber))))
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
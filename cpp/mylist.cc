#include "mylist.h"
#include <string>

MyList::MyList()
{
    _count = 0;
    _firstElem = 0;   
};

MyList::MyList(int count)
{
    _count = 0;
    _firstElem = 0;
    for (size_t i = 0; i < count; i++)
    {
        this->append(i);
    }
}

MyList::MyList(MyList& list)
{
    _count = list.len();
    if (_count != 0)
    {
        _firstElem = new MyListElem;
        _firstElem->value = list.get_val(0);
        MyListElem* p = _firstElem;
        for (int i = 1; i < list.len(); i++)
        {
            p->next = new MyListElem;
            p = p->next;
            p->value = list.get_val(i);
        }
        p = 0;
    }
    else
    {
        _firstElem = 0;
    }
}

MyList::~MyList()
{
    _count = 0;
    _firstElem = 0;
}

int MyList::len()
{
    return _count;
}

int MyList::get_index(int val)
{
    int count = 0;
    for (MyListElem* p = _firstElem; p != 0; p = p->next)
    {
        if (p->value == val)
        {
            return count;
        }
        ++count;
    }
    return -1;
}

int MyList::get_val(int index)
{
    MyListElem* disk = _firstElem;
    for (int i = 0; i < index; ++i)
    {
        disk = disk->next;
    }
    return disk->value;
}

int MyList::min_val()
{
    //list is not empty
    if (_firstElem != 0) //or _count > 0
    {
        int min = _firstElem->value;
        for (MyListElem* disk = _firstElem->next; disk != 0; disk = disk->next)
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

int MyList::max_val()
{
    //list is not empty
    if (_firstElem != 0)
    {
        int max = _firstElem->value;
        for (MyListElem* disk = _firstElem->next; disk != 0; disk = disk->next)
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

void MyList::append_ordered(int val)
{
    //MyListElem we want to insert
    MyListElem* ins = new MyListElem;
    ins->value = val;
    //enddisks is not empty
    if (_firstElem != 0)
    {
        for (MyListElem* disk = _firstElem; disk != 0; disk = disk->next)
        {
            //the appended disk doesn't have the biggest number
            if (disk->next != 0)
            {
                //disknumber is bigger than the current disk, but smaller than the next disk
                if (disk->value < val and disk->next->value > val)
                {
                    ins->next = disk->next;
                    disk->next = ins;
                    break;
                }
                //disknumber is smaller than all the other disks in this list
                else if (disk->value > val)
                {
                    ins->next = _firstElem;
                    _firstElem = ins;
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
        _firstElem = ins;
    }
    ++_count;
}

void MyList::insert_at_index(int val, int index)
{
    //MyListElem we want to insert
    MyListElem* ins = new MyListElem;
    ins->value = val;
    if (index != 0)
    {
        MyListElem* disk = _firstElem;
        for (int i = 1; i < index; ++i)
        {
            disk = disk->next;
        }
        ins->next = disk->next;
        disk->next = ins;
    }
    else
    {
        ins->next = _firstElem;
        _firstElem = ins;
    }
    ++_count;
}

void MyList::append(int val)
{
    insert_at_index(val, _count);
}

void MyList::remove_at_index(int index)
{
    if (index != 0)
    {
        MyListElem* disk = _firstElem;
        for (int i = 1; i < index; ++i)
        {
            disk = disk->next;
        }
        disk->next = disk->next->next;
    }
    else
    {
        _firstElem = _firstElem->next;
    }
    --_count;
}

void MyList::remove_val(int val)
{
    MyListElem* previousdisk = 0;
    for (MyListElem* disk = _firstElem; disk != 0; disk = disk->next)
    {
        if (disk->value == val)
        {
            if (previousdisk == 0)
            {
                _firstElem = disk->next;
            }
            else
            {
                previousdisk->next = disk->next;
            }
            break;
        }
        previousdisk = disk;
    }
    --_count;
}

std::string MyList::to_string()
{
    std::string retstring =  "[ ";
    for (MyListElem* i = _firstElem; i!=0; i = i->next)
    {
        retstring += std::to_string(i->value) + " ";
    }
    retstring += "]";
    return retstring;
}

bool MyList::is_equal(MyList& list)
{
    if (_count != list.len())
    {
        return false;
    }
    else
    {
        MyListElem* firstp = _firstElem;
        MyListElem* secondp = list._firstElem;
        for (int i = 0; i < _count; i++)
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
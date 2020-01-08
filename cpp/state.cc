#include "config.cc"
#include "state.h"
#include "help_calculate.h"
#include<iostream>


//important:
// add_child as function in order to add children from outside
// set_parent also as outside function? no, just add prevstate in constructor

State::State()
{
    movenumber = 0;
    config = new Config;
    prevstate = 0;
    prevmove = 0;
    nextstate = 0;
    index_in_master = -1;
}

State::State(int pegnumber, int disknumber)
{
    movenumber = 0;
    config = new Config(pegnumber, disknumber);
    prevstate = 0;
    prevmove = 0;
    nextstate = 0;
    index_in_master = -1;
}

State::State(State* oldstate, Move* newmove)
{
    movenumber = oldstate->get_movenumber() + 1;
    config = new Config(oldstate->get_config());
    config->move_config(*newmove);
    prevstate = oldstate;
    prevmove = newmove;
    nextstate = 0;
    index_in_master = -1;
}

State::~State()
{
    config = 0;
    prevmove = 0;
    nextstate = 0;
    //eliminate reference to this object in prevstate
    StateListElem* list = prevstate->nextstate;
    StateListElem* previous = 0;
    for (StateListElem* p = list; p != 0; p = p->next)
    {
        if (p->state = this)
        {
            if (previous == 0)
            {
                prevstate->nextstate = p->next;
            }
            else
            {
                previous->next = p->next;
            }
            break;
        }
        previous = p;
    }
    //if there are no children left for prevstate delete it
    /* if (list == 0)
    {
        delete prevstate;
    } */
    prevstate = 0;
}

Config* State::get_config()
{
    return config;
}

int State::get_movenumber()
{
    return movenumber;
}

State* State::get_prevstate()
{
    return prevstate;
}

Move* State::get_prevmove()
{
    return prevmove;
}

StateListElem* State::get_nextstate()
{
    return nextstate;
}

std::string State::to_string(bool all)
{
    std::string retstring = "State " + std::to_string(movenumber) + ": " + config->to_string() + "\n";
    retstring += move_to_string(prevmove);
    if (all)
    {
        State* p = prevstate;
        for (size_t i = 0; i < movenumber; i++)
        {
            retstring += "\n      " + std::to_string(p->get_movenumber()) + ": " + p->get_config()->to_string() + "\n";
            retstring += move_to_string(p->prevmove);
            p = p->prevstate;
        }
    }
    return retstring;
}

bool State::check(std::vector<std::vector<State*>>* master)
{
    ///can it be reached with less moves?
    for (size_t i = 0; i < movenumber; i++)
    {
        std::vector<State*> i_reach_states = master->at(i);
        for (size_t j = 0; j < i_reach_states.size(); j++)
        {
            State* i_j_state = i_reach_states.at(j);
            if (i_j_state != 0)
            {
                Config* comparison = i_j_state->get_config();
                //std::cout << comparison->to_string();
                if (config->normequal(comparison))
                {
                    //std::cout << comparison->to_string();
                    return false;
                }
            }
        }
    }

    //it isn't finished but took maxmoves
    int maxmoves = (M(config->disknumber(), config->pegnumber())-1)/2;
    //only biggest disk is left on peg 0
    bool bigalone = false;
    if (config->get_disks(0)->len() == 1)
    {
        bigalone = true;
    }
    else if (movenumber == maxmoves) // if it took maxmoves but isn't finished, it's not optimal
    {
        return false;
    }

    //\exists empty peg
    bool oneempty = false;
    for (int peg = 1; peg < config->pegnumber(); peg++)
    {
        if(config->get_disks(peg)->len() == 0)
        {
            oneempty = true;
        }
    }
    if (!oneempty and movenumber == maxmoves) //if it isn't finished but took maxmoves, then it's not optimal
    {
        return false;
    }
    return true;
}

//try if implementation works, otherwise change laststate->next stuff
void State::add_child(State* child)
{
    if (nextstate == 0)
    {
        nextstate = new StateListElem;
        nextstate->state = child;
        nextstate->next = 0;
    }
    else
    {
        StateListElem* laststate;
        for (StateListElem* p = nextstate; p != 0; p = p->next)
        {laststate = p;}
        laststate->next = new StateListElem;
        laststate->next->state = child;
        laststate->next->next = 0;
    }
}

int State::get_index()
{
    return index_in_master;
}

void State::set_index(int index)
{
    index_in_master = index;
}
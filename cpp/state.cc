#include "config.cc"
#include "state.h"
#include "help_calculate.h"
#include<iostream>

State::State()
{
    movenumber = 0;
    config = new Config;
    prevstate = 0;
    prevmove = 0;
    nextstate = 0;
    optimal = true;
}

State::State(int pegnumber, int disknumber)
{
    movenumber = 0;
    config = new Config(pegnumber, disknumber);
    prevstate = 0;
    prevmove = 0;
    nextstate = 0;
    optimal = true;
}

State::State(State* oldstate, Move* newmove)
{
    movenumber = oldstate->get_movenumber() + 1;
    config = new Config(oldstate->get_config());
    config->move_config(*newmove);
    prevstate = oldstate;
    prevmove = newmove;
    nextstate = 0;
    optimal = true;
}

/* State::~State()
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
    prevstate = 0;
} */

Config* State::get_config()
{
    return config;
}

int State::get_movenumber()
{
    return movenumber;
}

bool State::is_optimal()
{
    return optimal;
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
            if (config->normequal(i_j_state->get_config()))
            {
                optimal = false;
                return false;
            }
        }
    }

    int maxmoves = (M(config->disknumber(), config->pegnumber())-1)/2;
    //only biggest disk is left on peg 0
    bool bigalone = false;
    if (config->get_disks(0)->len() == 1)
    {
        bigalone = true;
    }
    else if (movenumber == maxmoves) // if it took maxmoves but isn't finished, it's not optimal
    {
        optimal = false;
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

void State::newlayer(std::vector<std::vector<State*>>* master)
{
    std::vector<Move> allmoves = config->allpossiblemoves();
    //debug
    printmoves(allmoves);
    nextstate = new StateListElem;
    StateListElem* p = nextstate;
    for (size_t i = 0; i < allmoves.size(); i++)
    {
        Move currentmove = allmoves.at(i);
        p->state = new State(this, &currentmove);
        if (p->state->check(master))
        {
            p->next = new StateListElem;
            p = p->next;   
        }
        else
        {
            p->state = 0;
        }
    }
    //p points to a new StateListElem, but we want it to be 0
    p = 0;
    //check if there are children at all
    if (nextstate == 0)
    {
        optimal = false;
    }
    else
    {
        //store elements of nextstate list in master[movenumber + 1]
        for (StateListElem* p = nextstate; p != 0; p = p->next)
        {
            master->at(movenumber + 1).push_back(p->state);
        }
    }
}
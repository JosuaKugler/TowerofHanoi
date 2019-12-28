#include "state.h"
#include<iostream>

State::State()
{
    movenumber = 0;
    config = new Config;
    laststate = 0;
}

State::State(int pegnumber, int disknumber)
{
    movenumber = 0;
    config = new Config(pegnumber, disknumber);
    laststate = 0;
}

State::State(State* oldstate, Move move)
{
    movenumber = oldstate->get_movenumber() + 1;
    config = new Config(oldstate->get_config());
    config->move_config(move);
    laststate = oldstate;
}

Config* State::get_config()
{
    return config;
}

int State::get_movenumber()
{
    return movenumber;
}

State* State::get_laststate()
{
    return laststate;
}

std::string State::to_string(bool all)
{
    std::string retstring = "State " + std::to_string(movenumber) + ": " + config->to_string() + "\n";
    if (all)
    {
        State* p = laststate;
        for (size_t i = 0; i < movenumber; i++)
        {
            retstring += "      " + std::to_string(p->get_movenumber()) + ": " + p->get_config()->to_string() + "\n";
            p = p->laststate;
        }
    }
    return retstring;
}

int main()
{
    State test = State(3,5);
    std::cout << test.to_string(true);
    Move move;
    move.disk = 0;
    move.destinationpeg = 2;
    move.startpeg = 0;
    State test2 = State(&test, move);
    std::cout << test2.to_string(true);
    return 0;
}
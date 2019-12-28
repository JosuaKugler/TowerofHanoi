#include "config.cc"

class State
{
public:
    State();
    //new state with standard config
    State(int pegnumber, int disknumber);
    //state basing on a preceding state, is created by performing move on oldstate
    State(State* oldstate, Move move);
    //~State();
    int get_movenumber();
    Config* get_config();
    State* get_laststate();
    //return a string with config
    //if all: add all lastconfigs to the string
    std::string to_string(bool all);
private:
    int movenumber;
    Config* config;
    State* laststate;
};
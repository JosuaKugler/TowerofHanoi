struct StateListElem;

class State
{
public:
    State();
    //new state with standard config
    State(int pegnumber, int disknumber);
    //state basing on a preceding state, is created by performing move on oldstate
    State(State* oldstate, Move* move);
    //~State();
    int get_movenumber();
    bool is_optimal();
    Config* get_config();
    State* get_prevstate();
    Move* get_prevmove();
    StateListElem* get_nextstate();
    //return a string with config
    //if all: add all lastconfigs to the string
    std::string to_string(bool all);
    //check if there are nextstates, 
    //if not this object can be deleted 
    //and the parent object has to do the childrencheck
    void childrencheck();
    //check if this state can lead to the maximum number of moves
    bool check(std::vector<std::vector<State*>>* master);
    //create nextstates
    void newlayer(std::vector<std::vector<State*>>* master);
    //following states
    StateListElem* nextstate;
private:
    int movenumber;
    Config* config;
    State* prevstate;
    Move* prevmove;
    //can this State be element of an optimal movesequence?
    //is important where check(config) returns true,
    //but check(state) = false forall state in nextstates, 
    //so this state can't be optimal
    bool optimal;
};

struct StateListElem
{
    State* state;
    StateListElem* next;
};
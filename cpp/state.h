//idea: add master position to class to avoid searching

struct StateListElem;

class State
{
public:
    State();
    //new state with standard config
    State(int pegnumber, int disknumber);
    //state basing on a preceding state, is created by performing move on oldstate
    State(State* oldstate, Move* move);
    ~State();
    int get_movenumber();
    Config* get_config();
    State* get_prevstate();
    Move* get_prevmove();
    int get_index();
    void set_index(int index);
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
    void add_child(State* child);
private:
    int movenumber;
    Config* config;
    State* prevstate;
    Move* prevmove;
    int index_in_master;
    //following states
    StateListElem* nextstate;
};

struct StateListElem
{
    State* state;
    StateListElem* next;
};
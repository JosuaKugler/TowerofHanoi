#include "state.cc"

typedef std::vector<Move> Movevec;

std::vector<std::vector<State>> Hello;

void print(std::vector<std::vector<State*>>* master)
{
    std::cout << "[";
    for (size_t movenumber = 0; movenumber < master->size(); movenumber++)
    {
        std::cout << std::endl;
        std::vector<State*> movenumber_reach_list = master->at(movenumber);
        std::cout << "    [";
        for (size_t i = 0; i < movenumber_reach_list.size(); i++)
        {
            std::cout << std::endl << "    " << movenumber_reach_list.at(i)->to_string(false);
        }
        std::cout << "    ]";
    }
    std::cout << std::endl << "]" << std::endl;
}

void run(int pegnumber, int disknumber)
{
    int maxmoves = (M(disknumber, pegnumber) -1)/2;
    std::vector<std::vector<State*>> realmaster(maxmoves);
    //std::vector<std::vector<State*>>* master = new std::vector<std::vector<State*>>(maxmoves);
    std::vector<std::vector<State*>>* master = &realmaster;
    print(master);
    State* firststate = new State(pegnumber, disknumber);
    master->at(0).push_back(firststate);
    print(master);
    firststate->newlayer(master);
    //print(master);
}


int main()
{
    int maxmoves = (M(5, 3) -1)/2;
    std::vector<std::vector<State*>> realmaster(maxmoves);
    std::vector<std::vector<State*>>* master = &realmaster;
    //run(3,5);
    State* test = new State(3,5);
    master->at(0).push_back(test);
    std::vector<Move> allmoves = test->get_config()->allpossiblemoves();
    test->nextstate = new StateListElem;
    StateListElem* p  = test->get_nextstate();
    print(master);
    for (size_t i = 0; i < allmoves.size(); i++)
    {
        Move currentmove = allmoves.at(i);
        p->state = new State(test, &currentmove);
        std::cout << p->state->to_string(true);
        //if (p->state->check(master))
        if(true)
        {
            p->next = new StateListElem;
            p = p->next;   
        }
        else
        {
            p->state = 0;
        }
    }
    p = 0;
    //check if there are children at all
    if (not test->nextstate == 0);
    {
        //store elements of nextstate list in master[movenumber + 1]
        for (StateListElem* p = test->nextstate; p != 0; p = p->next)
        {
            master->at(test->get_movenumber() + 1).push_back(p->state);
        }
    }
    print(master);
    return 0;
}
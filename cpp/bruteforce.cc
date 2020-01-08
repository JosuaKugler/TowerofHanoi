#include "state.cc"

//idea: operate in master, create new objects from master and collect the pointers inside master.
//Only delete from master with masterremove
//In destructor, delete all the pointers in parent structures that may point to this instance
//also in destructor, if object is the only child of another object, also delete the other object



typedef std::vector<Move> Movevec;
typedef std::vector<std::vector<State*>> mastertype;

//std::vector<std::vector<State>> Hello;

void print(mastertype* master)
{
    std::cout << "[";
    for (size_t movenumber = 0; movenumber < master->size(); movenumber++)
    {   
        std::vector<State*> movenumber_reach_list = master->at(movenumber);
        std::cout << std::endl;
        std::cout << "    [";
        for (size_t i = 0; i < movenumber_reach_list.size(); i++)
        {
            State* instance = movenumber_reach_list.at(i);
            if (instance != 0)
            {
                std::cout << std::endl << "    " << movenumber_reach_list.at(i)->to_string(false);
            }
        }
        std::cout << "    ]";
    }
    std::cout << std::endl << "]" << std::endl;
}


/* 
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
} */

/* 
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
} */

void master_remove(mastertype* master, int layer, int index)
{
    delete master->at(layer).at(index);
    master->at(layer).at(index) = NULL;
}

void make_children_else_destroy_parents_recursively(mastertype* master, int currentlayer, int index_of_parent)
{
    State* parent = master->at(currentlayer).at(index_of_parent);
    //create all children of parent and add them to the next layer of master
    std::vector<Move> allmoves = parent->get_config()->allpossiblemoves();
    for (size_t i = 0; i < allmoves.size(); i++)
    {
        print(master);
        Move currentmove = allmoves.at(i);
        State* child = new State(parent, &currentmove);
        bool optimal = child->check(master);
        if (optimal)
        {
            int size = master->at(currentlayer + 1).size();
            child->set_index(size);
            master->at(currentlayer + 1).push_back(child);
            //add child to parent instance, child reference to parent is already finished because of constructor
            parent->add_child(child);
        }
        else
        {
            delete child;
        }
    }
    //check if there are children at all
    if (parent->get_nextstate() == 0)
    {
        master_remove(master, currentlayer, index_of_parent);
    }
}

void run()
{
    int maxmoves = (M(5, 3) -1)/2;
    std::vector<std::vector<State*>> realmaster(maxmoves);
    std::vector<std::vector<State*>>* master = &realmaster;
    State* first = new State(3,5);
    first->set_index(0);
    master->at(0).push_back(first);
    State* parent = master->at(0).at(0);
    //std::cout << parent->get_config()->isequal(first->get_config());
    //create all children of parent and add them to the next layer of master
    std::vector<Move> allmoves = parent->get_config()->allpossiblemoves();
    Move currentmove = allmoves.at(0);
    State* child = new State(first, &currentmove);
    bool optimal = child->check(master);
    //make_children_else_destroy_parents_recursively(master, 0, 0);
    print(master);
}

int main()
{
    run();
    return 0;
}
<<<<<<< HEAD
#include "help_calculate.h"
//#include "state.cc"
=======
#include "state.cc"

//idea: operate in master, create new objects from master and collect the pointers inside master.
//Only delete from master with masterremove
//In destructor, delete all the pointers in parent structures that may point to this instance
//also in destructor, if object is the only child of another object, also delete the other object

typedef std::vector<Move> Movevec;
typedef std::vector<std::vector<State*>> mastertype;

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

void master_remove(mastertype* master, int layer, int index)
{
    delete master->at(layer).at(index);
    master->at(layer).at(index) = NULL;
}

void make_children(mastertype* master, int currentlayer, int index_of_parent)
{
    State* parent = master->at(currentlayer).at(index_of_parent);
    //create all children of parent and add them to the next layer of master
    std::vector<Move> allmoves = parent->get_config()->allpossiblemoves();
    for (size_t i = 0; i < allmoves.size(); i++)
    {
        Move* currentmovepointer = &(allmoves.at(i));
        State* child = new State(parent, currentmovepointer);
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
}

void newlayer(mastertype* master, int currentlayer)
{
    for (size_t i = 0; i < master->at(currentlayer).size(); ++i)
    {
        if (master->at(currentlayer).at(i) != 0)
        {
            make_children(master, currentlayer, i);
        }
    }
}

void run()
{
    int maxmoves = (M(5, 3) +1)/2;
    std::vector<std::vector<State*>> realmaster(maxmoves);
    std::vector<std::vector<State*>>* master = &realmaster;
    State* first = new State(3,5);
    first->set_index(0);
    master->at(0).push_back(first);
    for (size_t i = 0; i < maxmoves - 1; i++)
    {
        newlayer(master, i);
    }
    print(master);
}
>>>>>>> secondbfattempt

int main()
{
    run();
    return 0;
}
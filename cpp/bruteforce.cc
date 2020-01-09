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
        std::cout << move_to_string(&currentmove);
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
    make_children_else_destroy_parents_recursively(master, 0, 0);
    print(master);
}

int main()
{
    run();
    return 0;
}
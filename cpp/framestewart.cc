#include "help_calculate.h"
#include "config.cc"

typedef std::vector<Move> Movevec;

//returns the moves to solve a startconfiguration according to frame-stewart
Movevec framestewart(int pegnumber, int disknumber)
{
    
}

int main()
{
    Config testconfig = Config(3,5);
    testconfig.move_config(newmove(0,0,2));
    testconfig.print();
    Config newconfig = testconfig.normalize();
    newconfig.print();
    Config* testconfigpointer = &testconfig;
    std::cout << newconfig.normequal(testconfigpointer);
    return 0;
}
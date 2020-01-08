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
    std::cout << testconfig.to_string();
    Config newconfig = testconfig.normalize();
    std::cout << newconfig.to_string();
    Config* testconfigpointer = &testconfig;
    std::cout << newconfig.normequal(testconfigpointer);
    return 0;
}
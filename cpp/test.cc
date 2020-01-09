#include<vector>
int main()
{
    std::vector<std::vector<int*>>* test = new std::vector<std::vector<int*>>(3);
    int hi = 5;
    int hi2 = 6;
    int hi3 = 7;
    int* pointer = &hi;
    int* pointer2 = &hi2;
    int* pointer3 = &hi3;
    test->at(0) = std::vector<int*>(2);
    test->at(0).at(0) = pointer;
    test->at(0).at(1) = pointer2;
    test->at(1) = std::vector<int*>(1);
    test->at(1).at(0) = pointer3;
    std::vector<int*> test2 = test->at(0);
    return 0;
}
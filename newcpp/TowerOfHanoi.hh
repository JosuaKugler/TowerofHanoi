#include<vector>

using namespace std;

struct Move
{
    int disk;
    int destination;
};

struct FullMove
{
    int disk;
    int destination;
    int origin;
};

class TowerOfHanoi {
    public:
        TowerOfHanoi(int n, int k);
        TowerOfHanoi(int n, int k, int* config);
        TowerOfHanoi(TowerOfHanoi& tower);
        ~TowerOfHanoi();

        int get_n() {return _n;}
        int get_k() {return _k;}
        int* get_config() {return _config;}

        bool move(Move move);
        bool move(FullMove move);
        bool move(int disk, int destination);
        bool move(int disk, int destination, int origin);

    private:
        int _n;
        int _k;
        int *_config;
};
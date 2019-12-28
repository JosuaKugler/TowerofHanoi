#include "mylist.cc"

struct Move
{
    int disk;
    int startpeg;
    int destinationpeg;
};

struct ConfigElem
{
    ConfigElem* nextpeg;
    MyList* disks;
};

class Config
{
public:
    //initializes an empty configuration
    Config();
    //initializes a configuration with all disks on the first peg
    Config(int pegnumber, int disknumber);
    //initializes a configuration with _firstpeg pointing to firstpeg
    Config(int pegnumber, int disknumber, ConfigElem* firstpeg);
    //Destructor
    ~Config();
    //returns the number of pegs
    int pegnumber();
    //returns the number of disks
    int disknumber();
    //returns the peg a disk is positioned on
    int diskposition(int disk);
    //returns an Intlist* with the disks on peg
    MyList* get_disks(int peg);
    //inserts the disk in the list of peg
    void insert_disk(int disk, int peg);
    //remove the disk from the list of the peg
    void remove_disk(int disk, int peg);
    //changes the configuration by performing Move
    void move_config(Move move);
    //print the configuration
    void print();
    //return a vector containing all possible moves of this disk
    std::vector<Move> possiblemoves(int disk);
    //return a vector containing all possible moves of all disks
    std::vector<Move> allpossiblemoves();
    //return the normalized configuration as a new Config
    Config normalize();
    //test whether two configurations are exactly equal
    bool isequal(Config* compareconfig);
    //test whether two configurations are equal according to our normalization
    bool normequal(Config* compareconfig);
private:
    int _pegs;
    int _disks;
    ConfigElem* _firstpeg;
};
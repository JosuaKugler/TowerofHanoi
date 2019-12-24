struct IntListElem
{
    IntListElem* next;
    int value;
};

struct IntList
{
    int count;
    IntListElem* first;
};

struct Move
{
    int disk;
    int startpeg;
    int destinationpeg;
};

struct ConfigElem
{
    ConfigElem* nextpeg;
    IntList* disks;
};

class Config
{
public:
    //initializes an empty configuration
    Config();
    //initializes a configuration with all disks on the first peg
    Config(int pegnumber, int disknumber);
    //Destructor
    ~Config();
    //returns the number of pegs
    int pegnumber();
    //returns the number of disks
    int disknumber();
    //returns the peg a disk is positioned on
    int diskposition(int disk);
    //returns an Intlist* with the disks on peg
    IntList* get_disks(int peg);
    //inserts the disk in the list of peg
    void insert_disk(int disk, int peg);
    //remove the disk from the list of the peg
    void remove_disk(int disk, int peg);
    //changes the configuration by performing Move
    void move_config(Move move);
    //print the configuration
    void print();
private:
    int _pegs;
    int _disks;
    ConfigElem* _firstpeg;
};
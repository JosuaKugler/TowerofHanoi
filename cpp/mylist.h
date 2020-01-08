struct MyListElem
{
    MyListElem* next;
    int value;
};

class MyList
{
public:
    //initizializes an empty list
    MyList();
    //initializes a list with ascending ints from 0 to count
    MyList(int count);
    //deep Copy Constructor
    MyList(MyList& list);
    //Destruktor
    ~MyList();
    //length
    int len();
    //get the first index of val (if val not in list, return -1)
    int get_index(int val);
    //get val at position index
    int get_val(int index);
    //get the minimum value
    int min_val();
    //get the maximum value
    int max_val();
    //append value in a way that the value before val is 
    //leq and the value after val is geq
    void append_ordered(int val);
    //insert val at index
    void insert_at_index(int val, int index);
    //insert val at the end
    void append(int val);
    //remove at the given index
    void remove_at_index(int index);
    //remove the first occurence of val
    void remove_val (int val);
    //print list
    std::string to_string();
    //equality
    bool is_equal(MyList& list);
    private:
    int _count;
    MyListElem* _firstElem;
};
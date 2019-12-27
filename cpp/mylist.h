struct MyListElem
{
    MyListElem* next;
    int value;
};

class Mylist
{
public:
    //initizializes an empty list
    Mylist();
    //initializes a list with first as first element
    Mylist(MyListElem* first);
    //Destruktor
    ~Mylist();
    //get the first index of val
    int get_index(int val);
    //get val at position index
    int get_val(int index);
    //get the minimum value
    int min_val();
    //get the maximum value
    int max_val();
    //append value in a way that the value before val is 
    //smaller and the value after val is bigger
    void append_ordered(int val);
    //insert val at index
    void insert_at_index(int val, int index);
    //insert val at the end
    void insert_val(int val);
    //remove at the given index
    void remove_at_index(int index);
    //remove the first occurence of val
    void remove_val (int disk);
    private:
    int _count;
    MyListElem* _firstElem;
};
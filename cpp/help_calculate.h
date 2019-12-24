#include <cmath>
typedef unsigned long long my_int;

my_int faculty(my_int n)
{
    if (n == 0)
    {
        return 1;
    }
    else
    {
        return n * faculty(n-1);
    }   
}

my_int bk(my_int n, my_int k)
{
    if (n == k)
    {
        return 1;
    }
    else if ( k < 0 or k > n)
    {
        return 0;
    }
    return faculty(n)/(faculty(n-k) * faculty(k));
}

my_int t_(my_int n, my_int k)
{
    my_int t = -1;
    my_int x = 0;
    while ( n > x )
    {
        ++t;
        x = bk(k - 2 + t, k -2);
    }
    return t;
}

my_int formula(my_int n, my_int k, my_int t)
{
    if (k == 3)
    {
        //types?
        return pow(2, n) - 1;
    }
    my_int x = 0;
    for (my_int i = 0; i <= t+1; ++i)
    {
        x = x + pow(2, i*bk(i+k-3, k-3));
    }
    my_int correction = pow(2, t*(n-bk(t+k-2, k-2)));
    return x - correction;
}

my_int M(my_int n, my_int k)
{
    my_int t = t_(n,k);
    my_int x = formula(n , k , t);
    return x;
}
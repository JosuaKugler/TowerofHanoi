#include <cmath>

int faculty(int n)
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

int bk(int n, int k)
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

int t_(int n, int k)
{
    int t = -1;
    int x = 0;
    while ( n > x )
    {
        ++t;
        x = bk(k - 2 + t, k -2);
    }
    return t;
}

int formula(int n, int k, int t)
{
    if (k == 3)
    {
        //types?
        return pow(2, n) - 1;
    }
    int x = 0;
    for (int i = 0; i <= t+1; ++i)
    {
        x = x + pow(2, i*bk(i+k-3, k-3));
    }
    int correction = pow(2, t*(n-bk(t+k-2, k-2)));
    return x - correction;
}

int M(int n, int k)
{
    int t = t_(n,k);
    int x = formula(n , k , t);
    return x;
}
def faculty(x):
    """
    returns 'x!'
    """
    if x == 0:
        return 1
    value = 1
    for i in range(1, x+1):
        value *= i
    return int(value)

def bk(n, k):
    """
    returns 'n over k'
    """
    if n == k:
        return 1
    if k < 0 or k > n:
        return 0
    value = faculty(n) / (faculty(k) * faculty(n - k))
    return int(value)

def t_(n, k):
    """
    returns the exponent of the increment of a configuration with n disks and k pegs
    """
    t = -1
    x = 0
    while n > x:
        t += 1
        x = bk(k-2+t, k-2)
    return t

def formula(n, k, t):
    """
    returns the minimum number of moves for increment 2^t, k pegs and n disks
    """
    if k == 3:
        return 2**(n)-1
    x = 0
    for i in range(0, t+1):
        x = x + 2**i*bk(i+k-3, k-3)
    correction = 2**t*(n-bk(t+k-2, k-2))
    return x + correction

def M(n, k):
    """
    returns the minimum number of moves for k pegs and n disks
    """
    t = t_(n, k)
    x = formula(n, k, t)
    return x

def b_(p,t,k):
    """
    helper function for adjustedUpsilon
    """
    if t == 0:
        return 0
    return bk(k-p+t-3,t-1)

def h_(p,t,k):
    """
    helper function for adjustedUpsilon
    """
    return bk(k-p+t-2,t-1)

def A_(n,t,k):
    """
    helper function for adjustedUpsilon
    """
    if t == 0:
        return 0
    return n - bk(t-1+k-2,t-1)

def lowerbound(A,t,k):
    """
    helper function for adjustedUpsilon
    """
    summe = 0
    for p in range(2,k-1):
        summe += b_(p,t,k)
    return int(max([0,A-summe]))

def upperbound(A,t,k):
    """
    helper function for adjustedUpsilon
    """
    return int(min([A,b_(1,t,k)]))

def upsilon(n,k):
    """
    our first conjecture for the number of possibilities, proven to be wrong
    """
    s = t_(n,k)
    above = bk(s+k-3,k-3)
    below = bk(s+k-2,k-2)-n
    result = bk(above,below)
    return result

def adjustedUpsilon(n, k):
    """
    computes the number of possibilities according to the Frame-Stewart algorithm
    """
    if n==0 or k==3 or n<k:
        return 1
    t = t_(n,k)
    A = A_(n,t,k)
    lower = lowerbound(A,t,k)
    upper = upperbound(A,t,k)
    summe = 0
    for a in range(lower, upper + 1):
        value1 = adjustedUpsilon(n - h_(1, t-1, k) - a, k - 1)
        value2 = adjustedUpsilon(h_(1, t - 1, k) + a, k)
        summe += value1*value2
    return summe

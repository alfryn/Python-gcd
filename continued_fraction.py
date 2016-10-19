import random

# gcd
# I princip samma algoritm som kedjebråket.
def gcd(a, b):
    if a == b: return a
    while b > 0: a, b = b, a % b
    return a

# Pure continued fractions (only ones as dividends)
# Any rationional number can be written in this form.
# Ren form av kedjebråk med enbart ettor i täljaren.
# Varje rationellt bråk kan skrivas i denna form.
# Ett avkortat bråk är den bästa rationella approximationen. Återför med invcf.
    
# 1+ 3/67 = 70/67 : cf(70,67) -> [1,22,3]
def cf(a,b):
	res=[]	
	while b!=0:
         res.append(a//b)
         a, b = b, (a % b)
	return res
 
# cf(8,35)
# Out[12]: [0, 4, 2, 1, 2]

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

# Rekursiv returnerar även ax+by=gcd(a,b) behövs för att räkna ut invers vs modulo
def egcd(a, b):    
    if a == 0:
        return (b, 0, 1, 1)
    else:
        g, y, x, c = egcd(b % a, a)
        return (g, x - (b // a) * y, y, c+1)
        
def modinv(a, m):
    g, x, y, c = egcd(a, m)
    if g != 1:
        raise Exception('Invers till modulo saknas')
    else:
        return x % m        
 
# Numerisk approximation av en enkel cf. Ifall vi inte vill använda invcf av någon anledning.
# Anledningen kan vara att vår cf inte är på standardform [1, 3.55335, 2.934493, 1.13293] se testfall nedan.
def calcCF(c):
    b=c[-1]
    c=c[:-1]    
    while len(c)>0:
        a=1.0/b
        b=c[-1]
        c=c[:-1]
        b=b+a        
    return b

# Returns a mixed fraction from a cf list.
# invcf([1,22,3]) -> (1, 3, 67) = 1 + 3/67
def invcf(c):    
    b=c[-1]
    c=c[:-1]
    d=1
    while len(c)>1:
        a=b
        b=c[-1]
        c=c[:-1]
        b, d = a*b+d, a        
    return c[0], a,b

# Prova slumptal mellan 1 och 10

def RandDist(r,n):
    sysrand=random.SystemRandom()
    return [1+sysrand.randrange(r-1) for x in range(n)]

def RandDistTest(r,n,m):
    return [calcCF(RandDist(r,n)) for x in range(m)]
            
def AvList(l):
    return sum(l)/float(len(l))

def RandRoot(r,n):
    sysrand=random.SystemRandom()
    return [(1+sysrand.randrange(r-1))**0.5 for x in range(n)]

def RandRootTest(r,n,m):
    return [calcCF(RandRoot(r,n)) for x in range(m)]
    
# l=RandDistTest(10, 100, 100000)
# AvList(l)
# Out[36]: 5.281807091646388
# Out[38]: 5.272341361416181
# Out[40]: 5.27319339110916
# Out[42]: 5.277478294386115
# l=RandDistTest(10, 100, 1000000)
# Out[44]: 5.279200133660059
# Out[46]: 5.28093868455096
# Out[48]: 5.276942155886018
# 5.279 +- 0.0025
#
# l=RandRootTest(100, 100, 100000)
# AvList(l)
# 6.858137842152367
# 6.855671075638552
# 6.872599389709003
# 6.86868425712954
# l=RandRootTest(100, 100, 1000000)
# 6.8593819012644515

# Vad händer om vi kastar om siffror en sk. orbit
# [0,1,3,4]
# (0, 13, 17), (0, 13, 16), (0, 5, 19), (0, 5, 16), (0, 4, 19), (0, 4, 17)
# Tre nämnare och tre täljare.

# cf(a,b) har en maximal periodlängd proportionell mot b.
# Exempel med invcf
# invcf([0,1,1,1,1,2])
# (0, 8, 13)
# invcf([0,1,1,1,1,2])
# (0, 13, 21)
# Som följer av algoritmen byter 13 plats och följden har större a,b.
# invcf([0,1,1,1,1,3])
# (0, 11, 18)
# invcf([0,1,1,1,1,5])
# (0, 17, 28)
# Och ökande sista siffra har större a,b

# TODO General continued fractions. Useful as convergence for series with known square root forms.

# Returns list of "decimals" for 1/a in base b
def invbase(a,b,cnt):
    res=[]
    r=1
    for i in range(1,cnt):                
        q=r*b//a
        r=(r*b)%a
        res.append(q)
    return res
    
def binstr(a):
    return bin(a)[2:]

# p2 = list(bingen(2048))
def bingen(x):
   i = 1
   for n in range(x + 1):
       yield i
       i <<= 1
      
# Returns a list of remainders base 2        
def hildegard(n):
    bstr=binstr(n)
    l=len(bstr)
    p2=list(bingen(l))
    if len(p2)>l:
        p2=p2[:-1]
    # Filter out the powers of two needed.
    p2.reverse()
    p2used=[p2[i] for i in range(0,l) if bstr[i]=='1']
    res=[]
    nn=n    
    for p in p2used:        
        print(nn,p)
        nn=nn%p
        res.append(nn)
    res=res[:-1]
    return bstr, res
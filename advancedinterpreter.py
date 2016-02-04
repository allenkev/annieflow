import sys
import re

def c_div(a,b):
    x=a//b
    if x*b < a:
        return x+1
    else:
        return x

def f_div(a,b):
    return a//b

def log(a, r=f_div, b=2):
    if a<1 or b<2:
        raise Exception("can't take that log")
    i=0
    while a>1:
        a=r(a,b)
        i+=1
    return i

#same as int(), but returns 0 on empty string instead of erroring
def binInt(i,base=2):
    return 0 if i=="" else int(i,base)

def getFrom(k, s):
    y=log(k)
    x=2**(y+1)
    (a,s)=(s[:y], s[y:])
    if len(a)<y:
        a+="1"*(y-len(a))
    if binInt(a,2) < x-k:
        return (binInt(a,2),s)
    if len(s)==0:
        s="1"
    return (int(a+s[0], 2)-x+k, s[1:])

def getFromNoFill(k, s):
    y=log(k)
    x=2**(y+1)
    (a,s)=(s[:y], s[y:])
    if len(a)<y:
        raise Exception("no ending bits")
    if binInt(a,2) < x-k:
        return (binInt(a,2),s)
    if len(s)==0:
        raise Exception("no ending bits")
    return (int(a+s[0], 2)-x+k, s[1:])

def getInf(s, k=2):
    if k<2:
        raise Exception("need coarseness of at least 2")
    s="1"+s
    if "1"*k not in s:
        s+="1"*k
    num,count = 0,0
    while count<k:
        if s[0]=="0":
            num,count=num*k+count,0
        else:
            count+=1
        s=s[1:]
    return (num,s)

def getUnary(s):
    if "1" not in s:
        return (len(s),"")
    num=0
    while s[0]=="0":
        num,s=num+1,s[1:]
    s=s[1:]
    return (num,s)

def getUniqueList(s):
    a=[]
    while len(s)>0 and s[0] not in a:
        a.append(s[0])
        s=s[1:]
    s=s[1:]
    return (a, s)

myChars=" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~\n"

def compress(s, chars=myChars):
    fin = ""
    k=len(chars)
    y=log(k,c_div)
    x=2**y
    try:
        while 1:
            (a,s)=getFromNoFill(k,s)
            fin+=chars[a]
    except:
        q=2**len(s)-1+binInt(s)
        if len(s)==y-1 and binInt(s) >= x-k:
            q+=-x+k
        fin+=chars[q]
    return fin

def getDecompression(chars=myChars):
    k=len(chars)
    y=log(k,c_div)
    x = 2**y
    d={}
    i = 0
    while i < x-k:
        d[chars[i]]=format(i, "0"+str(y-1)+"b")
        i+=1
    n=2*i
    while n < x:
        d[chars[i]]=format(n, "0"+str(y)+"b")
        n+=1
        i+=1
    return d

def getLastDecompression(chars=myChars):
    k=len(chars)
    y=log(k,c_div)
    x = 2**y
    d={}
    i=1
    d[chars[0]]=""
    while i<2**(y-1)-1:
        length=log(i+1)
        val=i+1-2**(length)
        d[chars[i]]=format(val, "0"+str(length)+"b")
        i+=1
    i-+1
    while i < k-1:
        length=log(i+1)
        val=i+1-2**(length)+x-k
        d[chars[i]]=format(val, "0"+str(length)+"b")
        i+=1
    return d

def getDecompressions(chars=myChars):
    return (getDecompression(chars), getLastDecompression(chars))

def decompress(s, d=getDecompressions(), last=myChars[-1]):
    (a,b)=d
    c=s[-1]
    s=s[:-1]
    if c==last:
        return decompress(s,d,last)
    fin = ""
    for i in s:
        fin+=a[i]
    fin+=b[c]
    return fin

class AnyFlow:
    def __init__(self, C, chars, allowInput=True, listcase=lambda x: []):
        self.C=C
        self.chars=chars
        self.allowInput=allowInput
        self.listcase=listcase

    def run_me(self, a=None):
        if a==None:
            a=self.listcase(len(self.C)-1)
        A=[]
        for i in range(len(self.C)-1):
            A.append(self.listcase(i))
        A.append(a)
        if self.allowInput:
            s=raw_input()
            for i in s:
                if i not in self.chars:
                    raise Exception("invalid input character")
                self.push_me(A,len(self.C), self.chars.index(i))
        x=self.pop_me(A, len(self.C))
        while x!=None:
            x=self.pop_me(A, x)
        r=A[-1]

    def pop_me(self, A, i):
        if i==0:
            return
        i-=1
        if len(A[i])>0:
            (c,d)=self.C[i][0][A[i].pop()]
        else:
            (c,d)=self.C[i][1]
        for j,k in c:
            self.push_me(A,j,k)
        return d
            
    def push_me(self,A,i,j):
        if i == 0:
            sys.stdout.write(self.chars[j]),
        else:
            A[i-1].append(j)

def parse_me(s,comp = False,chars=None):
    if chars==None:
        (chars, s) = getUniqueList(s)
    if comp:
        s=decompress(s)
    if len(s)>0 and s[-1]=="1":
        s+="0"
    (allowInput,s)=getFrom(2,s)
    (a, s)=getInf(s)
    a+=1
    if a==1:
        chars=myChars
    A=range(a)
    B=[len(chars)]
    #get symbol counts for all except output and input
    for i in A[1:-1]:
        (c,s)=getInf(s)
        c+=1
        B.append(c)
    if a > 1:
        if allowInput:
            c=len(chars)
        else:
            (c,s)=getInf(s)
        B.append(c)
    #get rules for all stacks except 0th (output)
    C=[]
    for i in A[1:]:
        #get rules for this stack
        D=[]
        for j in range(B[i]+1):
            #get pushes from the symbol
            (b,s)=getInf(s)
            E=[]
            for k in range(b):
                (c,s)=getFrom(a,s)
                (d,s)=getFrom(B[c],s)
                E.append((c,d))
            #get next popped stack
            (f,s)=getFrom(a, s)
            D.append((E,f))
        e=D.pop()
        C.append((D,e))
    return AnyFlow(C,chars,allowInput)

if len(sys.argv) > 2:
    if sys.argv[1] == "run":
        with open(sys.argv[2]) as f:
            parse_me(f.read(), True).run_me()
    elif sys.argv[1] == "compress":
        with open(sys.argv[3],"w") as f:
            f.write(compress(sys.argv[2]))
    elif sys.argv[1] == "decompress":
        with open(sys.argv[2]) as f:
            print decompress(f.read())

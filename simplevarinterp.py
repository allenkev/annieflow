def parse(s):
    chars="^<>?!"
    doublis=[(False,[])]
    while len(s)>0:
        curr = ""
        while s[0] not in chars:
            curr+=s[0]
            s=s[1:]
        if s[0]==chars[0]:
            a="."+curr,
            doublis[-1][1].append(a)
        elif s[0]==chars[1]:
            doublis.append((curr,[]))
        elif s[0]==chars[2]:
            doublis[-2][1].append(doublis.pop())
        elif s[0]==chars[3]:
            a="?"+curr,
            doublis[-1][1].append(a)
        elif s[0]==chars[4]:
            a="!"+curr,
            doublis[-1][1].append(a)
        s=s[1:]
    if len(doublis) != 1:
        raise Exception()
    return doublis[0][1]

def run(p,**vals):
    doublis=[(0,p)]
    while len(doublis)>0:
        (i,d)=doublis.pop()
        if i<len(d):
            x=d[i]
            if len(x)==1:
                if x[0][0]==".":
                    if x[0][1:] not in vals:
                        vals[x[0][1:]]=1
                    else:
                        vals[x[0][1:]]+=1
                elif x[0][0]=="?":
                    if x[0][1:] not in vals:
                        vals[x[0][1:]]=abs(int(raw_input()))
                    else:
                        vals[x[0][1:]]+=abs(int(raw_input()))
                elif x[0][0]=="!":
                    if x[0][1:] not in vals:
                        print 0
                    else:
                        print vals[x[0][1:]]
                doublis.append((i+1,d))
            else:
                if x[0] in vals and vals[x[0]]:
                    vals[x[0]]-=1
                    doublis.append((i,d))    
                    doublis.append((0,x[1]))
                else:
                    doublis.append((i+1,d))

def par(s):
    run(parse(s))

from readData import readFile
#from method import MultiRound

def LDAGRank():
    S = []
    with open('LDAG_.txt', 'rt') as f:
        for line in f:
            S.append(line.split('\n')[0])
    return S

def ActivatedProbability():
    global data
    try:
        with open("network_ActivatedProbability.csv","rt") as f:
        for line in f:
            t = line.split(",")
            P[t[0]] = float(t[1].split("\n")[0])
            return P
    except IOError: 
        output = open("network_ActivatedProbability_.csv","w")
        P = dict.fromkeys(list(data.threshold.keys()),20/len(data.threshold))
        turn = 1
        SumOfP = sum(P.values())
        while turn < 3:
            tmp_P = dict(P)
            for node in data.threshold.keys():
                if node in data.IndegreeDic.keys():
                    tmp = 0.0
                    for n in data.IndegreeDic[node]:
                        tmp += P[n[0]]*n[1]
                    T = tmp
                    T -= data.threshold[node]
                    if T<0: T=0.0
                    tmp_P[node] = T
            P = dict(tmp_P)
            if sum(P.values()) == SumOfP:
                turn += 1
            else:
                SumOfP = sum(P.values())
                turn = 1
        Rank = sorted(list(P.items()),key=lambda x:x[1], reverse=True)
        for x in data.threshold.keys():
            output.write("{0},{1}\n".format(x,1-data.threshold[x]))
            P[x] = 1-data.threshold[x]
        output.close()
        P = dict.fromkeys(list(data.threshold.keys()))
        return P

def PageRank(d):
    try:
        score = dict.fromkeys(list(d.threshold.keys()))
        with open("pagerank.csv","rt") as f:
            for line in f:
                t = line.split(",")
                score[t[0]] = float(t[1].split("\n")[0])
    except IOError:
        output = open('pagerank.csv','w')
        global active_p
        N = len(d.threshold)
        turn = 1
        score = {}
        tmp_score = {}
        for x in range(1, N+1):
            score[str(x)] = 1.0
            tmp_score[str(x)] = 1.0
        SumOfScore = sum(score.values())
        count = 0
        while turn < 3 and count<100:
            count += 1
            for node in d.threshold.keys():
                tmp = 0
                if node not in d.OutdegreeDic.keys(): continue
                for outd in d.OutdegreeDic[node]:
                    inweight = 0.0
                    for ind in d.IndegreeDic[outd[0]]:
                        inweight += ind[1]
                    tmp += score[outd[0]]*outd[1]*active_p[outd[0]] / inweight
                tmp_score[node] = tmp
            score = dict(tmp_score)
            if sum(score.values()) == SumOfScore:
                turn += 1
            else:
                SumOfScore = sum(score.values())
                turn = 1
        for x in d.threshold.keys():
            output.write("{0},{1}\n".format(x,score[x]))
        output.close()
    
    return sorted(score, key=lambda x: score[x], reverse=True)

def merge(a1, b1):
    c = []
    while len(a1) != 0 and len(b1) != 0:
        if a1[0][1][0] > b1[0][1][0]:
            c.append(a1[0])
            a1.remove(a1[0])
        elif a1[0][1][0] == b1[0][1][0]:
            if a1[0][1][1] > b1[0][1][1]:
                c.append(a1[0])
                a1.remove(a1[0])
            elif a1[0][1][1] == b1[0][1][1]:
                if a1[0][1][2] > b1[0][1][2]:
                    c.append(a1[0])
                    a1.remove(a1[0])
                elif a1[0][1][2] == b1[0][1][2]:
                    if a1[0][1][3] > b1[0][1][3]:
                        c.append(a1[0])
                        a1.remove(a1[0])
                    else:
                        c.append(b1[0])
                        b1.remove(b1[0])
                else:
                    c.append(b1[0])
                    b1.remove(b1[0])
            else:
                c.append(b1[0])
                b1.remove(b1[0])
        else:
            c.append(b1[0])
            b1.remove(b1[0])
    if len(a1) == 0:
        c += b1
    else:
        c += a1
    return c

def mergesort(m):
    if len(m) == 0 or len(m) == 1:
        return m
    else:
        middle = len(m)//2
        a = mergesort(m[:middle])
        b = mergesort(m[middle:])
        return merge(a, b)

def findMajorityBigWeight(d):
    threshold = list(d.threshold.values())
    averageThreshold = sum(threshold) / len(threshold)
    N = len(threshold)
    majority = []
    for n in d.threshold.keys():
        count1 = 0
        count2 = 0
        count3 = 0
        if n not in d.OutdegreeDic.keys():
            majority.append([n, [0, 0, 0, 0.0]])
            continue
        for x in d.OutdegreeDic[n]:
            if x[1] >= averageThreshold: count1 += 1
            if x[1] >= averageThreshold / 2: count2 += 1
            if x[1] >= averageThreshold / 4: count3 += 1
        if n in d.OutdegreeDic.keys():
            majority.append([n, [count1, count2, count3, d.OutweightDic[n]]])
    rank = [x[0] for x in mergesort(majority)]
    return rank

data = readFile()
active_p = ActivatedProbability()
weight_rank = sorted(data.OutweightDic, key=lambda x: data.OutweightDic[x], reverse=True)
page_rank = PageRank(data)
majority_rank = findMajorityBigWeight(data)
LDAG_rank = LDAGRank()
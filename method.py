from random import choice
from LT_diffusion import Spreading
import setting

def resultofallmethods():
    Result = []
    METHODS = [MaxWeight, MajorityWeight, MaxPageRank, MaxLDAG]
    for M in METHODS:
        Active, Active1, Active2 = [], [], []
        Inactive = [x for x in setting.data.threshold.keys()]
        seed = []
        for i in range(10):
            X = M(list(Active),list(Active_1),list(Active_2),list(Inactive))
            Active.append(X)
            Active_1.append(X)
            Inactive.remove(X)
            (Active, Active_1, Active_2, Inactive) = Spreading(Active, Active_1, Active_2, Inactive)
        Result.append(len(Active_1))
    return Result

def MaxLDAG(active, my_active, your_active, inactive):
    for r in setting.LDAG_rank:
        if r in inactive:
            return r

def MajorityWeight(active, my_active, your_active, inactive):
    for r in setting.majority_rank:
        if r in inactive:
            return r

def MaxWeight(active, my_active, your_active, inactive):
    for r in setting.weight_rank:
        if r in inactive:
            return r

def MaxPageRank(active, my_active, your_active, inactive):
    for r in setting.page_rank:
        if r in inactive:
            return r

def FindCandidate(active, my_active, your_active, inactive):
    candidate = []
    for node in your_active:
        if node not in setting.data.OutdegreeDic.keys(): continue
        for outd in setting.data.OutdegreeDic[node]:
            if outd[0] not in inactive or outd[0] not in setting.data.IndegreeDic.keys(): continue
            for ind_L1 in setting.data.IndegreeDic[outd[0]]:
                if ind_L1[0] not in inactive or ind_L1[0] not in setting.data.IndegreeDic.keys(): continue
                for ind_L2 in setting.data.IndegreeDic[ind_L1[0]]:
                    if ind_L2[0] not in inactive: continue
                    candidate.append(ind_L2[0])
    return candidate

def CMaxSubGreedy(active, my_active, your_active, inactive):
    if not active or not your_active: return None
    rank = SubGreedy(active, my_active, your_active, inactive)
    candidate = FindCandidate(active, my_active, your_active, inactive)
    if not candidate: return None
    for r in rank:
        if r in candidate:
            return r
    return None

def CMajorityWeight(active, my_active, your_active, inactive):
    if not active or not your_active: return None
    candidate = FindCandidate(active, my_active, your_active, inactive)
    if not candidate: return None
    for r in setting.majority_rank:
        if r in candidate:
            return r
    return None

def CMaxWeight(active, my_active, your_active, inactive):
    if not active or not your_active: return None
    candidate = FindCandidate(active, my_active, your_active, inactive)
    if not candidate: return None
    for r in setting.weight_rank:
        if r in candidate:
            return r
    return None

def CMaxPageRank(active, my_active, your_active, inactive):
    if not active or not your_active: return None
    candidate = FindCandidate(active, my_active, your_active, inactive)
    if not candidate: return None
    for r in setting.page_rank:
        if r in candidate:
            return r
    return None

def BMaxSubGreedy(active, my_active, your_active, inactive):
    rank = SubGreedy(active, my_active, your_active, inactive)
    candidate = []
    for n in your_active:
        if n in setting.data.OutdegreeDic.keys():
            for n1 in setting.data.OutdegreeDic[n]:
                candidate.append(n1[0])
    if not candidate: return None
    for r in rank:
        if r in candidate and r in inactive:
            return r
    return None

def BMajorityWeight(active, my_active, your_active, inactive):
    candidate = []
    for n in your_active:
        if n in setting.data.OutdegreeDic.keys():
            for n1 in setting.data.OutdegreeDic[n]:
                candidate.append(n1[0])
    if not candidate: return None
    for r in setting.majority_rank:
        if r in candidate and r in inactive:
            return r
    return None

def BMaxWeight(active, my_active, your_active, inactive):
    candidate = []
    for n in your_active:
        if n in setting.data.OutdegreeDic.keys():
            for n1 in setting.data.OutdegreeDic[n]:
                candidate.append(n1[0])
    if not candidate: return None
    for r in setting.weight_rank:
        if r in candidate and r in inactive:
            return r
    return None

def BMaxPageRank(active, my_active, your_active, inactive):
    candidate = []
    for n in your_active:
        if n in setting.data.OutdegreeDic.keys():
            for n1 in setting.data.OutdegreeDic[n]:
                candidate.append(n1[0])
    if not candidate: return None
    for r in setting.page_rank:
        if r in candidate and r in inactive:
            return r
    return None

def Method(player, active, active_1, active_2, inactive):
    ACTIONS = [MaxWeight, CMaxWeight, BMaxWeight, MaxPageRank, CMaxPageRank, BMaxPageRank, MajorityWeight, CMajorityWeight, BMajorityWeight]
    candidate = []
    DIC = {}
    if player == '1':
        for a in ACTIONS:
            temp = (a,a(list(active), list(active_1), list(active_2), list(inactive)))
            if temp[1]:
                DIC[a] = temp[1]
    else:
        for a in ACTIONS:
            temp = (a,a(list(active), list(active_2), list(active_1), list(inactive)))
            if temp[1]:
                DIC[a] = temp[1]
    for k,v in DIC.items():
        if k.__name__[0]!='M':
            if v==DIC[MaxWeight]: continue
            if v==DIC[MajorityWeight]: continue
            if v==DIC[MaxPageRank]: continue
        candidate.append((k,v))
    return candidate
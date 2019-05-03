from method import MaxWeight
from method import MajorityWeight
from method import MaxPageRank
from method import BMaxWeight
from method import BMajorityWeight
from method import BMaxPageRank
from method import CMaxWeight
from method import CMajorityWeight
from method import CMaxPageRank
from method import MaxLDAG
import setting
from LT_diffusion import Spreading

def AIVSSTUPID(p1,p2,fileName):
    AI = []
    count = 0
    if fileName:
        with open(fileName,'rt') as f:
            for line in f:
                AI.append(line.split(',')[2].split('\n')[0])
                count+=1
                if count==20: break
        f.close()
    DIC = {'MaxWeight': MaxWeight, 'MajorityWeight': MajorityWeight, 'MaxPageRank': MaxPageRank, 'BMaxWeight': BMaxWeight, 'BMajorityWeight': BMajorityWeight, 'BMaxPageRank': BMaxPageRank, 'CMaxWeight': CMaxWeight, 'CMajorityWeight': CMajorityWeight, 'CMaxPageRank': CMaxPageRank, 'MaxLDAG': MaxLDAG}
    N = 0
    Method = []
    if p1=="AI":
        for x in range(20):
            if x%2==0: Method.append(AI[x])
            else: Method.append(p2)
    elif p2=="AI":
        for x in range(20):
            if x%2==1: Method.append(AI[x])
            else: Method.append(p1)
    else:
        for x in range(20):
            if x%2==0: Method.append(p1)
                else: Method.append(p2)
    Active, Active_1, Active_2 = [], [], []
    Inactive = [x for x in setting.data.threshold.keys()]
    seed = '1'
    for x in range(20):
        if x%2==0:
            seed = DIC[Method[x]](list(Active),list(Active_1),list(Active_2),list(Inactive))
            if not seed: 
                seed = MaxWeight(list(Active),list(Active_1),list(Active_2),list(Inactive))
            Active.append(seed)
            Active_1.append(seed)
            Inactive.remove(seed)
        else:
            seed = DIC[Method[x]](list(Active),list(Active_2),list(Active_1),list(Inactive))
            if not seed:
                seed = MaxWeight(list(Active),list(Active_2),list(Active_1),list(Inactive))
            Active.append(seed)
            Active_2.append(seed)
            Inactive.remove(seed)
        (Active, Active_1, Active_2, Inactive) = Spreading(list(Active),list(Active_1),list(Active_2),list(Inactive))
    return (len(Active_1),len(Active_2))

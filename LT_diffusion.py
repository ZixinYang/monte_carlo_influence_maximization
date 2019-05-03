import random
import setting

def Spreading(active, my_active, your_active, inactive):
    tmp_active = list(active)
    tmp_inactive = list(inactive)
    tmp_my_active = list(my_active)
    tmp_your_active = list(your_active)
    this_layer = list(active)
    next_layer = []
    for node in this_layer:
        if node in setting.data.OutdegreeDic.keys():
            for n in setting.data.OutdegreeDic[node]:
                if n[0] not in this_layer and n[0] not in next_layer: next_layer.append(n[0])
    while next_layer:
        this_layer = list(next_layer)
        tmp_this = list(next_layer)
        for node in this_layer:
            total = 0
            mine = 0
            yours = 0
            for n in setting.data.IndegreeDic[node]:
                if n[0] in tmp_active:
                    total += n[1]
                    if n[0] in tmp_my_active:
                        mine += n[1]
                    elif n[0] in tmp_your_active:
                        yours += n[1]
            if total >= setting.data.threshold[node]:
                if node not in tmp_active:
                    tmp_active.append(node)
                    tmp_inactive.remove(node)
                    if mine > yours:
                        tmp_my_active.append(node)
                    elif mine < yours:
                        tmp_your_active.append(node)
                    else:
                        random.choice([tmp_my_active, tmp_your_active]).append(node)
            else:
                tmp_this.remove(node)
        this_layer = list(tmp_this)
        next_layer = []
        for node in this_layer:
            if node in setting.data.OutdegreeDic.keys():
                for n in setting.data.OutdegreeDic[node]:
                    if n[0] in tmp_inactive and n[0] not in this_layer and n[0] not in next_layer:
                        next_layer.append(n[0])
    return [tmp_active, tmp_my_active, tmp_your_active, tmp_inactive]

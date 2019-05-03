from DATA import Data
import csv
import os.path

def readFile():
    data = Data({},{},{},{},{})
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "datasets/")
    path1 = os.path.join(path,"t1_1.csv")
    with open(path1, 'rt') as f:
        for line in f:
            tmp = line.split('\t')
            tmp[1] = float(tmp[1].split('\n')[0])
            data.threshold[tmp[0]] = tmp[1]
    f.close()
    path2 = os.path.join(path,"network_t1_1.csv")
    with open(path2, 'rt') as f:
        for line in f:
            tmp = line.split('\t')
            tmp[2] = float(tmp[2].split('\n')[0])
            if tmp[0] not in data.OutdegreeDic.keys():
                data.OutdegreeDic[tmp[0]] = [[tmp[1], tmp[2]]]
                data.OutweightDic[tmp[0]] = tmp[2]
            elif tmp[0] in data.OutdegreeDic.keys():
                data.OutdegreeDic[tmp[0]].append([tmp[1], tmp[2]])
                data.OutweightDic[tmp[0]] += tmp[2]
            if tmp[1] not in data.IndegreeDic.keys():
                data.IndegreeDic[tmp[1]] = [[tmp[0], tmp[2]]]
                data.InweightDic[tmp[1]] = tmp[2]
            elif tmp[1] in data.IndegreeDic.keys():
                data.IndegreeDic[tmp[1]].append([tmp[0], tmp[2]])
                data.InweightDic[tmp[1]] += tmp[2]
    f.close()
    print("Finish reading data")
    return data

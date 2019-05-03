import time
import setting
import argparse
from MCTS import CCIM
from MCTS import UCT
from MCTS import Node
from LT_diffusion import Spreading
from method import resultofallmethods
from AI_VS_STUPID import AIVSSTUPID

def breadth_first_search(R,T,buf,M):
    global args
    K = args.seed_size
    TURNS = K+1
    SEED = []
    fileName = "Path.csv"
    output = open(fileName, "w")
    cnt = R
    SEED = []
    for x in range(7):
        SEED.append(buf[x][1])
        output.write("{0},{1},{2}\n".format(x+1, buf[x][1], buf[x][0]))
    Active = []
    Active_1 = []
    Active_2 = []
    TREND = []
    Inactive = list(setting.data.threshold.keys())
    for i in range(K):
        Active.append(SEED[i])
        Inactive.remove(SEED[i])
        if i%2==0:
            Active_1.append(SEED[i])
        else:
            Active_2.append(SEED[i])
        (Active, Active_1, Active_2, Inactive) = Spreading(Active, Active_1, Active_2, Inactive)
        if i%2==1:
            TREND.append(len(Active)/len(setting.data.threshold))
    output.write("{0}\n{1}\n{2}\n".format(len(Active),len(Active_1),len(Active_2)))
    output.write("MCT Construction time: {0}\n".format(T))
    for t in TREND:
        output.write("{0},".format("{:.2%}".format(t)))
    output.write("\n\n")
    output.close()
    METHODS = ['MaxWeight','MajorityWeight','MaxPageRank','MaxLDAG']
    INDEX = METHODS.index(M.__name__)
    output = open("Result.csv","w")
    for i in range(4):
        STR = 'AI'
        output.write(M.__name__+' VS '+METHODS[i]+'\n')
        outcome = AIVSSTUPID(M.__name__, METHODS[i], None)
        output.write('p1:{0},p2:{1}\n'.format(outcome[0],outcome[1]))
        
        output.write(METHODS[i]+' VS '+M.__name__+'\n')
        outcome = AIVSSTUPID(METHODS[i], M.__name__, None)
        output.write('p1:{0},p2:{1}\n'.format(outcome[0],outcome[1]))
        
        output.write('AI VS '+METHODS[i]+'\n')
        outcome1 = AIVSSTUPID(STR,METHODS[i],fileName)
        output.write('p1:{0},p2:{1}\n\n'.format(outcome1[0],outcome1[1]))
        
        output.write(METHODS[i]+' VS '+'AI'+'\n')
        outcome2 = AIVSSTUPID(METHODS[i],STR,fileName)
        output.write('p1:{0},p2:{1}\n\n'.format(outcome2[0],outcome2[1]))
    output.close()

def construct_tree():
    global args
    tstart = time.time()
    r,buf,M = UCT(args)
    tend = time.time()
    breadth_first_search(r,tend-tstart,buf,M)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--seed_size', default=20, type=int, help='seed size')
    args = parser.parse_args()
    TURNS = args.seed_size+1
    construct_tree()
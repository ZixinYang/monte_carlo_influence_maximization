from random import choice, sample, uniform
from math import sqrt, log
from method import Method
from LT_diffusion import Spreading
from method import MaxWeight
from method import MajorityWeight
from method import MaxPageRank
from method import MaxLDAG
from method import resultofallmethods
import setting

class CCIM():
    TURNS = 20
    PLAYERS = ('1', '2')
    NODES = [i for i in setting.data.threshold.keys()]
    def __init__(self, players=PLAYERS):
        self.players = players
    def actions(self, state, player):
        return list(set(Method(player, state[1], state[2], state[3], state[4])))
    def result(self, state, action, player):
        newState = []
        T = [state[0] + 1]
        A, A1, A2, IA = list(state[1]), list(state[2]), list(state[3]), list(state[4])
        A.append(action[1])
        IA.remove(action[1])
        if player == self.PLAYERS[0]:
            A1.append(action[1])
            newState = Spreading(A, A1, A2, IA)
        else:
            A2.append(action[1])
            newState = Spreading(A, A1, A2, IA)
        newState = T + newState
        return newState
    def terminal(self, turn):
        if turn == self.TURNS+1:
            return True
        return False
    def next_player(self, player):
        if player == self.PLAYERS[0]:
            return self.PLAYERS[1]
        else:
            return self.PLAYERS[0]
    def outcome(self, state, player):
        if player == self.PLAYERS[0]:
            return len(state[2])
        else:
            return len(state[3])

class Node():
    def __init__(self, parent, state=None, player=None, ccim=None, act=None, M=None):
        self.ccim = ccim or parent.ccim
        self.parent = parent
        self.state = state
        self.player = player
        self.X = X
        self.visits = 1
        self.value = 0
        if player=='2': self.children = dict.fromkeys([(M,M(list(state[1]),list(state[2]),list(state[3]),list(state[4])))])
        else: self.children = dict.fromkeys(self.ccim.actions(state, player))
        self.act = act
    def terminal(self):
        return self.ccim.terminal(self.state[0])
    def next_player(self):
        return self.ccim.PLAYERS[self.ccim.PLAYERS.index(self.player)^1]
    def weight(self):
        if self.visits == 0:
            return 0
        return self.value / float(self.visits)
    def search_weight(self):
        if not self.parent or not self.parent.parent: return self.weight()
        return self.weight()
        #return self.weight() + (1/sqrt(10)) * sqrt(log(self.parent.parent.visits) / self.visits)
    def fully_expanded(self):
        return not None in self.children.values()
    def expand(self,M):
        action = None
        for k in self.children.keys():
            if self.children[k] == None:
                action = k
                break
        state = self.ccim.result(self.state, action, self.player)
        player = self.next_player()
        child = Node(self, state, player, None, action, M)
        self.children[action] = child
        return child
    def best_child(self):
        return max(self.children.values(), key=lambda x: x.search_weight())
    def simulation(self, METHOD):
        Actions = METHOD
        reward = 0.0
        for A in Actions:
            tmp_turn = self.state[0]
            st = [self.state[0], list(self.state[1]), list(self.state[2]), list(self.state[3]), list(self.state[4])]
            p1 = self.player
            before,before1 = 0,0
            if p1=='2':
                before = len(self.parent.state[2])
                before1 = len(self.parent.state[3])
            else:
                before = len(self.parent.state[3])
                before1 = len(self.parent.state[2])
            steps = 10
            while not self.ccim.terminal(tmp_turn):
                if p1 == '1':
                    #print("player1 selects--------------------")
                    if self.player=='1': action = A(list(st[1]),list(st[2]),list(st[3]),list(st[4]))
                    else:
                        action = A(list(st[1]),list(st[2]),list(st[3]),list(st[4]))
                    st[1].append(action)
                    st[2].append(action)
                else:
                    #print("player2 selects-------------------")
                    if self.player=='2': action = A(list(st[1]),list(st[3]),list(st[2]),list(st[4]))
                    else:
                        action = A(list(st[1]),list(st[3]),list(st[2]),list(st[4]))
                    st[1].append(action)
                    st[3].append(action)
                tmp = Spreading(st[1], st[2], st[3], st[4])
                tmp_turn += 1
                st = [tmp_turn]
                st.extend(tmp)
                steps -= 1
                if steps==0: break
                p1 = self.ccim.next_player(p1)
            Outcome = 0
            now_round = 0
            Outcome = self.ccim.outcome(st,p1)
            Outcome1 = self.ccim.outcome(st,self.ccim.next_player(p1))
            now_round = tmp_turn - 1
            reward += ((Outcome-before))
        reward /= len(Actions)
        return reward

def UCT(args):
    STUPID = resultofallmethods()
    METHODS = {MaxWeight: STUPID[0], MajorityWeight: STUPID[1], MaxPageRank: STUPID[2]}
    METHODS_sort = sorted(METHODS.items(), key=lambda x: x[1], reverse=True)
    METHOD = []
    for x in range(2):
        METHOD.append(METHODS_sort[x][0])
    Game = CCIM()
    id_node = {}
    root = parent
    deepbranch = 3
    child = root
    buf = []
    while deepbranch > 0:
        child = root
        while child.state[0]<=args.seed_size:
            if not child.fully_expanded():
                child = child.expand(METHOD[0])
                print("Player {0} in turn {1} expand {2}".format(child.parent.player, child.state[0]-1, child.act))
                break
            else:
                child = child.best_child()
                buf.append((child.act[0].__name__,child.act[1]))
                print("Player {0} in turn {1}, this action is {2}".format(child.parent.player, child.state[0]-1, child.act))
                if child.state[0] == args.seed_size+1:
                    deepbranch -= 1
        delta = child.simulation([MaxWeight])
        count = 5
        while child:
            child.visits += 1
            child.value += delta
            if not child.parent: break
            child = child.parent.parent
            count-=1
            if count==0: break
    return (root,list(buf[(-1)*args.seed_size:]), METHOD[0])
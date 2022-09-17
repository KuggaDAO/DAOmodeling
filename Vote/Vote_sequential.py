import numpy as np

class Vote_condition:
# 描述当前投票能获取到的信息
    def __init__(self, n, work, configs):
        self.members = []
        self.votes = []
        self.complete = 0
        self.wait = n
        self.collect = 0
        self.work = work
        self.configs = configs

    def add_vote(self, member, vote):
    # 添加信息
        self.members.append(member)
        self.votes.append(vote)
        self.complete = self.complete + 1
        self.wait = self.wait - 1
        self.collect = self.collect + self.configs['vote']['quad']['token_const'] * vote ** 2

class Vote_Sequential:
    def __init__(self, members, work, configs):
        self.members = members
        self.work = work
        self.configs = configs
        self.condition = Vote_condition(len(members), self.work, self.configs)
        self.outcome = 0     # 0 means the vote haven't completed yet, while 1 means pass, -1 means denied

    def order(self):
        # calculate and decide the voting order of this set of members
        time = []
        for n in range(len(self.members)):                      # calculate voting time for specific member
            time.append(0.5 * np.random.randn() + self.members[n].activity)
        index = sorted(range(len(time)), key=lambda k: time[k])
        tmp = []
        for n in range(len(self.members)):                      # rearrange the order of members
            tmp.append(self.members[index[n]])
        for n in range(len(tmp)):
            self.members[n] = tmp[n]

    def result(self):
        # calculate result and distribute the collected tokens
        s = sum(self.condition.votes)
        if s > 0:
            self.outcome = 1
        else:
            self.outcome = -1
        token_sum = 0   # calculate the total token owned by members
        for n in range(len(self.members)):
            token_sum += self.members[n].token
        for n in range(len(self.members)):
            self.members[n].token += np.sum(self.members[n].preference * self.work.preference) * self.outcome
            self.members[n].token += self.condition.collect * self.members[n].token / token_sum

    def vote(self):
        # the main voting procedure
        self.order()
        for n in range(len(self.members)):
            nv = self.members[n].sequential_voting(self.condition)
            self.members[n].token = self.members[n].token - self.configs['vote']['quad']['token_const'] * nv ** 2
            self.condition.add_vote(self.members[n], nv)
        self.result()

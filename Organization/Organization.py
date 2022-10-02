import numpy as np
from Work import *
from Member import *

class Organization:
    def __init__(self, name='DAO', **configs):
        self.name = name
        self.works = []
        self.members = []
        self.record = {'all_works':[]}

    def add_work(self, new):
        if isinstance(new, Work):
            self.works.append(new)
        elif all(isinstance(m, Work) for m in new):
            self.works.extend(new)
        else:
            raise TypeError("item must be member(s)")

    def add_member(self, new):
        if isinstance(new, Member):
            self.members.append(new)
        elif all(isinstance(m, Member) for m in new):
            self.members.extend(new)
        else:
            raise TypeError("item must be member(s)")


    def show_works(self):
        for work_id in range(len(self.works)):
            print('id: {0} {1}'.format(work_id, self.works[work_id].preference))
    
    def show_members(self):
        for member_id in range(len(self.members)):
            print('id: {0} {1}'.format(member_id, self.members[member_id].preference))

    def vote_all(self, logic):
        l = len(self.works)
        for work_id in range(l-1, -1, -1):
            self.vote_once(work_id, logic)

    def vote_once(self, work_id, logic):
        work = self.works[work_id]
        for member in self.members:
            vote = member.decide(work, logic)
            self.reduce_member_token(member, vote)
            work.votes.append(vote)
        work.voted = True
        if sum(work.votes) > 0:
            work.ans = True
        else:
            work.ans = False
        self.update_token(work_id)
        self.del_work(work_id)

    def del_work(self, work_id):
        self.record['all_works'].append(self.works[work_id])
        self.works.pop(work_id)

    def reduce_member_token(self, member, amount):
        if member.token >= amount:
            member.token -= amount
            return True
        raise RuntimeError('insufficient tokens')

    def update_token(self, work_id):
        work = self.works[work_id]
        for member_id in range(len(self.members)):
            benefit = np.sum(self.members[member_id].preference * work.preference)
            if not work.ans:
                benefit *= -1.0
            self.members[member_id].token += benefit

    def collect_benefit(self):
        benefit = []
        for work in self.works:
            _benefit = []
            for member in self.members:
                _benefit.append(np.sum(member.preference * work.preference))
            benefit.append(_benefit)
        return np.array(benefit)

import numpy as np


class Vote_quadratic:
    def __init__(self, members, works, configs):
        self.members = members
        self.works = works
        self.configs = configs
        self.votes = []

    def voting(self):
        self.votes = []
        self.vote_ans = []
        for i in range(len(self.works)):
            _votes, _vote_ans = self.vote_once(i)

            self.votes.append(_votes)
            self.vote_ans.append(_vote_ans)

            self.token_operation(_votes, _vote_ans, i)

    def vote_once(self, work_id):
        votes = []
        for member in self.members:
            vote = member.quad_vote(self.works[work_id])
            votes.append(vote)
        votes = np.array(votes)
        vote_num = np.sum(votes)
        if vote_num > 0:
            vote_ans = True
        else:
            vote_ans = False
        return votes, vote_ans

    def token_operation(self, votes, vote_ans, work_id):
        left_token = []
        for i in range(len(votes)):
            self.members[i].token -= self.configs['vote']['quad']['token_const'] * \
                                     (votes[i] ** 2)
            benefit = np.sum(self.members[i].preference * self.works[work_id].preference)
            if not vote_ans:
                benefit *= -1.0
            self.members[i].token += benefit
            left_token.append(self.members[i].token)

        vote_token = np.sum(votes * votes)
        left_token = np.sum(left_token)

        for member in self.members:
            member.token += member.token / left_token * vote_token

    def collect_benefit(self):
        benefit = []
        for work in self.works:
            _benefit = []
            for member in self.members:
                _benefit.append(np.sum(member.preference * work.preference))
            benefit.append(_benefit)
        return np.array(benefit)

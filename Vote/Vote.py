import numpy as np


class Vote_quadratic:
    def __init__(self, members, works, configs):
        self.members = members
        self.works = works
        self.configs = configs
        self.votes = []

    def voting(self, version=1.1):
        """
        do the voting
        """
        self.votes = []
        self.vote_ans = []
        self.token_voting = []
        self.token_voting.append(self.collect_tokens())
        for i in range(len(self.works)):
            if i % 5 == 0:
                print("work:{}".format(i))
            if version == 1.1:
                _votes, _vote_ans = self.vote_once(i)
            elif version == 1.2:
                _votes, _vote_ans = self.vote_once_visible(i)

            self.votes.append(_votes)
            self.vote_ans.append(_vote_ans)

            self.token_operation(_votes, _vote_ans, i)
            self.token_voting.append(self.collect_tokens())

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

    def vote_once_visible(self, work_id):
        """
        return the vote details and the vote result.
        this vote is operated under the speculation that everyone
        can see the current voting trend.
        !这里的doctest没有测试作用
        >>> v.vote_once_visible(0)
        [-13.2, 10, 3.3], True
        """
        votes = []
        agree_votes, reject_votes = 0, 0#record the number of currentvoting trend
        for member in self.members:
            T = max(20, (agree_votes + reject_votes) * 2)#还没想好怎么搞，就先这样吧
            vote = member.votes_with_forecast(self.works[work_id], T, agree_votes, reject_votes)
            votes.append(vote)
            if vote > 0:
                agree_votes += vote
            else:
                reject_votes += -vote
        votes = np.array(votes)
        return votes, agree_votes > reject_votes


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

    def collect_tokens(self):
        tokens = []
        for member in self.members:
            tokens.append(member.token)
        return tokens

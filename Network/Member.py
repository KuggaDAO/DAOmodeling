import numpy as np


class Member:
    def __init__(self, label, configs, emotion=np.random.rand(), token=0.0):
        self.label = label
        self.token = token
        self.emotion = emotion
        self.preference = np.random.randn(
            configs['preference']['dim']
        )
        self.quad_token_const = configs['vote']['quad']['token_const']
        self.quad_vote_const = configs['vote']['quad']['vote_const']
        return

    def __str__(self):
        return self.label

    def equal_vote(self, work):
        # one person one vote
        benefit = np.sum(self.preference * work.preference)
        if benefit > 0:
            return True
        else:
            return False

    def quad_vote(self, work):
        # apply the quadratic voting method
        # model: expectation = benefit * (2 * self.c * nv - 1 ) - nv ** 2 ,
        # nv stands of number of votes, self.c is a tunable parameter
        benefit = np.sum(self.preference * work.preference)
        nv = (self.quad_vote_const / self.quad_token_const) * benefit
        # nv>0为支持票，nv<0为反对票
        return nv

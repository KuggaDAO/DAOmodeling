import numpy as np
import sympy as sp

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
        self.a = configs['vote']['quad']['p_a']
        self.b = configs['vote']['quad']['p_b']
        self.c = configs['vote']['quad']['p_c']
        self.activity = np.random.uniform(low=0, high=1)    # Activity of user, used to decide who vote first

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
        # nv = (self.quad_vote_const / self.quad_token_const) * benefit
        nv = self.probability_estimate(benefit)
        # nv>0为支持票，nv<0为反对票
        return nv

    def probability_estimate(self, benefit):
        t = sp.Symbol('t')
        if benefit > 0:
            f = (2 * (self.a + (self.b * t) / (self.c + t))-1) * benefit - self.quad_token_const * t ** 2
        else:
            f = - (2 * (self.a - (self.b * t) / (self.c - t)) - 1) * benefit - self.quad_token_const * t ** 2
        f_diff = sp.diff(f, t)
        solution = sp.solve(f_diff, t)
        for n in range(len(solution)):
            solution[n] = sp.re(solution[n])
            if solution[n] * benefit < 0:
                solution[n] = 0
        value = f.evalf(subs={t: solution[0]})
        pos = 0
        for i in range(1, len(solution)):
            if f.evalf(subs={t: solution[i]}) > value:
                value = f.evalf(subs={t: solution[i]})
                pos = i
        return solution[pos]

    def sequential_voting(self, condition):
        benefit = np.sum(self.preference * condition.work.preference)
        v = sum(condition.votes)
        if v*benefit > 0:
            flag = 1
        else:
            flag = -1
        t = sp.Symbol('t')
        a = 0.5 * (1 + flag * (condition.complete - 1) / (condition.complete + condition.wait))
        b = 0.5 * (1 - flag * (condition.complete - 1) / (condition.complete + condition.wait))
        c = self.c
        if benefit > 0:
            p = a + b * t / (c + t)
        else:
            p = a - b * t / (c - t)
        f = (2 * p - 1) * abs(benefit) - self.quad_token_const * t ** 2
        f_diff = sp.diff(f, t)
        solution = sp.solve(f_diff, t)
        for n in range(len(solution)):
            solution[n] = sp.re(solution[n])
            if solution[n] * benefit < 0:
                solution[n] = 0
        value = f.evalf(subs={t: solution[0]})
        pos = 0
        for i in range(1, len(solution)):
            if f.evalf(subs={t: solution[i]}) > value:
                value = f.evalf(subs={t: solution[i]})
                pos = i
        return solution[pos]

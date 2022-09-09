import numpy as np
import sympy as sp
import math

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

    def cal_benefit(self, work):
        #calculate the benefit between a work and a member
        return np.sum(self.preference * work.preference)

    def probability_estimate(self, benefit):
        t = sp.Symbol('t')
        if benefit > 0:
            f = (2 * (self.a + (self.b * t) / (self.c + t)) - 1) * benefit - self.quad_token_const * t ** 2
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

    def votes_with_forecast(self, work, T, a, r):
        """
        return the number of votes going to be made
        with estimating the winning odds of the situation
        !这里的doctest没有测试作用
        >>> configs = {'preference': {'dim': 5}, 'vote': {'quad': {'token_const': 1.0, 'vote_const': 1.0, 'p_a': 1.0, 'p_b': 10.0, 'p_c': 10.0}}}
        >>> m = Member(None, configs)
        >>> m.preference = [1, 1]
        """
        benefit = self.cal_benefit(work)
        expectation = []
        #因为无法求导，这里用的方法是逐一求出并手动挑选出最大值。
        #如果有数学系的大佬没准可以尝试一下积分号下求导
        #作者还没想过这个问题
        for t in range(20):
            e = 2 * self.binary_probability(T, a+t, r) - 1
            if benefit > 0:
                expectation.append(e * benefit - self.quad_token_const * t * t)
            else:
                expectation.append((-e) * benefit - self.quad_token_const * t * t)
        print(expectation.index(max(expectation)), end=" ")
        return expectation.index(max(expectation))

    def binary_probability(self, T, a, r):
        """
        经典二项分布的累积概率
        return the odds of agree the work
        formula: (n-k)*(n k)*integrate t^n-k-1 * (1-t)^k dt 
        from 0 to 1-p
        >>> configs = {'preference': {'dim': 5}, 'vote': {'quad': {'token_const': 1.0, 'vote_const': 1.0, 'p_a': 1.0, 'p_b': 10.0, 'p_c': 10.0}}}
        >>> m = Member(None, configs)
        >>> abs(m.binary_probability(20, 0, 0) - 0.5) < 0.01
        True
        """
        n = T - a - r#number of votes remaining
        k = T // 2 - a#votes needed to win
        if k > n:
            return 0
        if T // 2 - r + 1 > n:
            return 1
        t = sp.Symbol('t')
        f = t**(n-k-1) * (1-t)**k
        lose_or_tie = (n - k) * math.comb(n, k) * sp.integrate(f, (t, 0, 0.5))#note that if n is a even number the vote may tie
        if T % 2 == 0:
            v = T // 2 - a
            tie_probability = math.comb(n, v) * 0.5**v * 0.5**(n-v)
        else:
            tie_probability = 0
        return 1 - lose_or_tie + tie_probability * 0.5

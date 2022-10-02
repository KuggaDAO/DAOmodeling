import numpy as np
import sympy as sp
import math

class Member:
    def __init__(self, label=None, token=0.0, logic="euqal", configs):
        """
        初始化一个Member对象
        """
        self.label = label#用户的标签
        self.token = token#用户的代币量
        self.logic_type = logic_type
        self.configs = configs
        self.init_preference()

    def init_preference(self):
        pf_configs = self.configs['preference']['Member']
        dis_configs = pf_configs['distribution']

        if dis_configs['type']=="Gaussion":
            self.preference = np.random.randn(
                pf_configs['dim']
            )*dis_configs['sigma'] + dis_configs['mu']
        
        elif dis_configs['type']=="Uniform":
            self.preference = np.random.uniform(
                dis_configs['low'],dis_configs['high'],
                size=[pf_configs['dim']]
            )

############以下是基础方法############
        
    def decide(self, work):
        """
        普通成员的vote.
        """
        if logic == 'equal':
            return self.equal_vote(work)
        elif logic == 'nonlinear':
            return self.nonlinear_logic(work)
        elif logic == 'sequential':
            return self.sequential_logic(work)
        elif logic == 'odds':
            return self.odds_logic(work)
        else:
            raise RuntimeError("vote logic not found")
    
    def __str__(self):
        return "Member:"+str(self.label)

    def cal_benefit(self, work):
        #calculate the benefit between a work and a member
        return np.sum(self.preference * work.preference)

###########以下是投票逻辑##############

    def equal_vote(self, work):
        # one person one vote
        benefit = self.cal_benefit(work)
        if benefit > 0:
            return 1
        else:
            return -1

    def nonlinear_logic(self, work):
        """
        非线性的概率估计投票方法
        """
        log_configs = self.configs['preference']['logic']['const']
        a = self.log_configs['a']
        b = self.log_configs['b']
        c = self.log_configs['c']
        quad_token_const = self.log_configs['quad_token_const']
        benefit = self.cal_benefit(work)
        t = sp.Symbol('t')
        if benefit > 0:
            f = (2 * (a + (b * t) / (c + t))-1) * benefit - quad_token_const * t ** 2
        else:
            f = - (2 * (a - (b * t) / (c - t)) - 1) * benefit - quad_token_const * t ** 2
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

    def sequential_logic(self, work):
        """
        有顺序地估计概率的投票方法
        """
        c = self.configs['c']
        benefit = self.cal_benefit(work)
        v = sum(condition.record)
        if v*benefit > 0:
            flag = 1
        else:
            flag = -1
        t = sp.Symbol('t')
        a = 0.5 * (1 + flag * (condition.complete - 1) / (condition.complete + condition.wait))
        b = 0.5 * (1 - flag * (condition.complete - 1) / (condition.complete + condition.wait))
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

    def odds_logic(self, work):
        """
        根据投票形式估计胜率的投票方法
        """
        T = self.configs['T']
        a = self.configs['a']
        r = self.configs['r']
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
        
        benefit = self.cal_benefit(work)
        expectation = []
        #因为无法求导，这里用的方法是逐一求出并手动挑选出最大值。
        for t in range(20):
            e = 2 * self.binary_probability(T, a+t, r) - 1
            if benefit > 0:
                expectation.append(e * benefit - quad_token_const * t * t)
            else:
                expectation.append((-e) * benefit - quad_token_const * t * t)
        return expectation.index(max(expectation))

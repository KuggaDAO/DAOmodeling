import numpy as np
from .Member import Member

class Forget_Member(Member):
    def decide(self, vote):
        forget_chance = self.configs['forget_chance']
        if forget_chance > np.random.rand():
            return 0
        else:
            if self.logic == 'equal':
                return self.equal_vote(work)
            elif self.logic == 'nonlinear':
                return self.nonlinear_logic(work)
            elif self.logic == 'sequential':
                return self.sequential_logic(work)
            elif self.logic == 'odds':
                return self.odds_logic(work)
            else:
                raise RuntimeError("vote logic not found")

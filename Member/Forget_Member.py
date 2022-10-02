import numpy as np
from .Member import Member

class Forget_Member(Member):
    def decide(self, vote, logic):
        forget_chance = self.configs['forget_chance']
        if forget_chance > np.random.rand():
            return 0
        else:
            return logic(vote)

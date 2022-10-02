import numpy as np

class Work:
    def __init__(self,preference=np.random.rand(5)):
        self.preference = preference
        self.votes = []
        self.ans = None

    def __str__(self):
        return self.preference

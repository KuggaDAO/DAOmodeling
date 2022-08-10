import numpy as np


class Member:
    def __init__(self, label, emotion=np.random.rand(), token=0):
        self.label = label
        self.token = token
        self.emotion = emotion
        return

    def __str__(self):
        return self.label

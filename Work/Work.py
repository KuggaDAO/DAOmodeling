import numpy as np

class Work:
    def __init__(self,label,configs):
        self.label=label
        self.preference=np.random.randn(
            configs['preference']['dim']
        )

    def __str__(self):
        return self.label
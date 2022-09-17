import numpy as np

class Work:
    def __init__(self,label,configs,manual=False,addition=0):
        self.label=label
        if manual:
            self.preference = np.array(manual)
        else:
            self.preference=np.random.randn(
                configs['preference']['dim']
            )
        for p in self.preference:
            p += addition

    def __str__(self):
        return self.label

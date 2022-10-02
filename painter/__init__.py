import matplotlib.pyplot as plt
import numpy as np

__all__ = ["token_tendency"]

#paint growth trend of tokens
def token_tendency(tokens):
    tokens = np.array(tokens)
    n_work, n_member = tokens.shape[0], tokens.shape[1]
    for i in range(n_member):
        plt.plot(range(n_work), tokens[:, i].reshape(-1), label=i)
    plt.legend(loc='best', frameon=False)
    plt.xlabel("work")
    plt.ylabel("tokens")

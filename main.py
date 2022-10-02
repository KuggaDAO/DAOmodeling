import matplotlib.pyplot as plt
from ruamel import yaml
import numpy as np

# a dict discribing global configs
with open('./config.yml', 'r') as f:
    configs = yaml.load(f, yaml.Loader)

from Work import *
from Member import *
from Organization import *
from Painter import *

"""
#plot configurations
plt.subplot(1, 2, 1)
token_tendency(vote_test.token_voting)
plt.subplot(1, 2, 2)
draw_prefer_diff_minispantree(members)
plt.show()
"""

works = []
members = []
for _ in range(5):
    works.append(Work())
    members.append(Member(token=1000.0, a=1.0, b=1.0, c=10.0, quad_token_const=0.1))
o = Organization()
o.add_work(works)
o.add_member(members)
o.vote_all('nonlinear')

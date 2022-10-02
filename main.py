import matplotlib.pyplot as plt
from ruamel import yaml
import numpy as np

# a dict discribing global configs
with open('./config.yml', 'r') as f:
    config = yaml.load(f, yaml.Loader)

from Work import *
from Member import *
from Organization import *
from Painter import *

works = []
members = []
for _ in range(5):
    works.append(Work())
    members.append(Member(extra=configs))
o = Organization()
o.add_work(works)
o.add_member(members)
o.vote_all('nonlinear')

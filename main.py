from ruamel import yaml
import numpy as np

# a dict discribing global configs
with open('./config.yml', 'r') as f:
    configs = yaml.load(f, yaml.Loader)

from Work import *
from Network import *
from Vote import *

n_work=2
n_member=5
works=[]
members=[]
for i in range(n_work):
    works.append(Work(i,configs))
for i in range(n_member):
    members.append(Member(i,configs,token=1000.0))

vote_test=Vote_quadratic(members,works,configs)

vote_test.voting()
benefit=vote_test.collect_benefit()

for i in range(n_work):
    print(np.sum(benefit[i]))
    print(vote_test.votes[i])
    print(vote_test.vote_ans[i])
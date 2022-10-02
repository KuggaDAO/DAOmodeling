#测试脚本

import numpy as np
import matplotlib.pyplot as plt

from ruamel import yaml
from Work import *
from Network import *
from Vote_sequential import Vote_Sequential

with open('../config.yml', 'r') as f:
    configs = yaml.load(f, yaml.Loader)

N_vote = 20         # number of voting times
N_member = 20       # number of members

members = []
works = []
flag = []         # sgn( sum(vote) * sum(benefit))
total_benefit_record = []
total_benefit = 0
last_vote = []
last_benefit = []
outcomes = []
last_dependence = []
last_member = []

for n in range(N_member):
    members.append(Member(n, configs, token=1000.0))

for n in range(N_vote):
    works.append(Work(n, configs))
    benefit_sum = 0
    for m in range(N_member):
        benefit_sum += np.sum(members[m].preference * works[n].preference)
    vote = Vote_Sequential(members, works[n], configs)
    vote.vote()
    flag.append(np.sign(vote.outcome * benefit_sum))
    total_benefit += vote.outcome * benefit_sum
    total_benefit_record.append(total_benefit)
    last_vote.append(vote.condition.votes[-1])
    last_benefit.append(np.sum(members[-1].preference * works[n].preference))
    outcomes.append(vote.outcome)
    last_dependence.append(vote.outcome * last_benefit[-1])
    last_member.append(members[-1].label)
print(flag)
print(total_benefit_record)
print(last_dependence)
print(sum(last_dependence))
print(last_member)

fig1, ax1 = plt.subplots()
ax1.plot([n for n in range(N_vote)], total_benefit_record)
plt.show()

"""
fig2, ax2 = plt.subplots()
ax2.plot([n for n in range(N_vote)], last_dependence)
plt.show()
"""

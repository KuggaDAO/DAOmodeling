import matplotlib.pyplot as plt
from ruamel import yaml
import numpy as np

from work import *
from member import *
from runners import *

def set_configs():
    with open('./configs.yml', 'r') as f:
        configs = yaml.load(f, yaml.Loader)
    
    Work.configs=configs
    Member.configs=configs
    Runner.configs=configs


set_configs()

n_member=3
n_work=500

members=[]
works=[]
for i in range(n_member):
    members.append(Member(label=i,token=50.))
for i in range(n_work):
    works.append(Work(label=i,n_choice=3))

vote_runner=Vote_Runner(members=members,works=works)

vote_runner.vote_works()

vote_runner.show_token_record()

plt.clf()
for member in members:
    plt.arrow(0,0,member.preference[0],member.preference[1],label=member)
plt.legend()
plt.savefig("2.jpg")
import matplotlib.pyplot as plt
from ruamel import yaml
import numpy as np

from work import *
from member import *

def set_configs():
    with open('./configs.yml', 'r') as f:
        configs = yaml.load(f, yaml.Loader)
    
    Work.configs=configs
    Member.configs=configs


set_configs()

w1=Work(random=False,preferences=[[1,2,3,4,5],[1,2,3,4,5]])

print(w1.preferences)
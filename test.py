import matplotlib.pyplot as plt
from ruamel import yaml
import numpy as np

from work import *
from member import *
# from runners import *

def set_configs():
    with open('./configs.yml', 'r') as f:
        configs = yaml.load(f, yaml.Loader)
    
    Work.configs=configs
    Member.configs=configs
    # Runner.configs=configs


set_configs()

m1=Member(label="sfovbo")
m2=Member()

w1=Work()
w2=Work()
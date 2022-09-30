import numpy as np
import sys

from .Logic import logic2rule

class Member:
########## 初始化功能 ##########
    def __init__(self, label=None, token=0.0,\
        logic_type="Equal_Logic", **configs):
        self.label = label
        self.token = token

        # 如果逻辑类型错误,报错并终止程序
        if logic2rule(logic_type)=="invalid type":
            raise ValueError(
                "Member:{} logic_type error\n".format(
                    self.label)
            )
        self.logic_type = logic_type

        self.configs = configs
        self.init_preference()
 
    def init_preference(self):
        pf_configs = self.configs['Member']['preference']
        dis_configs = pf_configs['distribution']

        if dis_configs['type']=="Gaussion":
            self.preference = np.random.randn(
                pf_configs['dim']
            )*dis_configs['sigma'] + dis_configs['mu']
        
        elif dis_configs['type']=="Uniform":
            self.preference = np.random.uniform(
                dis_configs['low'],dis_configs['high'],
                size=[pf_configs['dim']]
            )


########## 基础方法 ##########
    # 对象统一输出格式 "类名称:编号"
    def __str__(self):
        return "Member:"+str(self.label)
    
    # 基于提供的condition信息的决策函数
    def decide(self, condition):
        if condition.vote_rule!=logic2rule(self.logic_type):
            raise Exception(
                "Member:{} logic_type not match vote_rule\n".format(
                    self.label)
            )
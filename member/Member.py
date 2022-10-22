import numpy as np

from .Logic import *

class Member:
    # 基本设置信息configs为静态变量
    configs=None

    def __init__(self, label=None, token=0.0,\
        logic_type="Equal_Logic", **kwargs):
        self.label = label
        self.token = token

        # 如果逻辑类型错误,报错并终止程序
        if logic2rule(logic_type)=="invalid type":
            raise Exception(
                "logic_type error\n"
            )
        self.logic_type = logic_type

        self.init_preference()

    # 初始化自身的preference向量
    def init_preference(self):
        pf_configs = Member.configs['preference']
        dis_configs = pf_configs['Member']['distribution']

        if dis_configs['type']=="Gaussion":
            self.preference = np.random.randn(
                pf_configs['dim']
            )*dis_configs['sigma'] + dis_configs['mu']
        
        elif dis_configs['type']=="Uniform":
            self.preference = np.random.uniform(
                dis_configs['low'],dis_configs['high'],
                size=[pf_configs['dim']]
            )
        else:
            self.preference=None
    
    # 打印身份信息
    def __str__(self):
        return "Member:"+str(self.label)

    # 投票中的决策函数
    def decide(self,condition):
        # 如果决策类型和投票的规则不匹配,报错并终止程序
        if condition.vote_rule!=logic2rule(self.logic_type):
            raise Exception(
                "Member:{} logic_type not match vote_rule\n".format(
                    self.label)
            )
        
        if self.logic_type=="Equal_Logic":
            return Equal_Logic.calculation(self,condition)
    
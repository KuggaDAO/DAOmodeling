from inspect import stack
from os import stat
from sqlite3 import adapt
import numpy as np
import sympy as sp
import math

__all__=['logic2rule','Equal_Logic']

# 将逻辑的名称logic转化为预期匹配的规则名称rule
def logic2rule(logic_type):
    if logic_type=="Equal_Logic":
        return "equal"
    elif logic_type=="Sequential_Logic":
        return "quadratic"
    else:
        return "invalid type"

class Logic:
    logic_type="Base_Logic"

    # 验证决策类型与投票规则是否匹配
    @staticmethod
    def rule_match(logic_type, condition):
        if condition.vote_rule!=logic2rule(logic_type):
            raise Exception(Logic.logic_type +\
                "logic_type({}) not match vote_rule({})\n".format(
                    logic_type, condition.vote_rule
                ))

class Equal_Logic(Logic):
    logic_type="Equal_Logic"

    # 返回一个n_choice长度的一维数组
    # 由于只能投一票,所以数组中只能有一个数字为1
    @staticmethod
    def calculation(member, condition):
        Logic.rule_match(Equal_Logic.logic_type,condition)

        n_choice=condition.work.n_choice
        decision=np.zeros([n_choice])
        max_i=0
        max_benefit=np.sum(member.preference*\
                condition.work.preferences[0])
        for i in range(1,n_choice):
            benefit=np.sum(member.preference*\
                condition.work.preferences[i])
            if benefit>= max_benefit:
                max_i=i
                max_benefit=benefit
        
        decision[max_i]=1
        return decision
        



            

        

        
        

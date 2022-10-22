from Runner import Runner
from work import *
from member import *
import numpy as np

# 进行投票的脚本类，增加了脚本中的worklist
class Vote_Runner(Runner):
    def __init__(self, name="DAO", vote_rule="equal", **kwargs):
        super().__init__(name, **kwargs)
        # 投票规则默认为equal vote
        self.vote_rule=vote_rule

        # works=Work list触发
        # 在初始化的时候添加抽象投票对象
        if kwargs.get("works")!=None:
            self.works=kwargs.get("works")
            # 检查worklist规范性
            self.check_object_list(self.works, Work)
        else:
            self.works=[]

    # 添加新抽象投票对象
    def add_works(self, new_works):
        # 检查worklist规范性
        self.check_object_list(new_works, Work)

        self.works.extend(new_works)
    
    # 打印抽象投票对象信息
    def show_works(self,*args):
        for work in self.works:
            # 打印work的标签
            print(work,end="")
            # 打印其余附加信息，如preferences
            # 以show_members("preferences")的args输入方式进行
            for arg in args:
                print(" "+arg+": {}".format(
                    eval("work."+arg)
                ),end="")
            print()

    # 对所有work进行投票
    def vote_works(self):
        # 所有的投票情况decision_all和所有的投票结果vote_ans
        self.decisions_all=[]
        self.vote_ans=[]

        # 初始化condition
        condition=Vote_Condition(self.vote_rule)

        for work in self.works:
            condition.update(work=work)

            # 单轮投票中的实时投票情况记录
            decisions=[]
            for member in self.members:
                decision=member.decide(condition)
                decisions.append(decision)
                condition.update(decisions=decisions)
            
            # 更新投票的结果
            self.vote_ans.append(self.collect_ans(decisions))
            condition.update(vote_ans=self.vote_ans)

            # 更新所有的投票信息
            self.decisions_all.append(decisions)
            condition.update(decisions_all=self.decisions_all)

    
    

            
    # 统计投票情况计算投票结果
    @staticmethod
    def collect_ans(decisions):
        decisions=np.array(decisions)
        # 统计每个选项的票数
        total=np.sum(decisions,axis=0).tolist()
        # 最大票数的index
        maxi=total.index(max(total))
        return maxi



                
            
            
        

class Vote_Condition:
    def __init__(self,vote_rule):
        self.vote_rule=vote_rule
    
    def update(self,**kwargs):
        for key in kwargs.keys():
            eval("self."+key+"=kwargs[key]")
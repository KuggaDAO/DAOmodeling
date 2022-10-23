from .Runner import Runner
from work import *
from member import *
import numpy as np
import matplotlib.pyplot as plt

# 进行投票的脚本类，增加了脚本中的worklist
class Vote_Runner(Runner):
    def __init__(self, name="DAO", vote_rule="equal",\
        distribute_rule="proportional", **kwargs):
        super().__init__(name, **kwargs)
        # 投票规则默认为equal vote
        self.vote_rule=vote_rule
        # 分发代币的规则
        self.distribute_rule=distribute_rule

        self.token_record=[]

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

        # 记录token变化
        self.collect_token()

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
            ans=self.collect_ans(decisions)
            work.ans=ans
            self.vote_ans.append(ans)
            condition.update(vote_ans=self.vote_ans)

            # 更新所有的投票信息
            self.decisions_all.append(decisions)
            condition.update(decisions_all=self.decisions_all)

            # 根据投票规则收取投票所需代币
            token_cost=self.cost_token(decisions,self.vote_rule)

            # 收取代币后重新分发代币
            self.distribute_token(token_cost.sum())

            # 根据投票结果分发奖励
            self.award_token(work,ans)

            # 收集token
            self.collect_token()


            
    # 投票代币的重新分发
    def distribute_token(self,token_collected):
        n_member=len(self.members)
        token_distribution=np.ones(n_member)
        # 平均分发代币
        if self.distribute_rule=="average":
            token_distribution=token_distribution*token_collected/n_member
        elif self.distribute_rule=="proportional":
            # 统计手头上剩下所有代币数量
            token_total=0
            for member in self.members:
                token_total+=member.token
            token_distribution=token_distribution/token_total
            
            for i in range(n_member):
                token_distribution[i]*=self.members[i].token
            
        # 重新分发
        self.update_token(token_distribution)
            
    # 计算每个成员消耗的代币值
    # 根据投票规则进行代币的收取，如果是equal投票无需收取代币
    def cost_token(self,decisions,vote_rule):
        decisions=np.array(decisions)
        token_cost=np.zeros([decisions.shape[0]])
        if vote_rule=="equal":
            pass
        elif vote_rule=="quadratic":
            # 根据quadratic投票的投票常数token_cost进行计算
            for i in decisions.shape[0]:
                decision=decisions[i]
                token_const=Vote_Runner.configs["rule"]["token_const"]
                token_cost=token_const*(decision.sum())**2
        
        self.update_token(token_cost)
        return token_cost
    
    # 分发投票奖励
    def award_token(self,work,ans):
        n_member=len(self.members)
        award=np.zeros(n_member)

        for i in range(n_member):
            award[i]=np.sum(
                work.preferences[ans]*self.members[i].preference
            )
        
        self.update_token(award)
    
    # 收集各个member的token
    def collect_token(self):
        record=[]
        for member in self.members:
            record.append(member.token)
        self.token_record.append(record)

    # 展示token变化
    def show_token_record(self):
        n_work=len(self.works)
        n_member=len(self.members)

        record=np.array(self.token_record)
        for i in range(n_member):
            plt.plot(range(n_work+1),record[:,i],\
                label=self.members[i])
        plt.legend()
        plt.savefig("1.jpg")


    # 统计投票情况计算投票结果
    # 对所有runner的计算方法都一致，故设为静态函数
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
            exec("self."+key+"=kwargs[key]")
from cmath import exp
from os import pread
import numpy as np

class Work:
    # 基本设置信息configs为静态变量
    configs=None

    def __init__(self,n_choice=2,random=True,**kwargs):
        # 若没有指明该work的选项个数，则默认为两个选项
        self.n_choice=n_choice
        
        # 判断work的选项preference信息是否随机生成
        # 如果random=False则需要手动输入数据
        if random==False:
            # 判断是否存在手动输入数据
            if "preferences" not in kwargs.keys():
                raise Exception(
                    "need preferences data\n"
                )
            
            self.preferences=np.array(kwargs.get("preferences"))

            # 判断手动输入数据类型是否正确
            if self.preferences.shape[0]!=self.n_choice or\
                self.preferences.shape[1]!=\
                    Work.configs['preference']['dim']:
                raise Exception(
                    "preferences size error\n"
                )
        else:
            self.preferences=[]
            for i in range(self.n_choice):
                self.preferences.append(
                    Work.get_preference()
                )
            self.preferences=np.array(self.preferences)
        
        # 判断是否获得简化版的work对象
        # 即两个选项preference为一组相反数
        if kwargs.get("simplify")==True:
            # 如果不为两个选项,报错
            if self.n_choice!=2:
                raise Exception(
                    "only work of 2 choices could be simplified\n"
                )
            # 取反操作
            self.preferences[1]=-self.preferences[0]
    
    # 根据configs信息获取单个preference
    @staticmethod
    def get_preference():
        pf_configs = Work.configs['preference']
        dis_configs = pf_configs['Work']['distribution']

        if dis_configs['type']=="Gaussion":
            preference = np.random.randn(
                pf_configs['dim']
            )*dis_configs['sigma'] + dis_configs['mu']
        
        elif dis_configs['type']=="Uniform":
            preference = np.random.uniform(
                dis_configs['low'],dis_configs['high'],
                size=[pf_configs['dim']]
            )
        
        return preference

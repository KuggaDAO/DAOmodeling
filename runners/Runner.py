'''
Runner类为所有脚本类的父类,其中包含了基础功能
为接下来的Vote_Runner以及后续其他Runner类提供遍历
'''
from work import *
from member import *
import numpy as np

class Runner:
    # 设置基本信息configs为静态变量
    configs=None

    def __init__(self,name="DAO",**kwargs):
        self.name=name
        
        # members=Member list触发
        # 在初始化的时候添加成员对象
        if kwargs.get("members")!=None:
            self.members=kwargs.get("members")
            # 检查memberlist规范性
            self.check_object_list(self.members, Member)
        else:
            self.members=[]
    
    # 添加新成员
    def add_members(self, new_members):
        # 检查memberlist规范性
        self.check_object_list(new_members, Member)

        self.members.extend(new_members)

    # 打印成员列表信息
    def show_members(self,*args):
        for member in self.members:
            # 打印label
            print(member,end="")
            # 打印其余附加信息，如preference和token
            # 以show_members("preference","token")的args输入方式进行
            for arg in args:
                print(" "+arg+": {}".format(
                    eval("member."+arg)
                ),end="")
            print()
            
    # 更新全体成员token信息
    def update_token(self, tokens):
        n_member=len(self.members)
        for i in range(n_member):
            self.members[i]+=tokens[i]


    # 检查传入的object list规范性
    # 可以同时用于memberlist和worklist的检查
    @staticmethod
    def check_object_list(objects, object_class):
        # 判断是否是list
        if type(objects)!=type([]):
            raise Exception(
                    "Runner only accept {} list\n".format(
                        object_class
                    )
                )
        
        # 判断list中元素是否是object对象
        for object in objects:
            if isinstance(object, object_class)==False:
                raise Exception(
                    "list only contain object of class {}".format(
                        object_class
                    )
                )







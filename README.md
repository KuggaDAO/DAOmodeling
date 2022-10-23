# DAOmoeling

这个项目旨在对不同的去中心化自治组织(Decentralized Autonomous Organization,下简称DAO)进行建模.

## requirements

使用以下指令安装项目所需的python安装包:

```setup
pip install -r requirements.txt
```

## project structure

项目目前主要由以下几个结构组成:

- work
  
  Work类的基本定义和相关附属功能:Work类是DAO中投票对象的抽象,其对象包含了DAO中单次投票对象的特征信息.

- member
  
  Member类的基本定义和相关附属功能：Member类是DAO成员的抽象，其对象包含了DAO成员的基本信息(姓名或编号,代币数等),以及描述DAO成员决策逻辑的函数或对象.

- runners
  
  运行DAO模拟的执行模块:目前仅有关于投票模拟的Vote_Runner类,其主要作用类似运行整个投票模拟的脚本.

- configs.yml
  
  运行DAO模拟的基本设置信息:关于Work,Member等类的基础设置信息.

- requirements.txt
  
  项目所需python安装包

- readme.md
  
  项目介绍文件

## ideas

1. configs.yml仅提供最基本的DAO建模的设置信息,更多复杂灵活的设置信息需要手动通过python函数的keyword arguments功能传入.通过configs.yml设置的基本信息configs将设置为各类的静态变量，减少内存开销.
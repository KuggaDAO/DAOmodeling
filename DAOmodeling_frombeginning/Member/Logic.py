import numpy as np
import sympy as sp
import math

def logic2rule(logic_type):
    if logic_type=="Equal_Logic":
        return "equal"
    elif logic_type=="Sequential_Logic":
        return "quadratic"
    else:
        return "invalid type"
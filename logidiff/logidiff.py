#!/usr/bin/env python

import sys, re

class Infix:
    def __init__(self, function):
        self.function = function
    def __or__(self, other):
        return self.function(other)
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __truediv__(self, other):
        return self.function(other)
    def __rtruediv__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __call__(self, value1, value2):
        return self.function(value1, value2)

# functions for implementing VHDL operators in python for evaluating statements
# logical
l_and  = Infix(lambda x,y:      x and y)
l_or   = Infix(lambda x,y:      x  or y)
l_nand = Infix(lambda x,y: not (x and y))
l_nor  = Infix(lambda x,y: not (x  or y))
l_xor  = Infix(lambda x,y:      x  != y)
l_xnor = Infix(lambda x,y:      x  == y)

dont_touch = ['and', 'or', 'nand', 'nor', 'xor', 'xnor', 'not']

def clean(statement):
    statement = statement.replace('(', ' ( ')
    statement = statement.replace(')', ' ) ')
    statement = statement.replace('=', ' == ')
    return statement

def replace_logic(statement):
    statement = statement.replace( ' and ', ' |l_and| ')
    statement = statement.replace(  ' or ',  ' |l_or| ')
    statement = statement.replace(' nand ',' |l_nand| ')
    statement = statement.replace( ' nor ', ' |l_nor| ')
    statement = statement.replace( ' xor ', ' |l_xor| ')
    statement = statement.replace(' xnor ',' |l_xnor| ')
    return statement

def find_vars(statement):
    vars = []

    for thing in statement.split(' '):
        thing = re.sub(r'[^a-zA-Z0-9_]', '', thing)
        if len(thing) == 0:
            continue
        if thing[0].isnumeric():
            continue
        elif thing in dont_touch:
            continue
        elif thing not in vars:
            vars.append(thing)

    return vars

def replace_vars(statement, vars):
    for i, var in enumerate(vars):
        statement = statement.replace(f' {var} ', f' vars[{i}] ')

    return statement    

if __name__=="__main__":
    input_eq = clean(' '.join(sys.argv[1:]).lower() + ' ')

    vars = find_vars(input_eq)
    var_names = vars.copy()

    input_eq = replace_vars(input_eq, vars)

    num_vars = len(vars)

    for i in range(num_vars):
        vars = list(bin(i)[2:0].zfill(num_vars))
        print(input_eq)
        print(vars)
        print(eval('print(' + input_eq + ')'))
    

    # for thing in inut_eq.split(' '):
        
    #     pass

    # eq1 = replace(input_eq.split('=')[0].strip())
    # eq2 = replace(input_eq.split('=')[1].strip())

    # print(eq1)
    # print(eq2)

    # eval(eq1)


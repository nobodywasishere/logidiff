#!/usr/bin/env python

import sys, re

class Infix:
    def __init__(self, function):
        self.function = function

    def __pow__(self, other):
        # return Infix(lambda x, self=self, other=other: self.function(x))
        return not other

    def __truediv__(self, other):
        return self.function(other)
    def __rtruediv__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __add__(self, other):
        return self.function(other)
    def __radd__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __lshift__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __and__(self, other):
        return self.function(other)
    def __rand__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __xor__(self, other):
        return self.function(other)
    def __rxor__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __or__(self, other):
        return self.function(other)
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __call__(self, value1, value2):
        return self.function(value1, value2)

# functions for implementing VHDL operators in python for evaluating statements
# logical, in order of precedence
l_not  = Infix(lambda x:   not  x      )
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
    # These are like this due to operator precedence
    statement = statement.replace( ' not ',    ' l_not** ')
    statement = statement.replace( ' and ',   ' /l_and/ ' )
    statement = statement.replace(  ' or ',    ' +l_or+ ' )
    statement = statement.replace(' nand ', ' <<l_nand<< ')
    statement = statement.replace( ' nor ',   ' &l_nor& ' )
    statement = statement.replace( ' xor ',   ' ^l_xor^ ' )
    statement = statement.replace(' xnor ',  ' |l_xnor| ' )
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

def evaluate(equation):
    input_eq = clean(' ' + equation.lower() + ' ')

    vars = find_vars(input_eq)
    var_names = vars.copy()

    input_eq = replace_vars(input_eq, vars)
    input_eq = replace_logic(input_eq)

    num_vars = len(vars)

    not_eqs = []

    for i in range(2**num_vars):
        vars = list(bin(i)[2:].zfill(num_vars))
        vars = [int(i) for i in vars]
        result = eval(input_eq.strip())
        if not result:
            thing = []
            for i in range(num_vars):
                thing.append(f'{var_names[i]}: {vars[i]}')
            not_eqs.append(thing)

    return not_eqs

if __name__=="__main__":

    if len(sys.argv) < 2:
        print('No statement to evaluate!')
    
    else:

        not_eqs = evaluate(' '.join(sys.argv[1:]))

        if not_eqs:
            print( 'Statements not equivalent for inputs:')
            for i in not_eqs:
                print(f'  {", ".join(i)}')
        else:
            print( 'Statements are equivalent')


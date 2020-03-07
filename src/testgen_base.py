import numpy as np
import pandas as pd


class Test():
    
    def __init__(self):
        self.variables = np.array(
            [
                "a","b","c","d","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u",
                "v","w","x","y","z"
            ]
        )
        self.digits = np.array(["0","1","2","3","4","5","6","7","8","9"])
        self.arithmetic = np.array(["-","+","*","/"])
        self.equalities = ["==", ">", "<", ">=", "<="]
        self.power = "**"
        self.assignment = "="
        self.if_start = "if CONDITION:\n"
        self.if_else = "else:\n"
        self.if_elif = "elif CONDITION:\n"
        self.list_comprehension = "[FUNCTION(VARIABLE) for VARIABLE in LIST]"
        self.function_start = "def NAME(ARGUMENTS):\n"
        self.function_return = "return(NAME)"
        
    def make_digit(self, min_s=1, max_s=5):
        s = "".join(
            np.random.choice(self.digits, size=np.random.choice(np.arange(min_s, max_s)))
        )
        if s[0] == "0" and len(s) > 1:
            s = s[1:]
        return(s)
        
    def init_variable(self, current_variables):
        if np.random.choice([True, False]):
            s = np.random.choice(self.variables)+" = "+self.random_expression()
        else:
            if len(current_variables) > 0:
                s = np.random.choice(current_variables)+" = "+self.random_expression()
            else:
                s = np.random.choice(self.variables)+" = "+self.random_expression()
        return(s)
    
    def random_expression(self, min_s, max_s):
        s = self.make_digit(min_s, max_s)
        while np.random.choice([True, False]):
            if np.random.choice([True, False]):
                s += np.random.choice(self.arithmetic)
                s += self.make_digit(min_s, max_s)
        return(s)
    
    def make_condition(self, current_variables):
        if len(current_variables) > 0:
            var = np.random.choice(current_variables)
        else:
            var = np.random.choice(self.variables)
        s = var + " " + np.random.choice(self.equalities) + " "
        what = np.random.choice(["variable", "digit", "expression"])
        if what == "variable":
            if len(current_variables):
                s += np.random.choice(current_variables)
            else:
                s += np.random.choice(self.variables)
        elif what == "digit":
            s += self.make_digit()
        else:
            s += self.random_expression()
        return(s)
    
    def make_code(self, n):
        code = []
        current_variables = []
        open_ifs = []
        block_count = 0
        prev = "start"
        for a in range(n):
            what = np.random.choice(
                [
                    "assignment", "if_start", "if_elif", "if_else", "b++", "b--"
                ], p = [0.5, 0.3, 0.09, 0.09, 0.01, 0.01]
            )
            if what == "assignment":
                line = self.init_variable(current_variables)
                current_variables.append(line[0])
                current_variables = list(set(current_variables))
                code.append(block_count*"    ")
                code.append(line)
            elif what == "b++":
                block_count += 1
            elif what == "b++":
                block_count -= 1
            elif what == "if_start":
                if a != n-1 and n != 0:
                    code.append(block_count*"    ")
                    code.append(self.if_start.replace("CONDITION", self.make_condition(current_variables)))
                    block_count += 1
                    open_ifs.append(block_count)
                else:
                    code.append(block_count*"    ")
                    line = self.init_variable(current_variables)
                    current_variables.append(line[0])
                    current_variables = list(set(current_variables))
                    code.append(line)
            elif what == "if_elif":
                if prev == "assignment" and a != n-1 and n != 0:
                    if len(open_ifs) > 0:
                        if open_ifs[-1] == block_count:
                            code.append(
                                self.if_elif.replace("CONDITION", self.make_condition(current_variables))
                            )
                            block_count += 1
                else:
                    if len(open_ifs) > 0:
                        block_count = open_ifs[-1]
                    code.append(block_count*"    ")
                    line = self.init_variable(current_variables)
                    current_variables.append(line[0])
                    current_variables = list(set(current_variables))
                    code.append(line)
            elif what == "if_else":
                if prev == "assignment" and a != n-1 and n != 0:
                    if len(open_ifs) > 0:
                        if open_ifs[-1] == block_count:
                            code.append(
                                self.if_else.replace("CONDITION", self.make_condition(current_variables))
                            )
                            block_count += 1
                else:
                    if len(open_ifs) > 0:
                        block_count = open_ifs[-1]
                    code.append(block_count*"    ")
                    line = self.init_variable(current_variables)
                    current_variables.append(line[0])
                    current_variables = list(set(current_variables))
                    code.append(line)
            code += "\n"
            prev = what
      #  print(a, what)
        if len(current_variables) > 0:
            to_output = np.random.choice(current_variables)
        else:
            to_output = np.random.choice(variables)
        code += "print("+np.random.choice(current_variables)+")"
        return(code, current_variables)
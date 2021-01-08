from collections import deque
from enum import Enum
from operator import add, sub, mul, floordiv
import re
from var_dict import VarDict


class ValidCommand(Enum):
    HELP = "/help"
    EXIT = "/exit"


def execute_command(command: ValidCommand):
    if command is ValidCommand.HELP:
        print("some information about the program.")

    elif command is ValidCommand.EXIT:
        print("Bye!")
        exit()


class Calculator:
    __vars_ = VarDict()

    __op_priority = {"+": 1, "-": 1, "*": 2, "/": 2}

    __op_func = {"+": add, "-": sub, "*": mul, "/": floordiv}


    def eval(self, expr: str):
        expr = expr.replace(" ", "")
        self.__check_valid_expr(expr)
        if "=" in expr:
            try:
                self.__vars_[expr[:expr.find("=")]] = self.__calculate(expr[expr.find("=")+1:])
                return None
            except (SyntaxError, ValueError):
                raise ValueError("Invalid assignment")
        else:
            return self.__calculate(expr)


    def __check_valid_expr(self, expr: str):
        expr = expr.replace(" ", "")
        if "=" in expr:

            if not expr[:expr.find("=")].isalpha():
                raise SyntaxError("Invalid identifier")

            elif expr.count("=") > 1:
                raise ValueError("Invalid assignment")

            else:
                try:
                    self.__check_valid_expr(expr[expr.find("=") + 1:])

                except (SyntaxError, ValueError):
                    raise ValueError("Invalid assignment")
        else:
            if any(var not in self.__vars_ for var in re.findall('[a-z]+', expr)):
                raise NameError("Unknown variable")

            elif re.findall('[a-z]+[0-9]+', expr):
                raise SyntaxError("Invalid identifier")

            elif re.sub('[ +*/()a-zA-Z0-9]|[-]', '', expr):
                raise ValueError("Invalid expression")

            elif re.findall('[+-][*]+|[+-][/]+|[*/]{2,}', expr):   # '[*][+-]+|[/][+-]+' is ok e.g 9*-2
                raise ValueError("Invalid expression")

            elif expr[0] in ["*", "/"] or expr[-1] in ["*", "/", "+", "-", "("]:
                ValueError("Invalid expression")

            Calculator.__check_balanced_brackets(expr)


    @staticmethod
    def __check_balanced_brackets(expr: str):
        stack = deque()
        try:
            for ch in expr:
                if ch == "(":
                    stack.append(ch)
                elif ch == ")":
                    stack.pop()
            if len(stack) != 0:
                raise ValueError("Invalid expression")

        except IndexError:
            raise ValueError("Invalid expression")


    def __calculate(self, expr: str) -> int:
        try:
            expr = Calculator.__normalize_expr('0+' + expr)     # '0+' is a fix for expressions starting with unary +/-
            postfix_expr = Calculator.__transform_infix_to_postfix(expr)
            calculation_stack = deque()

            for current_term in postfix_expr:

                if Calculator.__is_number(current_term):
                    calculation_stack.append(int(current_term))
                elif current_term.isalpha():
                    calculation_stack.append(int(self.__vars_[current_term]))
                elif current_term in Calculator.__op_priority:
                    b = calculation_stack.pop()
                    a = calculation_stack.pop()
                    calculation_stack.append(Calculator.__op_func[current_term](a, b))

            return calculation_stack.pop()

        except IndexError:
            raise ValueError("Invalid expression")


    # recursive solution;
    # def calc_postfix_step(self, postfix_stack: deque, op: str):
    #     if len(postfix_stack) == 2:
    #         b = postfix_stack.pop()
    #         a = postfix_stack.pop()
    #
    #     else:
    #         b = postfix_stack.pop()
    #         if b in Calculator.__op_priority:
    #             b = self.calc_postfix_step(postfix_stack, b)
    #             a = postfix_stack.pop()
    #             if a in Calculator.__op_priority:
    #                 a = self.calc_postfix_step(postfix_stack, a)
    #         else:
    #             a = postfix_stack.pop()
    #             if a in Calculator.__op_priority:
    #                 a = self.calc_postfix_step(postfix_stack, a)
    #
    #     if isinstance(a, str) and a.isalpha():
    #         a = self.__vars_[a]
    #     if isinstance(b, str) and b.isalpha():
    #         b = self.__vars_[b]
    #
    #     return Calculator.__op_func[op](int(a), int(b))


    @staticmethod
    def __transform_infix_to_postfix(expr: [str]) -> [str]:
        stack = deque()
        res = []
        for term in expr:
            if Calculator.__is_number(term) or term.isalpha():
                res.append(term)
            elif term == "(":
                stack.append(term)
            elif term == ")":
                last_term = stack.pop()
                while last_term != "(":
                    res.append(last_term)
                    last_term = stack.pop()

            elif term in Calculator.__op_priority:
                if not stack:
                    stack.append(term)
                else:
                    last_term = stack.pop()
                    if last_term == "(" \
                        or (last_term in Calculator.__op_priority
                            and Calculator.__op_priority[term] > Calculator.__op_priority[last_term]):
                        stack.append(last_term)
                        stack.append(term)

                    else:
                        while last_term in Calculator.__op_priority \
                                and Calculator.__op_priority[term] <= Calculator.__op_priority[last_term]:
                            res.append(last_term)
                            if not stack:
                                break
                            last_term = stack.pop()
                        if stack:
                            stack.append(last_term)
                        stack.append(term)

        while stack:
            res.append(stack.pop())

        return res


    @staticmethod
    def __normalize_term(term: str) -> str:

        while "++" in term or "--" in term or "+-" in term or "-+" in term:
            while "--" in term:
                term = term.replace("--", "+")
            while "++" in term:
                term = term.replace("++", "+")
            while "+-" in term:
                term = term.replace("+-", "-")
            while "-+" in term:
                term = term.replace("-+", "-")
        return term


    @staticmethod
    def __normalize_expr(expr: str) -> [str]:
        tokenized_expr = re.findall('[*/][+-]+|[+-]+|[0-9]+|[a-zA-Z]+|[*]+|[/]+|[(]|[)]', expr)

        # fix for *,/ followed by a unary +,-; e.g 9*-2.
        for i in range(len(tokenized_expr) - 1):
            if any(op in tokenized_expr[i] for op in ["*-", "*+", "/-", "/+"]):
                tokenized_expr[i + 1] = tokenized_expr[i][1:] + tokenized_expr[i + 1]
                tokenized_expr[i] = tokenized_expr[i][0]

        return [Calculator.__normalize_term(term) for term in tokenized_expr]


    @staticmethod
    def __is_number(expr: str) -> bool:
        return expr.isnumeric() or (expr[0] in "+-" and expr[1:].isnumeric())


def main():
    while 1:
        c = Calculator()
        inp = input()
        if inp.startswith("/"):
            try:
                execute_command(ValidCommand(inp))

            except ValueError:
                print("Unknown command")

        elif inp:
            try:
                res = c.eval(inp)
                if res is not None:
                    print(res)

            except (TypeError, ValueError, NameError, SyntaxError, KeyError, ArithmeticError) as c:
                print(c.args[0])


if __name__ == '__main__':
    main()


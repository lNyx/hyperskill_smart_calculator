from enum import Enum
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


class Eval_:

    __vars_ = VarDict()

    def eval_(self, args: str) -> str:
        if "=" in args:
            self.__eval_assignment(args)
            return ""

        else:
            return str(self.__eval_arith_expr(("+" + self.__parse_var_names(args)).split()))


    def __parse_var_names(self, args: str):
        res = ""
        for term in args.split():
            if any(c.isalpha() for c in term):
                res += " " + term[:len(term)-len(term.lstrip("-+"))] + str(self.__vars_[term.lstrip("-+")])

            else:
                res += " " + term

        return res


    def __eval_assignment(self, args: str):
        var = args[:args.index("=")].strip()
        self.__vars_[var] = 0

        try:
            self.__vars_[var] = \
                self.__eval_arith_expr(self.__parse_var_names("+" + args[args.index("=") + 1:]).split())

        except (ValueError, SyntaxError):
            raise ValueError("Invalid assignment")


    def __eval_arith_expr(self, args: [str]) -> int:
        if not args:
            return 0

        elif len(args) == 1 and not args[0].lstrip("-+").isnumeric():
            raise ValueError("Invalid expression")            # doesn't end on a number, e.g "+1 +", "+1 @"

        else:
            if args[0].lstrip("-+").isnumeric() and args[0][0] in "-+":     # avoid no -/+ between numbers, e.g "1 1"
                return int(args[0].lstrip("-+")) * (-1) ** args[0].count("-") + self.__eval_arith_expr(args[1:])

            elif args[0].lstrip("-+"):                        # isn't just a string of -/+, e.g "1", "+1@", "@"
                raise ValueError("Invalid expression")        # and has chars other than at least one leading -/+ char followed by a number

            else:                       # defer to the next call when arg[0] has only -/+ chars and arg[1] exists
                return self.__eval_arith_expr([args[0] + args[1]] + args[2:])



def main():
    while 1:
        e = Eval_()
        inp = input()
        if inp.startswith("/"):
            try:
                execute_command(ValidCommand(inp))

            except ValueError:
                print("Unknown command")

        elif inp:
            try:
                res = e.eval_(inp)
                if res:
                    print(res)

            except (TypeError, ValueError, NameError, SyntaxError, KeyError) as e:
                print(e.args[0])


if __name__ == '__main__':
    main()

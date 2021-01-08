from enum import Enum


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
    class VarsDict(dict):

        def __setitem__(self, key, value):
            if not isinstance(key, str) or not isinstance(value, int):
                raise TypeError("Invalid identifier or Value")

            elif not key.isalpha():
                raise TypeError("Invalid identifier")      # var name can only contain letters


    vars_ = VarsDict()


    def eval_(self, args: str) -> str:
        if "=" in args:
            self.eval_assignment(args)
            return ""

        else:
            return str(self.eval_arith_expr(("+" + self.parse_var_names(args)).split()))


    def parse_var_names(self, args: str):
        res = ""
        for term in args.split():
            if any(c.isalpha() for c in term):
                try:
                    res += args[:len(args)-len(args.lstrip("-+"))] + str(self.vars_[term.lstrip("-+")])
                except KeyError:
                    raise NameError("Unknown variable")
            else:
                res += term
        return res


    def eval_assignment(self, args: str):
        try:
            self.vars_[args[:args.index("=")]] = \
                self.eval_arith_expr(self.parse_var_names(args[args.index("=")+1:]).split())

        except ValueError:
            raise ValueError("Invalid assignment")



    def eval_arith_expr(self, args: [str]) -> int:
        if not args:
            return 0

        elif len(args) == 1 and not args[0].lstrip("-+").isnumeric():
            raise ValueError("Invalid expression")            # doesn't end on a number, e.g "+1 +", "+1 @"

        else:
            if args[0].lstrip("-+").isnumeric() and args[0][0] in "-+":     # avoid no -/+ between numbers, e.g "1 1"
                return int(args[0].lstrip("-+")) * (-1) ** args[0].count("-") + self.eval_arith_expr(args[1:])

            elif args[0].lstrip("-+"):  # isn't just a string of -/+,                              e.g "1", "+1@", "@"
                raise ValueError("Invalid expression")        # and has chars other than at least one leading -/+ char followed by a number

            else:                       # defer to the next call when arg[0] has only -/+ chars and arg[1] exists
                return self.eval_arith_expr([args[0] + args[1]] + args[2:])



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
                print(e.eval_(inp))

            except (TypeError, ValueError, NameError) as e:
                print(e)

                # print("Invalid identifier")
                # print("Invalid assignment")



if __name__ == '__main__':
    main()

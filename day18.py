from abc import *
from operator import *


class Expression:
    @abstractmethod
    def evaluate(self) -> int:
        return NotImplemented

    @abstractmethod
    def evaluate2(self) -> int:
        return NotImplemented


class AtomicExpression(Expression):
    def __init__(self, value: int):
        self.value = value

    def evaluate(self) -> int:
        return self.value

    def evaluate2(self) -> int:
        return self.value


class CompositeExpression(Expression):
    def __init__(self, sub_expressions, operators):
        self.sub_expressions = sub_expressions
        self.operators = operators

    def evaluate(self) -> int:
        last_value = self.sub_expressions[0].evaluate()
        for i in range(0, len(self.operators)):
            last_value = self.operators[i](last_value, self.sub_expressions[i+1].evaluate())
        return last_value

    def evaluate2(self) -> int:
        # First bracket execute all adds into subexpressions. Avoid endless recursions.
        if len(self.operators) > 1:
            new_exprs = []
            new_operators = []
            last_expr = self.sub_expressions[0]
            for i in range(0, len(self.operators)):
                if self.operators[i].__name__ == 'add':
                    last_expr = CompositeExpression([last_expr, self.sub_expressions[i+1]], [add])
                else:
                    new_exprs.append(last_expr)
                    new_operators.append(self.operators[i])
                    last_expr = self.sub_expressions[i+1]

            new_exprs.append(last_expr)
            last_value = new_exprs[0].evaluate2()
            for i in range(0, len(new_operators)):
                last_value = new_operators[i](last_value, new_exprs[i + 1].evaluate2())
            return last_value
        else:
            return self.operators[0](self.sub_expressions[0].evaluate2(), self.sub_expressions[1].evaluate2())


def parse_expression(line: str) -> Expression:
    # parse from left to right until eof or closing bracket having state: expect_nr or expect_operator
    # when bracket comes: recurse until closing bracket
    pos = 0
    line = line.strip()

    def strip_spaces():
        nonlocal pos
        while pos < len(line) and line[pos] == ' ':
            pos += 1

    def parse_operator():
        nonlocal  pos
        strip_spaces()
        char = line[pos]
        pos += 1
        strip_spaces()

        if char == '+':
            return add
        if char == '*':
            return mul
        raise Exception('Unknown operator: ' + line[pos])

    def parse_expr():
        nonlocal pos
        strip_spaces()
        if line[pos] == '(':
            pos += 1
            result = sub_parse()
            pos += 1  # the closing bracket
            return result

        chrs = []
        while pos < len(line) and line[pos] != ')' and line[pos] != ' ':
            chrs.append(line[pos])
            pos += 1

        return AtomicExpression(int(''.join(chrs)))

    def sub_parse() -> Expression:
        expect_expr = True
        exprs = []
        operators = []

        while pos < len(line) and line[pos] != ')':
            if expect_expr:
                exprs.append(parse_expr())
                expect_expr = False
            else:
                operators.append(parse_operator())
                expect_expr = True
            strip_spaces()

        if len(exprs) > 1:
            return CompositeExpression(exprs, operators)
        else:
            return exprs[0]

    return sub_parse()


if __name__ == '__main__':
    inputs = open('input_day18.txt', 'r')
    lines = inputs.readlines()
    inputs.close()

    expressions = list(map(parse_expression, filter(lambda line: len(line) > 0, lines)))

    result = 0
    for expr in expressions:
        result += expr.evaluate()

    print('Part 1: {}'.format(result))

    result = 0
    for expr in expressions:
        result += expr.evaluate2()

    print('Part 2: {}'.format(result))

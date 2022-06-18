from functools import reduce
from typing import Any
from tqdm import tqdm

eqn_string: str = "(((((1 + 2) * 3) + 4) * 5) + 6)"


def expr_to_text(e: "list[str]"):
    return " ".join(e)

def eqn_to_list(e: str) -> "list[str]":
    return list(filter(lambda x: x != " ", e))

def evaluate(threesymbols: "list[str]"):
    assert len(threesymbols) == 3
    a, b, c = threesymbols
    return str(eval(f"{a} {b} {c}"))


def join(xs: "list[str]", i: int) -> "list[str]":
    return xs[: i - 1] + [evaluate(xs[i - 1: i + 2])] + xs[i + 2:]

def add_pass(xs: "list[str]") -> "list[str]":
    for i in range(1, len(xs)-1):
        if xs[i] == '+':
            return join(xs, i)
    return xs

def mul_pass(xs: "list[str]") -> "list[str]":
    for i in range(1, len(xs)-1):
        if xs[i] == '*':
            return join(xs, i)
    return xs


def generic_pass(xs: "list[str]") -> "list[str]":
    for i in range(1, len(xs)-1):
        if xs[i] in '*+':
            return join(xs, i)
    return xs

def eval_pass_2(xs: "list[str]") -> "list[str]":
    while True:
        before = [x for x in xs]
        xs = add_pass(xs)
        if xs == before: break
    while True:
        before = [x for x in xs]
        xs = mul_pass(xs)
        if xs == before: break
    return xs


def eval_pass_3(xs: "list[str]") -> "list[str]":
    while True:
        before = [x for x in xs]
        xs = mul_pass(xs)
        if xs == before:
            break
    while True:
        before = [x for x in xs]
        xs = add_pass(xs)
        if xs == before:
            break
    return xs

def eval_pass_1(xs: "list[str]") -> "list[str]":
    while True:
        before = [x for x in xs]
        xs = generic_pass(xs)
        if xs == before:
            break
    return xs


def top_level_brackets(xs: "list[str]") -> "tuple[list[int], list[int], list[list[str]]]":
    acc = 0
    depths = [0]
    for v in xs:
        if v == '(': acc += 1
        depths.append(acc)
        if v == ')': acc -= 1
    depths.append(0)
    starts = [i 
            for i, (a, b) in enumerate(zip(depths, depths[1:])) 
            if a == 0 and b == 1]
    stops = [i - 1
            for i, (a, b) in enumerate(zip(depths, depths[1:]))
            if a == 1 and b == 0]
    
    subexprs = [xs[a+1:b] for a, b in zip(starts, stops)]

    # print(starts, stops)
    assert len(starts) == len(stops)
    assert len(starts) == len(subexprs)

    # print(f"We were given this global expression:   {expr_to_text(xs)}")
    # print(f"We found these bracket depths:        {expr_to_text(list(map(str, depths)))}")
    # print(f"Start top-level brackets:               {starts}")
    # print(f"Stop top-level brackets:                {stops}")
    # print(f"Final subexprs found:                   {list(map(expr_to_text, subexprs))}")

    return starts, stops, subexprs

def replace_range(xs: "list[Any]", begin: int, end: int, sub: "list[Any]"):
    # print(f"given this expression: {expr_to_text(xs)}")
    # print(f"we try to substitute: {expr_to_text(sub)} between positions {begin} and {end}")
    out = xs[:begin] + sub + xs[end+1:]
    # print(f"we get: {expr_to_text(out)}")
    return out


def solve(xs: "list[str]", order: int = 1, debug: bool = False) -> "list[str]":
    partial_solve = lambda x: solve(x, order=order, debug=debug)
    if debug: print(f"{' '.join(xs)}")
    if '(' not in xs:
        if order == 1: return eval_pass_1(xs)
        elif order == 2: return eval_pass_2(xs)
        else: return eval_pass_3(xs)
    else:
        starts, ends, subexprs = top_level_brackets(xs)
        # print(subexprs)
        solved_subexprs = map(partial_solve, subexprs)
        original_length = len(xs)
        for s, e, sol in zip(starts, ends, solved_subexprs):
            # print(xs)
            scale = original_length - len(xs)
            xs = replace_range(xs, s - scale, e - scale, sol)
            # print(xs)
        return partial_solve(xs)

def strip_newline(s: str) -> str:
    if s[-1] == '\n': return s[:-1]
    else: return s

def pipeline(s: str, order: int = 1, debug: bool = False) -> int:
    s = strip_newline(s)
    xs = eqn_to_list(s)
    str_sol = solve(xs, order=order, debug=debug)
    assert len(str_sol) == 1
    return int(str_sol[0])


def main(order: int = 1):
    with open("input18.txt", 'r') as f:
        results = [
            pipeline(row, order) 
            for row in f
        ]
    
    add = lambda x, y: x + y
    print(reduce(add, results))


# print(pipeline(eqn_string))

NO_PRIORITY, REVERSE_ORDER, STANDARD_ORDER = range(1, 4)

# main(part = 1)
# main(part = 2)

prompt = '\n>>> '

while(True):
    print(f"--> {pipeline(input(prompt), order=STANDARD_ORDER, debug=True)}")

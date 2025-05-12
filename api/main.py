import numpy as np
from typing import Union, List, Tuple
from collections import deque

# Create your models here.

# We assume "X" always starts
# States are 9-length string with characters " ", "X", or "O"
# 

START_STATE = " " * 9

N_POSITIONS = len(START_STATE)

WIN_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8), # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8), # columns
    (0, 4, 8), (2, 4, 6)             # diagonals
]

WIN_MOVES = [
    [tuple(j for j in comb if j != i) for comb in WIN_COMBINATIONS if i in comb]
    for i in range(N_POSITIONS)
]

def apply_one(xs, t):
    if isinstance(xs, str):
        return "".join(xs[i] for i in t)
    if isinstance(xs, list):
        return list(xs[i] for i in t)
    if isinstance(xs, tuple):
        return tuple(xs[i] for i in t)
    if isinstance(xs, int):
        return next(i for i in t if i == xs)
    TypeError(f"Unsupported type: {type(xs).__name__}")

def apply(xs, *ts):
    for t in ts:
        xs = apply_one(xs, t)
    return xs

IDENT = ( 0, 1, 2, 3, 4, 5, 6, 7, 8 )
REFL_HORZ = ( 2, 1, 0, 5, 4, 3, 8, 7, 6 )
TRANSPOSE = ( 0, 3, 6, 1, 4, 7, 2, 5, 8 )
REFL_VERT = apply(TRANSPOSE, REFL_HORZ, TRANSPOSE)
ROT_90 = apply(TRANSPOSE, REFL_HORZ)
ROT_180 = apply(ROT_90, ROT_90)
ROT_270 = apply(ROT_180, ROT_90)
TRANSFORMATIONS = (IDENT, REFL_HORZ, TRANSPOSE, REFL_VERT, ROT_90, ROT_180, ROT_270)
INVERT = {IDENT: IDENT, REFL_HORZ: REFL_HORZ, TRANSPOSE: TRANSPOSE, REFL_VERT: REFL_VERT, ROT_90: ROT_270, ROT_180: ROT_180, ROT_270: ROT_90}

def equiv(xs):
    return frozenset(apply(xs, t) for t in TRANSFORMATIONS)

def possible_moves(state: str):
    for i, p in enumerate(state):
        if p == " ":
            yield i

def get_turn(state: str):
    cntX = state.count("X")
    cntO = state.count("O")
    if cntX == cntO:
        return "X"
    if cntX == cntO + 1:
        return "O"
    raise ValueError("Illegal state.")

def move(state: str, i: int):
    if state[i] != " ":
        raise ValueError("Invalid move.")
    return state[:i] + get_turn(state) + state[i+1:]

def is_draw(state: str):
    if " " not in state:
        return True
    return False

def get_winner(state: str):
    for a, b, c in WIN_COMBINATIONS:
        if state[a] != " " and state[a] == state[b] == state[c]:
            return state[a]
    return None

def get_result(state: str):
    if is_draw(state):
        return "Draw"
    return get_winner(state)

def get_score(result: str, player: str):
    if result == player:
        return 1
    if result == "Draw":
        return 0
    if result == opp(player):
        return -1
    raise ValueError(f"result cannot be {result}")

def all_states(state: str, visited: set = None):
    if visited is None:
        visited = set()
    q = deque()
    q.append(state)
    while len(q) > 0:
        state = q.popleft()
        equiv_s = equiv(state)
        if equiv_s in visited:
            continue
        visited.add(equiv_s)
        for i in possible_moves(state):
            q.append(move(state, i))
    return visited

def opp(player):
    if player == "X":
        return "O"
    elif player == "O":
        return "X"
    raise ValueError("Invalid player. Must be 'X' or 'O'.")

def safe_next(iter):
    for v in iter:
        return v
    return None

def winning_move(s: str, p: str):
    return safe_next(winning_moves(s, p))

def winning_moves(s: str, p: str):
    for i in possible_moves(s):
        for j, k in WIN_MOVES[i]:
            if s[j] == s[k] == p:
                yield i

def smart_move(s: str) -> int:
    p = get_turn(s)
    move = winning_move(s, p)
    if move:
        return move
    move = winning_move(s, opp(p))
    if move:
        return move
    return safe_next(possible_moves(s))

def neat(s: str) -> str:
        ps = [p if p != " " else i for i, p in enumerate(s) ] 
        return f"""
{ps[0]} | {ps[1]} | {ps[2]}
---------
{ps[3]} | {ps[4]} | {ps[5]}
---------
{ps[6]} | {ps[7]} | {ps[8]}

Turn: {get_turn(s)}
Result: {get_result(s)}
"""
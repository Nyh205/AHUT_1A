"""Hog 游戏。"""

from dice import six_sided, make_test_dice
from ucb import main, trace, interact

GOAL = 100  # Hog 的目标是得到 100 分。

# 第一阶段：
# 模拟器
# #


def roll_dice(num_rolls, dice=six_sided):
    """模拟恰好掷 DICE NUM_ROLLS > 0 次。
    返回各结果之和，除非有任一结果是 1。在这种情况下，返回 1。

    num_rolls：将要进行的掷骰次数。
    dice：模拟单次掷骰结果的函数。默认为六面骰。
    """
    # 这些 assert 语句确保 num_rolls 是正整数。
    assert type(num_rolls) == int, "num_rolls must be an integer."
    assert num_rolls > 0, "Must roll at least once."
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    # END PROBLEM 1


def boar_brawl(player_score, opponent_score):
    """返回当前玩家根据 Boar Brawl 掷 0 个骰子时得到的分数。

    player_score：当前玩家的总分。
    opponent_score：另一名玩家的总分。

    """
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    # END PROBLEM 2


def take_turn(num_rolls, player_score, opponent_score, dice=six_sided):
    """返回当前玩家有 PLAYER_SCORE 分且对手有 OPPONENT_SCORE
    分时，一回合掷 NUM_ROLLS 个骰子所得的分数。

    num_rolls：将要进行的掷骰次数。
    player_score：当前玩家的总分。
    opponent_score：另一名玩家的总分。
    dice：模拟单次掷骰结果的函数。
    """
    # 将这些 assert 语句保留在此处；它们有助于检查错误。
    assert type(num_rolls) == int, "num_rolls must be an integer."
    assert num_rolls >= 0, "Cannot roll a negative number of dice in take_turn."
    assert num_rolls <= 10, "Cannot roll more than 10 dice."
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    # END PROBLEM 3


def simple_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """返回以 PLAYER_SCORE 开始回合然后掷 NUM_ROLLS
    个 DICE 的玩家的总分，忽略 Sus Fuss。
    """
    score = player_score + take_turn(num_rolls, player_score, opponent_score, dice)
    return score


def is_prime(n):
    """返回 N 是否为质数。"""
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True


def num_factors(n):
    """返回 N 的因数个数，包括 1 和 N 本身。"""
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    # END PROBLEM 4


def sus_points(score):
    """返回考虑 Sus Fuss 规则后玩家的新分数。"""
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    # END PROBLEM 4


def sus_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """返回以 PLAYER_SCORE 开始回合然后掷 NUM_ROLLS
    个 DICE 的玩家的总分，*包括* Sus Fuss。
    """
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    # END PROBLEM 4


def always_roll_5(score, opponent_score):
    """一种总是掷 5 个骰子的策略，
    无论玩家的分数或对手的分数如何。
    """
    return 5


def play(strategy0, strategy1, update, score0=0, score1=0, dice=six_sided, goal=GOAL):
    """模拟一局游戏并返回两名玩家的最终分数，Player
    0 的分数在前，Player 1 的分数在后。

    例如，play(always_roll_5, always_roll_5,
    sus_update) 模拟一局游戏，其中两名玩家在每一回合都总是选择掷
    5 个骰子，并且 Sus Fuss 规则生效。

    策略函数，例如 always_roll_5，
    接受当前玩家的分数和对手的分数，
    并返回当前玩家选择掷的骰子数量。

    更新函数，例如 sus_update 或
    simple_update，接受要掷的骰子数量、
    当前玩家的分数、对手的分数以及用于模拟掷骰的
    dice 函数。它返回当前玩家在结束回合后的更新分数。

    strategy0：player0 的策略。
    strategy1：player1 的策略。
    update：更新函数（两名玩家共用）。
    score0：Player 0 的起始分数
    score1：Player 1 的起始分数
    dice：不接受参数、模拟掷骰的函数。goal：
    达到该分数时游戏结束并产生获胜者。
    """
    who = 0  # 谁将要进行回合，0（先手）或 1（后手）
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    # END PROBLEM 5
    return score0, score1


# 第二阶段：
# 策略
# #


def always_roll(n):
    """返回一个总是掷 N 个骰子的玩家策略。

    玩家策略是一个接受两个总分作为参数（当
    前玩家的分数和对手的分数）的函数，
    并返回当前玩家本回合将要掷的骰子数量。

    >>> strategy = always_roll(3)
    >>> strategy(0, 0)
    3
    >>> strategy(99, 99)
    3
    """
    assert n >= 0 and n <= 10

    # BEGIN PROBLEM 6
    "*** YOUR CODE HERE ***"
    # END PROBLEM 6


def catch_up(score, opponent_score):
    """一种玩家策略，总是掷 5 个骰子，
    除非对手的分数更高，此时掷 6 个骰子。

    >>> catch_up(9, 4)
    5
    >>> strategy(17, 18)
    6
    """
    if score < opponent_score:
        return 6  # 多掷一个以追赶
    else:
        return 5


def is_always_roll(strategy, goal=GOAL):
    """返回在游戏达到 GOAL 分的情况下，对于分数和
    opponent_score 的每一种可能组合，
    STRATEGY 是否总是选择相同的骰子数量。

    >>> is_always_roll(always_roll_5)
    True
    >>> is_always_roll(always_roll(3))
    True
    >>> is_always_roll(catch_up)
    False
    """
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    # END PROBLEM 7


def make_averaged(original_function, times_called=1000):
    """返回一个函数，该函数返回 ORIGINAL_FUNCTION
    被调用 TIMES_CALLED 次后的平均值。

    要实现这个函数，你必须使用 *args 语法。

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 40)
    >>> averaged_dice(1, dice)  # The avg of 10 4's, 10 2's, 10 5's, and 10 1's
    3.0
    """

    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, times_called=1000):
    """返回给出一个回合最大平均分数的骰子数量（1
    到 10）。假设骰子总是返回正的结果。

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """如果 strategy0 战胜 strategy1 则返回 0，否则返回 1。"""
    score0, score1 = play(strategy0, strategy1, sus_update)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """返回 STRATEGY 对 BASELINE 的平均胜率。对以
    player 0 和 player 1 身份开始游戏时的胜率取平均。
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """运行一系列策略实验并报告结果。"""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print("Max scoring num rolls for six-sided dice:", six_sided_max)

    print("always_roll(6) win rate:", average_win_rate(always_roll(6)))  # 接近 0.5
    print("catch_up win rate:", average_win_rate(catch_up))
    print("always_roll(3) win rate:", average_win_rate(always_roll(3)))
    print("always_roll(8) win rate:", average_win_rate(always_roll(8)))

    print("boar_strategy win rate:", average_win_rate(boar_strategy))
    print("sus_strategy win rate:", average_win_rate(sus_strategy))
    print("final_strategy win rate:", average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"




def boar_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """如果 Boar Brawl 给出至少 THRESHOLD 分，该策略返回
    0 个骰子，否则返回 NUM_ROLLS。忽略 Sus Fuss 规则。
    """
    # BEGIN PROBLEM 10
    return num_rolls  # 实现后删除这一行。
    # END PROBLEM 10


def sus_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """当掷 0 个骰子使分数增加至少 THRESHOLD 分时，
    该策略返回 0 个骰子，否则返回 NUM_ROLLS。
    同时考虑 Boar Brawl 和 Suss Fuss 规则。"""
    # BEGIN PROBLEM 11
    return num_rolls  # 实现后删除这一行。
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """为你的最终策略写一段简短描述。

    *** 在此处填写你的描述 ***
    """
    # BEGIN PROBLEM 12
    return 6  # 实现后删除这一行。
    # END PROBLEM 12


# 命令行界面
# #
# 

# 注意：本节中的函数不需要修改。
# 它使用了本课程尚未涉及的 Python 特性。


@main
def run(*args):
    """读取命令行参数并调用相应的函数。"""
    import argparse

    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument(
        "--run_experiments", "-r", action="store_true", help="Runs strategy experiments"
    )

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
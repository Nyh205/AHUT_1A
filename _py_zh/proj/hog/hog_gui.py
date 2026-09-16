"""hog GUI 的 Web 服务器。"""
import io
import os
import logging
from contextlib import redirect_stdout

from gui_files.common_server import route, start

import hog
import dice
import default_graphics

PORT = 31415
DEFAULT_SERVER = "https://hog.cs61a.org"
GUI_FOLDER = "gui_files/"
PATHS = {}


class HogLoggingException(Exception):
    pass


@route
def take_turn(prev_rolls, move_history, goal, game_rules):
    """模拟直到当前回合的整局游戏。"""
    fair_dice = dice.make_fair_dice(6)
    dice_results = []

    sus_fuss = game_rules["Sus Fuss"]

    def logged_dice():
        if len(dice_results) < len(prev_rolls):
            out = prev_rolls[len(dice_results)]
        else:
            out = fair_dice()
        dice_results.append(out)
        return out

    final_scores = None
    who = 0

    move_cnt = 0

    def strategy_for(player):
        def strategy(*scores):
            nonlocal final_scores, move_cnt, who
            final_scores = scores
            if player:
                final_scores = final_scores[::-1]
            who = player
            if move_cnt == len(move_history):
                raise HogLoggingException()
            move = move_history[move_cnt]
            move_cnt += 1
            return move

        return strategy

    game_over = False

    try:
        final_scores = trace_play(
            hog.play,
            strategy_for(0),
            strategy_for(1),
            hog.sus_update if sus_fuss else hog.simple_update,
            0,
            0,
            dice=logged_dice,
            goal=goal,
        )[:2]
    except HogLoggingException:
        pass
    else:
        game_over = True

    return {
        "rolls": dice_results,
        "finalScores": final_scores,
        "message": "",
        "gameOver": game_over,
        "who": who,
    }


@route
def strategy(name, scores):
    STRATEGIES = {
        "boar_strategy": hog.boar_strategy,
        "sus_strategy": hog.sus_strategy,
        "final_strategy": hog.final_strategy,
    }
    return STRATEGIES[name](*scores[::-1])


@route("dice_graphic.svg")
def draw_dice_graphic(num):
    num = int(num[0])
    # 绘制学生提供的骰子或我们的默认骰子
    if hasattr(hog, "draw_dice"):
        graphic = hog.draw_dice(num)
        return str(graphic)
    return default_graphics.dice[num]


def trace_play(play, strategy0, strategy1, update, score0, score1, dice, goal):
    """包装用户的 play 函数，并 (1) 确保 strategy0
    和 strategy1 每回合恰好被调用一次 (2) 记录整局游戏，
    将结果作为字典列表返回，每个字典包含键 "s0_start"、
    "s1_start"、"who"、"num_dice"、
    "dice_values"。返回 (s0, s1, trace)
    ，其中 s0、s1 是 play 的返回值，trace
    是上述指定的追踪记录。这可能看起来有点过于复杂，但它也将用于为
    fuzz 测试创建游戏追踪（在针对 staff 解答运行时）。
    """
    game_trace = []

    def mod_strategy(who, my_score, opponent_score):
        if game_trace:
            prev_total_score = game_trace[-1]["s0_start"] + game_trace[-1]["s1_start"]
            if prev_total_score == my_score + opponent_score:
                # 游戏在上一回合仍在进行，
                # 因为总分每回合都会增加
                return game_trace[-1]["num_dice"]
        current_num_dice = (strategy0, strategy1)[who](my_score, opponent_score)
        current_turn = {
            "s0_start": [my_score, opponent_score][who],
            "s1_start": [my_score, opponent_score][1 - who],
            "who": who,
            "num_dice": current_num_dice,
            "dice_values": [],  # 还没有掷任何骰子
        }
        game_trace.append(current_turn)
        return current_num_dice

    def mod_dice():
        roll = dice()
        if not game_trace:
            raise RuntimeError("roll_dice called before either strategy function")
        game_trace[-1]["dice_values"].append(roll)
        return roll

    s0, s1 = play(
        lambda a, b: mod_strategy(0, a, b),
        lambda a, b: mod_strategy(1, a, b),
        update,
        score0,
        score1,
        dice=mod_dice,
        goal=goal,
    )
    return s0, s1, game_trace


if __name__ == "__main__" or "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
    app = start(PORT, DEFAULT_SERVER, GUI_FOLDER)
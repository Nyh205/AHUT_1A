import ants
import argparse
from ants import AssaultPlan


def make_test_assault_plan(ants_impl=None):
    ants_impl = ants_impl or ants
    return AssaultPlan().add_wave(ants_impl.Bee, 3, 2, 1).add_wave(ants_impl.Bee, 3, 3, 1)


def make_easy_assault_plan(ants_impl=None):
    ants_impl = ants_impl or ants_impl
    plan = AssaultPlan()
    for time in range(3, 16, 2):
        plan.add_wave(ants_impl.Bee, 3, time, 1) # 在时间戳 TIME 添加 1 只 health 为 3 的蜜蜂
    plan.add_wave(ants_impl.Wasp, 3, 4, 1) # 在时间戳 4 分配 1 只 health 为 3 的黄蜂
    plan.add_wave(ants_impl.Wasp, 3, 8, 1)
    plan.add_wave(ants_impl.Wasp, 3, 12, 1)
    plan.add_wave(ants_impl.Boss, 15, 16, 1)
    return plan


def make_normal_assault_plan(ants_impl=None):
    ants_impl = ants_impl or ants
    plan = AssaultPlan()

    for time in range(3, 16, 2): # 在时间戳 3, 5, 7, 9, 11, 13, 15 添加 2 只 health 为 3 的蜜蜂（时间 = 3, 5 时为 1 只蜜蜂）
        if time == 3 or time == 5:
            # 把蜜蜂的数量改为 1
            plan.add_wave(ants_impl.Bee, 3, time, 1)
        else:
            plan.add_wave(ants_impl.Bee, 3, time, 2)

    for time in range(6, 13, 3): # 在时间 6, 9, 12 添加 1 只 health 为 2 的 Wasp
        plan.add_wave(ants_impl.Wasp, 2, time, 1)

    for time in range(7, 11, 3): # 在时间 7, 10 添加 1 只 health 为 1 的 Ninja
        plan.add_wave(ants_impl.Wasp, 1, time, 1)

    for time in range(12, 15, 2): # 在时间 12, 14 添加 1 只 Wasp（health 3）和 1 只 Ninja（health 2）
        plan.add_wave(ants_impl.Wasp, 3, time, 1)
        plan.add_wave(ants_impl.Wasp, 2, time, 1)

    for time in range(13, 19, 2): # 在时间 13, 15, 17 添加 2 只 Wasp（health 3）+ 2 只 Ninja（health 3）
        plan.add_wave(ants_impl.Wasp, 3, time, 2)
        plan.add_wave(ants_impl.Wasp, 3, time, 2)

    for time in range(16, 23, 2): # 在时间戳 16, 18, 20, 22 添加 2 只 health 为 5 的蜜蜂
        plan.add_wave(ants_impl.Bee, 5, time, 2)

    for time in range(24, 31, 2): # 在时间戳 24, 26, 28, 30 添加 2 只 health 为 6 的蜜蜂
        plan.add_wave(ants_impl.Bee, 6, time, 2)

    for time in range(20, 30, 3): # 在时间 20, 23, 26, 29 添加 2 只 health 为 3 的 Ninja
        plan.add_wave(ants_impl.Wasp, 3, time, 2)

    for time in range(21, 26, 2): # 在时间 21, 23, 25 添加 1 只 health 为 5 的 Wasp
        plan.add_wave(ants_impl.Wasp, 5, time, 1)

    for time in range(28, 31): # 在时间 28, 29, 30 添加 2 只 health 为 6 的 Wasp
        plan.add_wave(ants_impl.Wasp, 6, time, 2)

    plan.add_wave(ants_impl.Boss, 50, 30, 1)

    return plan


def make_hard_assault_plan(ants_impl=None):
    ants_impl = ants_impl or ants
    plan = AssaultPlan()

    for time in range(3, 9, 2): # 在时间戳 3, 5, 7 添加 2 只 health 为 3 的蜜蜂（时间 = 3 时为 1 只蜜蜂）
        if time == 3:
            # 把蜜蜂的数量改为 1
            plan.add_wave(ants_impl.Bee, 3, time, 1)
        else:
            plan.add_wave(ants_impl.Bee, 3, time, 2)

    for time in range(9, 16, 2): # 在时间戳 9, 11, 13, 15 添加 3 只 health 为 3 的蜜蜂
        plan.add_wave(ants_impl.Bee, 3, time, 3)

    for time in range(5, 9, 3): # 在时间 5, 8 添加 1 只 health 为 2 的 Wasp
        plan.add_wave(ants_impl.Wasp, 2, time, 1)

    for time in range(7, 12, 2): # 在时间 7, 9 添加 3 只 health 为 1 的 Ninja
        plan.add_wave(ants_impl.Wasp, 1, time, 3)

    for time in range(10, 15, 2): # 在时间 10, 12, 14 添加 2 只 Wasp（health 3）和 1 只 Ninja（health 3）
        plan.add_wave(ants_impl.Wasp, 3, time, 2)
        plan.add_wave(ants_impl.Wasp, 3, time, 1)

    for time in range(13, 19, 2): # 在时间 13, 15, 17 添加 3 只 Wasp（health 3）+ 3 只 Ninja（health 3）
        plan.add_wave(ants_impl.Wasp, 3, time, 3)
        plan.add_wave(ants_impl.Wasp, 3, time, 3)

    for time in range(16, 23, 2): # 在时间戳 16, 18, 20, 22 添加 3 只 health 为 5 的蜜蜂
        plan.add_wave(ants_impl.Bee, 5, time, 3)

    for time in range(24, 31, 2): # 在时间戳 24, 26, 28, 30 添加 3 只 health 为 6 的蜜蜂
        plan.add_wave(ants_impl.Bee, 6, time, 3)

    for time in range(20, 30, 2): # 在时间 20, 22, 24, 26, 28 添加 2 只 health 为 3 的 Ninja
        plan.add_wave(ants_impl.Wasp, 3, time, 2)

    for time in range(21, 26, 2): # 在时间 21, 23, 25 添加 2 只 health 为 6 的 Wasp
        plan.add_wave(ants_impl.Wasp, 6, time, 2)

    for time in range(28, 31): # 在时间 28, 29, 30 添加 4 只 health 为 8 的 Wasp
        plan.add_wave(ants_impl.Wasp, 8, time, 4)

    plan.add_wave(ants_impl.Boss, 65, 30, 1)

    return plan


def make_extra_hard_assault_plan(ants_impl=None):
    ants_impl = ants_impl or ants
    plan = AssaultPlan()

    for time in range(3, 9, 2): # 在时间戳 3, 5, 7 添加 2 只 health 为 3 的蜜蜂
        plan.add_wave(ants_impl.Bee, 3, time, 2)

    for time in range(9, 16, 2): # 在时间戳 9, 11, 13, 15 添加 3 只 health 为 3 的蜜蜂
        plan.add_wave(ants_impl.Bee, 3, time, 3)

    for time in range(5, 12, 2): # 在时间 5, 7, 9, 11 添加 1 只 health 为 2 的 Wasp
        plan.add_wave(ants_impl.Wasp, 2, time, 1)

    for time in range(7, 12, 2): # 在时间 7, 9, 11 添加 3 只 health 为 2 的 Ninja
        plan.add_wave(ants_impl.Wasp, 2, time, 3)

    for time in range(10, 15, 2): # 在时间 10, 12, 14 添加 2 只 Wasp（health 3）和 2 只 Ninja（health 3）
        plan.add_wave(ants_impl.Wasp, 3, time, 2)
        plan.add_wave(ants_impl.Wasp, 3, time, 2)

    for time in range(13, 19, 2): # 在时间 13, 15, 17 添加 3 只 Wasp（health 4）+ 3 只 Ninja（health 3）
        plan.add_wave(ants_impl.Wasp, 4, time, 3)
        plan.add_wave(ants_impl.Wasp, 3, time, 3)

    plan.add_wave(ants_impl.Boss, 10, 15, 1)

    for time in range(16, 25, 2): # 在时间戳 16, 18, 20, 22, 24 添加 3 只 health 为 6 的蜜蜂
        plan.add_wave(ants_impl.Bee, 6, time, 3)

    for time in range(26, 31, 2): # 在时间戳 26, 28, 30 添加 4 只 health 为 6 的蜜蜂
        plan.add_wave(ants_impl.Bee, 6, time, 4)

    for time in range(20, 30, 2): # 在时间 20, 22, 24, 26, 28 添加 2 只 health 为 3 的 Ninja
        plan.add_wave(ants_impl.Wasp, 3, time, 2)

    for time in range(21, 26, 2): # 在时间 21, 23, 25 添加 2 只 health 为 8 的 Wasp
        plan.add_wave(ants_impl.Wasp, 8, time, 2)

    for time in range(28, 31): # 在时间 28, 29, 30 添加 4 只 health 为 10 的 Wasp
        plan.add_wave(ants_impl.Wasp, 10, time, 4)

    plan.add_wave(ants_impl.Boss, 75, 30, 1)

    return plan


def create_game_state():
    """读取命令行参数并返回带有这些选项的游戏状态。"""

    parser = argparse.ArgumentParser(description="Play Ants vs. SomeBees")

    parser.add_argument('-d', type=str, metavar='DIFFICULTY', help='sets difficulty of game (test/easy/normal/hard/extra-hard)')
    parser.add_argument('-w', '--water', action='store_true', help='loads a full layout with water')
    parser.add_argument('--food', type=int, help='number of food to start with when testing', default=2)
    args = parser.parse_args()

    if args.d in ['t', 'test']:
        assault_plan = make_test_assault_plan(ants)
        num_tunnels = 1
    elif args.d in ['e', 'easy']:
        assault_plan = make_easy_assault_plan(ants)
        num_tunnels = 2
    elif args.d in ['h', 'hard']:
        assault_plan = make_hard_assault_plan(ants)
        num_tunnels = 4
    elif args.d in ['i', 'extra-hard']:
        assault_plan = make_extra_hard_assault_plan(ants)
        num_tunnels = 4
    else:
        assault_plan = make_normal_assault_plan(ants)
        num_tunnels = 4

    beehive = ants.Hive(assault_plan)
    layout = ants.wet_layout if args.water else ants.dry_layout
    food = args.food
    tunnel_length = 10
    dimensions = (num_tunnels, tunnel_length)

    return ants.GameState(beehive, ants.ant_types(), layout, dimensions, food)
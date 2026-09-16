"""蚂蚁大战蜜蜂。"""

from __future__ import annotations  # 这让类型注解能够正常工作
import random
from ucb import main, interact, trace
from collections import OrderedDict

# 核心类
# #
# 


class Place:
    """Place 存放昆虫，并有一个通往另一个 Place 的出口。"""
    is_hive = False

    def __init__(self, name: str, exit: Place | None = None):
        """用给定的 NAME 和 EXIT 创建一个 Place。

        name -- 一个字符串；这个 Place 的名称。exit --
        离开这个 Place 所到达的 Place（可能为 None）。
        """
        self.name = name
        self.exit = exit
        self.bees: list[Bee] = []
        self.ant: Ant | None = None
        self.entrance: Place | None = None
        # 阶段 1：给出口添加入口
        # BEGIN Problem 2
        "*** YOUR CODE HERE ***"
        # END Problem 2

    def add_insect(self, insect: Insect):
        """要求昆虫将自身加入这个 place。
        这个方法的存在是为了能够在子类中被重写。
        """
        insect.add_to(self)

    def remove_insect(self, insect: Insect):
        """要求昆虫将自身从这个 place 中移除。
        这个方法的存在是为了能够在子类中被重写。
        """
        insect.remove_from(self)

    def __str__(self) -> str:
        return self.name


class Insect:
    """Insect 是 Ant 和 Bee 的基类，拥有 health 和一个 Place。"""

    next_id = 0  # 每只昆虫获得一个唯一的 id 编号
    damage = 0
    # 在这里添加类属性

    def __init__(self, health: int, place: Place | None = None):
        """用 health 和一个起始 PLACE 创建一个 Insect。"""
        self.health = health
        self.full_health = health
        self.place = place

        # 给每只昆虫分配一个唯一的 ID
        self.id = Insect.next_id
        Insect.next_id += 1

    def reduce_health(self, damage_taken: float):
        """将 health 减少 DAMAGE_TAKEN，如果昆虫没有剩余 health，
        则将其从其 place 中移除。在 gui.py 中被装饰以支持 GUI。

        >>> test_insect = Insect(5)
        >>> test_insect.reduce_health(2)
        >>> test_insect.health
        3
        """
        self.health -= damage_taken
        if self.health <= 0:
            self.zero_health_callback()

            if self.place is not None:
                self.place.remove_insect(self)

    def action(self, gamestate: GameState):
        """每回合执行的动作。"""

    def zero_health_callback(self):
        """
        当 health 降到 0 或以下时被调用。
        在 gui.py 中被装饰以支持 GUI
        """

    def add_to(self, place: Place):
        self.place = place

    def remove_from(self, place: Place):
        self.place = None

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.health, self.place)


class Ant(Insect):
    """Ant 占据一个 place 并为蚁群工作。"""

    implemented = False  # 只应实例化已实现的 Ant 类
    food_cost = 0
    is_container = False
    # 在这里添加类属性

    def __init__(self, health: int = 1):
        super().__init__(health)

    def can_contain(self, other: Ant) -> bool:
        return False

    def store_ant(self, ant: Ant):
        assert False, "{0} cannot contain an ant".format(self)

    def remove_ant(self, ant: Ant):
        assert False, "{0} cannot contain an ant".format(self)

    def add_to(self, place: Place):
        if place.ant is None:
            place.ant = self
        else:
            # BEGIN Problem 8b
            assert place.ant is None, 'Too many ants in {0}'.format(place)
            # END Problem 8b
        Insect.add_to(self, place)

    def remove_from(self, place: Place):
        if place.ant is self:
            place.ant = None
        elif place.ant is None:
            assert False, '{0} is not in {1}'.format(self, place)
        else:
            place.ant.remove_ant(self)
        Insect.remove_from(self, place)

    def double(self):
        """如果这只蚂蚁的 damage 尚未翻倍，则将其翻倍。"""
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        # END Problem 12


class HarvesterAnt(Ant):
    """HarvesterAnt 每回合为蚁群额外生产 1 个 food。"""

    name = 'Harvester'
    implemented = True
    # 在这里重写类属性

    def action(self, gamestate: GameState):
        """为蚁群额外生产 1 个 food。

        gamestate -- GameState，用于访问游戏状态信息。
        """
        # BEGIN Problem 1
        "*** YOUR CODE HERE ***"
        # END Problem 1


class ThrowerAnt(Ant):
    """ThrowerAnt 每回合向范围内最近的 Bee 投掷一片叶子。"""

    name = 'Thrower'
    implemented = True
    damage = 1
    # 在这里添加/重写类属性

    def nearest_bee(self) -> Bee | None:
        """返回一只随机的 Bee，来自最近的包含 Bees
        且可以从 ThrowerAnt 的 Place
        出发沿入口到达的 Place（不包括 Hive）。
        如果没有这样的 Bee（或范围内没有），此方法返回 None。
        """
        if not self.place:
            return None  # 不在 Place 中的 Ant 没有最近的 Bee
        # BEGIN Problem 3 and 4
        return random_bee(self.place.bees) # 替换这一行
        # END Problem 3 and 4

    def throw_at(self, target: Bee | None):
        """向目标 Bee 投掷一片叶子，减少其 health。"""
        if target is not None:
            target.reduce_health(self.damage)

    def action(self, gamestate: GameState):
        """向范围内最近的 Bee 投掷一片叶子。"""
        self.throw_at(self.nearest_bee())


def random_bee(bees: list[Bee]) -> Bee | None:
    """从 bees 列表中返回一只随机的 bee，如果 bees 为空则返回 None。"""
    assert isinstance(bees, list), \
        "random_bee's argument should be a list but was a %s" % type(bees).__name__
    if bees:
        return random.choice(bees)

# 扩展
# #
# 


class ShortThrower(ThrowerAnt):
    """一种 ThrowerAnt，只向至多 3 个 place 之外的 Bees 投掷叶子。"""

    name = 'Short'
    food_cost = 2
    # 在这里重写类属性
    # BEGIN Problem 4
    implemented = False   # 改为 True 即可在 GUI 中查看
    # END Problem 4


class LongThrower(ThrowerAnt):
    """一种 ThrowerAnt，只向至少 5 个 place 之外的 Bees 投掷叶子。"""

    name = 'Long'
    food_cost = 2
    # 在这里重写类属性
    # BEGIN Problem 4
    implemented = False   # 改为 True 即可在 GUI 中查看
    # END Problem 4


class FireAnt(Ant):
    """FireAnt 在消亡时会烤熟其 Place 中的任何 Bee。"""

    name = 'Fire'
    damage = 3
    food_cost = 5
    # 在这里重写类属性
    # BEGIN Problem 5
    implemented = False   # 改为 True 即可在 GUI 中查看
    # END Problem 5

    def __init__(self, health: int = 3):
        """用 HEALTH 数量创建一个 Ant。"""
        super().__init__(health)

    def reduce_health(self, damage_taken: float):
        """将 health 减少 DAMAGE_TAKEN，如果 FireAnt
        没有剩余 health，则将其从其 place 中移除。

        确保减少当前 place 中每只 bee 的 health，
        并在 fire ant 死亡时施加额外的伤害。
        """
        # BEGIN Problem 5
        "*** YOUR CODE HERE ***"
        # END Problem 5

# BEGIN Problem 6
# WallAnt 类
# END Problem 6

# BEGIN Problem 7
# HungryAnt 类
# END Problem 7


class ContainerAnt(Ant):
    """
    ContainerAnt 可以通过容纳其他蚂蚁来与它们共享一个空间。
    """
    is_container = True

    def __init__(self, health: int):
        super().__init__(health)
        self.ant_contained = None

    def can_contain(self, other: Ant) -> bool:
        # BEGIN Problem 8a
        "*** YOUR CODE HERE ***"
        # END Problem 8a

    def store_ant(self, ant: Ant):
        # BEGIN Problem 8a
        "*** YOUR CODE HERE ***"
        # END Problem 8a

    def remove_ant(self, ant: Ant):
        if self.ant_contained is not ant:
            assert False, "{} does not contain {}".format(self, ant)
        self.ant_contained = None

    def remove_from(self, place: Place):
        # 对容器蚂蚁的特殊处理
        if place.ant is self:
            # 容器已被移除。被容纳的蚂蚁应保留在游戏中
            place.ant = self.ant_contained
            Insect.remove_from(self, place)
        else:
            # 默认为正常行为
            Ant.remove_from(self, place)

    def action(self, gamestate: GameState):
        # BEGIN Problem 8a
        "*** YOUR CODE HERE ***"
        # END Problem 8a


class ProtectorAnt(ContainerAnt):
    """ProtectorAnt 为其他 Ants 提供保护。"""

    name = 'Protector'
    food_cost = 4
    # 在这里重写类属性
    # BEGIN Problem 8c
    implemented = False   # 改为 True 即可在 GUI 中查看
    # END Problem 8c

# BEGIN Problem 9
# TankAnt 类
# END Problem 9


class Water(Place):
    """Water 是一个只能容纳防水昆虫的 place。"""

    def add_insect(self, insect: Insect):
        """向这个 place 添加一个 Insect。
        如果该昆虫不防水，则将其 health 减为 0。"""
        # BEGIN Problem 10
        "*** YOUR CODE HERE ***"
        # END Problem 10

# BEGIN Problem 11
# ScubaThrower 类
# END Problem 11


class QueenAnt(ThrowerAnt):
    """QueenAnt 提升其身后所有蚂蚁的 damage。"""

    name = 'Queen'
    food_cost = 7
    # 在这里重写类属性
    # BEGIN Problem 12
    implemented = False   # 改为 True 即可在 GUI 中查看
    # END Problem 12

    def action(self, gamestate: GameState):
        """蚁后投掷一片叶子，但同时将其隧道中蚂蚁的
        damage 翻倍。
        """
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        # END Problem 12

    def reduce_health(self, damage_taken: float):
        """将 health 减少 DAMAGE_TAKEN，如果
        QueenAnt 没有剩余 health，则发出游戏结束的信号。
        """
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        # END Problem 12


# 额外挑战
# #
# 

class SlowThrower(ThrowerAnt):
    """会对 Bees 造成 Slow 的 ThrowerAnt。"""

    name = 'Slow'
    food_cost = 6
    # BEGIN Problem EC 1
    implemented = False   # 改为 True 即可在 GUI 中查看
    # END Problem EC 1

    def throw_at(self, target: Bee | None):
        # BEGIN Problem EC 1
        "*** YOUR CODE HERE ***"
        # END Problem EC 1


class ScaryThrower(ThrowerAnt):
    """威慑 Bees 的 ThrowerAnt，使它们后退而不是前进。"""

    name = 'Scary'
    food_cost = 6
    # BEGIN Problem EC 2
    implemented = False   # 改为 True 即可在 GUI 中查看
    # END Problem EC 2

    def throw_at(self, target: Bee | None):
        # BEGIN Problem EC 2
        "*** YOUR CODE HERE ***"
        # END Problem EC 2


class NinjaAnt(Ant):
    """NinjaAnt 不会阻挡路径，并伤害其 place 中的所有 bees。"""

    name = 'Ninja'
    damage = 1
    food_cost = 5
    # 在这里重写类属性
    # BEGIN Problem EC 3
    implemented = False   # 改为 True 即可在 GUI 中查看
    # END Problem EC 3

    def action(self, gamestate: GameState):
        # BEGIN Problem EC 3
        "*** YOUR CODE HERE ***"
        # END Problem EC 3


class LaserAnt(ThrowerAnt):
    """伤害其路径上所有 Insects 的 ThrowerAnt。"""

    name = 'Laser'
    food_cost = 10
    # 在这里重写类属性
    # BEGIN Problem EC 4
    implemented = False   # 改为 True 即可在 GUI 中查看
    # END Problem EC 4

    def __init__(self, health: int = 1):
        super().__init__(health)
        self.insects_shot = 0

    def insects_in_front(self) -> dict[Bee, int]:
        # BEGIN Problem EC 4
        return {}
        # END Problem EC 4

    def calculate_damage(self, distance: int) -> float:
        # BEGIN Problem EC 4
        return 0
        # END Problem EC 4

    def action(self, gamestate: GameState):
        insects_and_distances = self.insects_in_front()
        LaserAnt.play_sound_effect() # 激光束音效
        for insect, distance in insects_and_distances.items():
            damage = self.calculate_damage(distance)
            insect.reduce_health(damage)
            if damage:
                self.insects_shot += 1

    @classmethod
    def play_sound_effect(cls):
        """播放激光音效。在 gui.py 中被装饰"""
        pass


# 蜜蜂
# #
# 

class Bee(Insect):
    """Bee 从一个 place 移动到另一个 place，沿着出口前进并蜇蚂蚁。"""

    name = 'Bee'
    damage = 1


    def sting(self, ant: Ant):
        """攻击一个 ANT，将其 health 减少 1。"""
        ant.reduce_health(self.damage)

    def move_to(self, place: Place):
        """从 Bee 当前的 Place 移动到新的 PLACE。"""
        if self.place is not None:
            self.place.remove_insect(self)

        if place is not None:
            place.add_insect(self)

    def blocked(self) -> bool:
        """如果这只 Bee 无法前进到下一个 Place，则返回 True。"""
        # 对 NinjaAnt 的特殊处理
        # BEGIN Problem EC 3
        return self.place is not None and self.place.ant is not None
        # END Problem EC 3

    def action(self, gamestate: GameState):
        """Bee 的动作：如果被阻挡，就蜇挡住其出口的
        Ant；否则移动到其当前 place 的出口。

        gamestate -- GameState，用于访问游戏状态信息。
        """
        destination = None
        if self.place:
            destination = self.place.exit


        if self.blocked() and self.place and self.place.ant:
            self.sting(self.place.ant)
        elif self.health > 0 and destination is not None:
            self.move_to(destination)

    def add_to(self, place: Place):
        place.bees.append(self)
        super().add_to(place)

    def remove_from(self, place: Place):
        place.bees.remove(self)
        super().remove_from(place)

    def scare(self, length: int):
        """
        如果这只 Bee 之前没有被吓到过，
        则让它尝试后退 LENGTH 次。
        """
        # BEGIN Problem EC 2
        "*** YOUR CODE HERE ***"
        # END Problem EC 2


class Wasp(Bee):
    """具有更高 damage 的 Bee 类。"""
    name = 'Wasp'
    damage = 2


class Boss(Wasp):
    """蜜蜂的首领。对 boss 的任何攻击造成的 damage 都有上限。
    """
    name = 'Boss'
    damage_cap = 8

    def reduce_health(self, damage_taken: float):
        super().reduce_health(min(damage_taken, self.damage_cap))

    @classmethod
    def play_sound_effect(cls):
        "boss 到达时播放音效！在 gui.py 中被装饰"
        pass


class Hive(Place):
    """Bees 发起攻击的 Place。

    assault_plan -- 一个 AssaultPlan；蜜蜂何时以及从何处进入蚁群。
    """
    is_hive = True

    def __init__(self, assault_plan: AssaultPlan):
        self.name = 'Hive'
        self.assault_plan = assault_plan
        self.bees: list[Bee] = []
        for bee in assault_plan.all_bees():
            self.add_insect(bee)
        # 对于 Hive，以下属性始终为 None
        self.entrance: None = None
        self.ant: None = None
        self.exit: Place | None = None

    def strategy(self, gamestate: GameState):
        exits = [p for p in gamestate.places.values() if p.entrance is self]

        for bee in self.assault_plan.get(gamestate.time, []):
            if Boss in bee.__class__.__mro__:
                Boss.play_sound_effect()
                GameState.display_notification('Boss Bee is Here!')
            bee.move_to(random.choice(exits))
            gamestate.active_bees.append(bee)

# 游戏组件
# #
# 

class GameState:
    """一个蚂蚁集体，管理全局游戏状态并模拟时间。

    属性：time -- 已流逝的时间 food
    -- 蚁群可用的 food 总量 places
    -- 蚁群中所有 place 的列表（包括一个
    Hive）bee_entrances --
    蜜蜂可以进入的 place 的列表
    """

    def __init__(self, beehive: Hive, ant_types: list, create_places, dimensions, food: int = 2):
        """创建一个 GameState 用于模拟游戏。

        参数：beehive -- 装满蜜蜂的
        Hive ant_types --
        蚂蚁类的列表 create_places
        -- 创建 place 集合的函数
        dimensions -- 包含游戏布局尺寸的一对值
        """
        self.time: int = 0
        self.food = food
        self.beehive = beehive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)
        self.dimensions = dimensions
        self.active_bees: list = []
        self.configure(beehive, create_places)

    def configure(self, beehive: Hive, create_places):
        """配置蚁群中的 place。"""
        self.base: AntHomeBase = AntHomeBase('Ant Home Base')
        self.places: OrderedDict = OrderedDict()
        self.bee_entrances: list = []

        def register_place(place: Place, is_bee_entrance: bool):
            self.places[place.name] = place
            if is_bee_entrance:
                place.entrance = beehive
                self.bee_entrances.append(place)
        register_place(self.beehive, False)
        create_places(self.base, register_place,
                      self.dimensions[0], self.dimensions[1])

    def ants_take_actions(self): # 让蚂蚁采取行动
        for ant in self.ants:
            if ant.health > 0:
                ant.action(self)

    def bees_take_actions(self, num_bees: int) -> int: # 让蜜蜂采取行动
        for bee in self.active_bees[:]:
            if bee.health > 0:
                bee.action(self)
            if bee.health <= 0:
                num_bees -= 1
                self.active_bees.remove(bee)
        if num_bees == 0: # 检查玩家是否获胜
            GameState.play_win_sound()
            raise AntsWinException()
        return num_bees

    def simulate(self):
        """模拟对蚁群的攻击。GUI 会调用它来进行游戏。"""
        num_bees = len(self.bees)
        try:
            while True:
                self.beehive.strategy(self) # 蜜蜂从蜂巢入侵
                yield None # 让出之后，玩家有时间放置蚂蚁
                self.ants_take_actions()
                self.time += 1
                yield None # 让出之后，等待抛叶子动画播放完毕，然后让蜜蜂行动
                num_bees = self.bees_take_actions(num_bees)
        except AntsWinException:
            print('All bees are vanquished. You win!')
            yield True
        except AntsLoseException:
            print('The bees reached homebase or the queen ant queen has perished. Please try again :(')
            yield False

    def deploy_ant(self, place_name: str, ant_type_name: str) -> Ant | None:
        """如果有足够的食物，就放置一只蚂蚁。

        当前策略会调用这个方法部署蚂蚁。
        """
        ant_type = self.ant_types[ant_type_name]
        if ant_type.food_cost > self.food:
            message = 'Not enough food!'
            print(message)
            GameState.display_notification(message)
        else:
            ant: Ant = ant_type()
            self.places[place_name].add_insect(ant)
            self.food -= ant.food_cost
            return ant

    def remove_ant(self, place_name: str):
        """从游戏中移除一只 Ant。"""
        place = self.places[place_name]
        if place.ant is not None:
            place.remove_insect(place.ant)

    @staticmethod
    def display_notification(message):
        """显示一条通知！在 gui.py 中被装饰以支持 GUI"""
        pass

    @classmethod
    def play_win_sound(cls):
        """蚂蚁获胜时播放音效！在 gui.py 中被装饰"""
        pass

    @property
    def ants(self):
        return [p.ant for p in self.places.values() if p.ant is not None]

    @property
    def bees(self):
        return [b for p in self.places.values() for b in p.bees]

    @property
    def insects(self):
        return self.ants + self.bees

    def __str__(self):
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
        return str([str(i) for i in self.ants + self.bees]) + status


class AntHomeBase(Place):
    """位于隧道尽头的 AntHomeBase，蚁后通常居住在那里。"""

    def add_insect(self, insect):
        """向这个 Place 添加一只 Insect。

        实际上不能向 AntHomeBase 添加 Ant。不过，
        如果 Bee 试图进入 AntHomeBase，就会引发
        AntsLoseException，标志着游戏结束。
        """
        assert isinstance(insect, Bee), 'Cannot add {0} to AntHomeBase'
        raise AntsLoseException()


def ants_win():
    """表示 Ant 获胜。"""
    raise AntsWinException()


def ants_lose():
    """表示 Ant 失败。"""
    raise AntsLoseException()


def ant_types() -> list:
    """返回所有已实现的 Ant 类的列表。"""
    all_ant_types: list = []
    new_types: list = [Ant]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_ant_types.extend(new_types)
    return [t for t in all_ant_types if t.implemented]


def bee_types() -> list:
    """返回所有已实现的 Bee 类的列表。"""
    all_bee_types: list = []
    new_types: list = [Bee]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_bee_types.extend(new_types)
    return all_bee_types


class GameOverException(Exception):
    """游戏结束的基础 Exception。"""
    pass


class AntsWinException(GameOverException):
    """表示蚂蚁获胜的 Exception。"""
    pass


class AntsLoseException(GameOverException):
    """表示蚂蚁失败的 Exception。"""
    pass


# 布局
# #
# 


def wet_layout(queen: AntHomeBase, register_place, tunnels: int = 3, length: int = 9, moat_frequency: int = 3):
    """注册湿的和干的地点的混合。"""
    for tunnel in range(tunnels):
        exit = queen
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)
            else:
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
            register_place(exit, step == length - 1)


def dry_layout(queen: AntHomeBase, register_place, tunnels: int = 3, length: int = 9):
    """注册干的隧道。"""
    wet_layout(queen, register_place, tunnels, length, 0)


# 进攻计划
# #
# 

class AssaultPlan(dict):
    """蜜蜂对蚁群的进攻计划。进攻以定时的波次到来。

    AssaultPlan 是一个从时间（int）到波次（Bee 的列表）的字典。

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """
    def add_wave(self, bee_type, bee_health: int, time: int, count: int) -> AssaultPlan:
        """在 time 时刻添加一波，包含 count 只具有指定 health 的 Bee。"""
        bees = [bee_type(bee_health) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    def all_bees(self) -> list:
        """把所有 Bee 放入蜂巢并返回 Bee 的列表。"""
        return [bee for wave in self.values() for bee in wave]
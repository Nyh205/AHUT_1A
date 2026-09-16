from __future__ import annotations


class Transaction:
    def __init__(self, id: int, before: int, after: int):
        self.id = id
        self.before = before
        self.after = after

    def changed(self) -> bool:
        """返回该交易是否导致余额发生了变化。"""
        return self.before != self.after

    def report(self) -> str:
        """返回一个描述该交易的字符串。

        >>> Transaction(3, 20, 10).report()
        '3: decreased 20->10'
        >>> Transaction(4, 20, 50).report()
        '4: increased 20->50'
        >>> Transaction(5, 50, 50).report()
        '5: no change'
        """
        msg: str = 'no change'
        if self.changed():
            if self.after < self.before:
                verb = 'decreased'
            else:
                verb = 'increased'
            msg = verb + ' ' + str(self.before) + '->' + str(self.after)
        return str(self.id) + ': ' + msg

class BankAccount:
    """一个记录其交易历史的银行账户。

    >>> a = BankAccount('Eric')
    >>> a.deposit(100)    # Transaction 0 for a
    100
    >>> b = BankAccount('Erica')
    >>> a.withdraw(30)    # Transaction 1 for a
    70
    >>> a.deposit(10)     # Transaction 2 for a
    80
    >>> b.deposit(50)     # Transaction 0 for b
    50
    >>> b.withdraw(10)    # Transaction 1 for b
    40
    >>> a.withdraw(100)   # Transaction 3 for a
    'Insufficient funds'
    >>> len(a.transactions)
    4
    >>> len([t for t in a.transactions if t.changed()])
    3
    >>> for t in a.transactions:
    ...     print(t.report())
    0: increased 0->100
    1: decreased 100->70
    2: increased 70->80
    3: no change
    >>> b.withdraw(100)   # Transaction 2 for b
    'Insufficient funds'
    >>> b.withdraw(30)    # Transaction 3 for b
    10
    >>> for t in b.transactions:
    ...     print(t.report())
    0: increased 0->50
    1: decreased 50->40
    2: no change
    3: decreased 40->10
    """

    # *** 你需要在这个类中的多个地方做出修改 ***
    def next_id(self) -> int:
        # 实现这个计数器有很多种方法，
        # 比如使用一个实例属性来跟踪下一个 ID。
        return len(self.transactions)

    def __init__(self, account_holder: str):
        self.balance: int = 0
        self.holder = account_holder
        self.transactions = []

    def deposit(self, amount: int) -> int:
        """把账户余额增加 amount，
        把这次存款加入交易历史，并返回新的余额。
        """
        self.transactions.append(Transaction(self.next_id(), self.balance, self.balance + amount))
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount: int) -> int | str:
        """把账户余额减少 amount，
        把这次取款加入交易历史，并返回新的余额。
        """
        if amount > self.balance:
            self.transactions.append(Transaction(self.next_id(), self.balance, self.balance))
            return 'Insufficient funds'
        self.transactions.append(Transaction(self.next_id(), self.balance, self.balance - amount))
        self.balance = self.balance - amount
        return self.balance


class Email:
    """一封邮件有以下实例属性：

        msg (str)：消息的内容 sender
        (Client)：发送该邮件的客户端
        recipient_name (str)：收件人（另一个客户端）的名字
    """
    def __init__(self, msg: str, sender, recipient_name: str):
        self.msg = msg
        self.sender = sender
        self.recipient_name = recipient_name

class Server:
    """每个 Server 都有一个名为 clients
    的实例属性，它是一个从客户端名字到客户端对象的字典。

    >>> s = Server()
    >>> # Dummy client class implementation for testing only
    >>> class Client:
    ...     def __init__(self, server, name):
    ...         self.inbox = []
    ...         self.server = server
    ...         self.name = name
    >>> a = Client(s, 'Alice')
    >>> b = Client(s, 'Bob')
    >>> s.register_client(a) 
    >>> s.register_client(b)
    >>> len(s.clients)  # we have registered 2 clients
    2
    >>> all([type(c) == str for c in s.clients.keys()])  # The keys in self.clients should be strings
    True
    >>> all([type(c) == Client for c in s.clients.values()])  # The values in self.clients should be Client instances
    True
    >>> new_a = Client(s, 'Alice')  # a new client with the same name as an existing client
    >>> s.register_client(new_a)
    >>> len(s.clients)  # the key of a dictionary must be unique
    2
    >>> s.clients['Alice'] is new_a  # the value for key 'Alice' should now be updated to the new client new_a
    True
    >>> e = Email("I love 61A", b, 'Alice')
    >>> s.send(e)
    >>> len(new_a.inbox)  # one email has been sent to new Alice
    1
    >>> type(new_a.inbox[0]) == Email  # a Client's inbox is a list of Email instances
    True
    """
    def __init__(self):
        self.clients = {}

    def send(self, email: Email):
        """把这封邮件追加到它所寄往的客户端的收件箱中。
        email 是 Email 类的一个实例。
        """
        self.clients[email.recipient_name].inbox.append(email)

    def register_client(self, client):
        """把一个客户端添加到 clients
        映射中（它是一个从客户端名字到客户端实例的字典）
        。client 是 Client 类的一个实例。
        """
        self.clients[client.name] = client

class Client:
    """一个客户端有一个 server、一个名字（str）和一个收件箱（列表）。

    >>> s = Server()
    >>> a = Client(s, 'Alice')
    >>> b = Client(s, 'Bob')
    >>> a.compose('Hello, World!', 'Bob')
    >>> b.inbox[0].msg
    'Hello, World!'
    >>> a.compose('CS 61A Rocks!', 'Bob')
    >>> len(b.inbox)
    2
    >>> b.inbox[1].msg
    'CS 61A Rocks!'
    >>> b.inbox[1].sender.name
    'Alice'
    """
    def __init__(self, server: Server, name: str):
        self.inbox: list = []
        self.server = server
        self.name = name
        server.register_client(self)

    def compose(self, message: str, recipient_name: str):
        """把带有给定消息的邮件发送给收件人。"""
        email = Email(message, self, recipient_name)
        self.server.send(email)


class Mint:
    """铸币厂通过在年份上压印来制造硬币。

    update 方法会把铸币厂的印记设置为 Mint.present_year。

    >>> mint = Mint()
    >>> mint.year
    2025
    >>> dime = mint.create(Dime)
    >>> dime.year
    2025
    >>> Mint.present_year = 2105  # Time passes
    >>> nickel = mint.create(Nickel)
    >>> nickel.year     # The mint has not updated its stamp yet
    2025
    >>> nickel.worth()  # 5 cents + (80 - 50 years)
    35
    >>> mint.update()   # The mint's year is updated to 2105
    >>> Mint.present_year = 2180     # More time passes
    >>> mint.create(Dime).worth()    # 10 cents + (75 - 50 years)
    35
    >>> Mint().create(Dime).worth()  # A new mint has the current year
    10
    >>> dime.worth()     # 10 cents + (155 - 50 years)
    115
    >>> Dime.cents = 20  # Upgrade all dimes!
    >>> dime.worth()     # 20 cents + (155 - 50 years)
    125
    """
    present_year = 2025

    def __init__(self):
        self.update()

    def create(self, coin):
        return coin(self.year)

    def update(self) -> None:
        self.year = Mint.present_year

class Coin:
    cents = None # 将由子类提供，而不是由 Coin 本身提供

    def __init__(self, year: int):
        self.year = year

    def worth(self) -> int:
        return self.cents + max(0, Mint.present_year - self.year - 50)

class Nickel(Coin):
    cents = 5

class Dime(Coin):
    cents = 10


class VirFib():
    """一个 Virahanka 斐波那契数。

    >>> start = VirFib()
    >>> start
    VirFib object, value 0
    >>> start.next()
    VirFib object, value 1
    >>> start.next().next()
    VirFib object, value 1
    >>> start.next().next().next()
    VirFib object, value 2
    >>> start.next().next().next().next()
    VirFib object, value 3
    >>> start.next().next().next().next().next()
    VirFib object, value 5
    >>> start.next().next().next().next().next().next()
    VirFib object, value 8
    >>> start.next().next().next().next().next().next() # Ensure start isn't changed
    VirFib object, value 8
    """

    def __init__(self, value: int = 0):
        self.value = value

    def next(self):
        if self.value == 0:
            result = VirFib(1)
        else:
            result = VirFib(self.value + self.previous)
        result.previous = self.value
        return result

    def __repr__(self) -> str:
        return "VirFib object, value " + str(self.value)


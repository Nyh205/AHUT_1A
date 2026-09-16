from math import gcd

# Example 1: Bank Account ADT
def create_account(owner, balance):
    return [owner, balance]

def get_owner(account):
    return account[0]

def get_balance(account):
    return account[1]

# ------- abstraction barrier -------
def withdraw(account, amount):
    balance = get_balance(account)
    if amount > balance:
        return 'Insufficient funds'
    return create_account(get_owner(account), balance - amount)


# Example 2: Rational Number ADT
def rational(n, d):
    # Uncomment this when ready
    # g = gcd(n, d)
    # return {'numer': n // g, 'denom': d // g}

    return {'numer': n, 'denom': d}

def numer(x):
    return x['numer']

def denom(x):
    return x['denom']

# ------- abstraction barrier -------
def add_rationals(x, y):
    nx, dx = numer(x), denom(x)
    ny, dy = numer(y), denom(y)
    return rational(nx * dy + ny * dx, dx * dy)

def mul_rationals(x, y):
    return rational(numer(x) * numer(y), denom(x) * denom(y))

def print_rational(x):
    print(numer(x), '/', denom(x))

def rationals_are_equal(x, y):
    return numer(x) * denom(y) == numer(y) * denom(x)

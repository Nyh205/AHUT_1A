def cascadeA(n):
    if n < 10:
        print(n)
    else:
        print(n)
        cascadeA(n // 10)
        print(n)

def cascadeB(n):
    print(n)
    if n >= 10:
        cascadeB(n // 10)
        print(n)

def cascadeC(n):
    print(n)
    if n < 10:
        cascadeC(n // 10)
        print(n)

def cascadeD(n):
    print(n)
    cascadeD(n // 10)
    print(n)

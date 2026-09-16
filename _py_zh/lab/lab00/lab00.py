def twenty_twenty_six():
    """想出一个最有创意的表达式，只用数字和 +、*、- 运算符（如果你愿意，
    也可以用 ** 和 %），使其求值结果为 2026。

    >>> twenty_twenty_six()
    2026
    """
    return ______


passphrase = 'REPLACE_THIS_WITH_PASSPHRASE'

def presem_survey(p):
    """
    你不需要理解这段代码。
    >>> presem_survey(passphrase)
    '490cbafdbd19352a62ff3988211180244329a1d311d1ee5e4a452791'
    """
    import hashlib
    return hashlib.sha224(p.encode('utf-8')).hexdigest()


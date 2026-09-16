def sum_list_iter(lst: list) -> int:
    """
    Given a list of integers, return the sum of
    all the elements iteratively (don't just use `sum`).

    >>> sum_list_iter([])
    0
    >>> sum_list_iter([1, 2, 3])
    6
    >>> sum_list_iter([4, 6434, 16, 20, 46, 7])
    6527
    """
    total = 0
    for elem in lst:
        total += elem
    return total

    # ALTERNATE SOLUTION:
    total = 0
    i = 0
    while i < len(lst):
        total += lst[i]
    return total


def sum_list_rec(lst: list) -> int:
    """
    Given a list of integers, return the sum of
    all the elements recursively (don't just use `sum`).

    >>> sum_list_rec([])
    0
    >>> sum_list_rec([1, 2, 3])
    6
    >>> sum_list_rec([4, 6434, 16, 20, 46, 7])
    6527
    """
    if len(lst) == 0:
        return 0
    else:
        return lst[0] + sum_list_rec(lst[1:])


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def decode(message: str) -> str:
    """
    Given an encoded secret message made of either spaces
    or all lowercase English letters that are shifted right by 3 letters,
    return the decoded message.

    Fun fact: This is a Caesar cipher with shift = 3

    >>> decode('d')
    'a'
    >>> decode('khoor')
    'hello'
    >>> decode('jrrgebh')
    'goodbye'
    >>> decode('pdb wkh irufh eh zlwk brx')
    'may the force be with you'
    """
    decoded_chars = []

    for char in message:
        if char == " ":
            decoded_chars.append(" ")
        else:
            # Find the current position, shift left by 3
            encoded_index = ALPHABET.index(char)
            # This is fine even for encoded_index < 3 because Python supports negative indexing
            decoded_index = encoded_index - 3
            decoded_chars.append(ALPHABET[decoded_index])

    # Join each character in decoded_chars into a single string,
    # where we "separate" each character with an empty string
    return "".join(decoded_chars)


def encode(message: str) -> str:
    """
    Given a plaintext message made of either spaces
    or all lowercase English letters, return the encoded message
    which shifts all the letters to the right by 3.

    Fun fact: This is a Caesar cipher with shift = 3

    >>> encode('a')
    'd'
    >>> encode('hello')
    'khoor'
    >>> encode('may the force be with you')
    'pdb wkh irufh eh zlwk brx'
    >>> 'go bears' == decode(encode('go bears'))
    True
    """
    encoded_chars = []

    for char in message:
        if char == " ":
            encoded_chars.append(" ")
        else:
            # Find the current position, shift right by 3,
            # and use modulo to wrap around if we go past 'z'
            original_index = ALPHABET.index(char)
            encoded_index = (original_index + 3) % len(ALPHABET)
            encoded_chars.append(ALPHABET[encoded_index])

    # Join each character in encoded_chars into a single string,
    # where we "separate" each character with an empty string
    return "".join(encoded_chars)

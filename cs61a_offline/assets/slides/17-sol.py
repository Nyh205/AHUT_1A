# O(n)
def search_list1(nums, target_num):
    """Returns the index of TARGET_NUM in sorted list NUMS or -1 if not found.
    >>> search_list1([1, 2, 3, 4], 3)
    2
    >>> search_list1([14, 23, 37, 48, 59], 23)
    1
    >>> search_list1([14, 23, 37, 48, 59], 47)
    -1
    """
    found_index = -1
    for i, elem in enumerate(nums):
        if elem == target_num:
            found_index = i
            break
    return found_index

# O(log n)
def search_list2(nums, target_num):
    """Returns the index of TARGET_NUM in sorted list NUMS or -1 if not found.
    >>> search_list2([1, 2, 3, 4], 3)
    2
    >>> search_list2([14, 23, 37, 48, 59], 23)
    1
    >>> search_list2([14, 23, 37, 48, 59], 47)
    -1
    """
    min_index = 1
    max_index = len(nums)
    while min_index <= max_index:
        middle_index = (min_index + max_index) // 2
        if target_num == nums[middle_index]:
            return middle_index
        elif target_num > nums[middle_index]:
            min_index = middle_index + 1
        else:
            max_index = middle_index - 1
    return -1


# O(n)
def is_prime1(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

# O(sqrt(n))
def is_prime2(n):
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


# O(n^2)
def bar(n):
    i, sum = 1, 0
    while i <= n:
        sum += biz(n)
        i += 1
    return sum

def biz(n):
    i, sum = 1, 0
    while i <= n:
        sum += i**3
        i += 1
    return sum

def factorial_one(x):
    if x == 1:          # 1 is simple
        return x
    else:
        result = 1
        while x > 1:
            result *= x
            x -= 1      # x * (x - 1) * (x - 2) ... * 2 * result(=1) factorial!
        return result   # jump out of the while loop and return the result

factorial_one(4)
# 24

def factorial_two(n):
    count = 1
    result = 1
    while count <= n:
        result *= count
        count += 1
    return result

factorial_two(4)
# 24

def factorial_three(n):
    result = 1
    for i in range(1, n+1): # for loop is much easier
        result *= i
    return result

factorial_three(4)
# 24

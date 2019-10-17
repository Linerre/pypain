# usr/bin/python3
# -*- coding: utf-8 -*-

# let's say user does enter a number
user_raw = float(input('Please enter a number: ')) # num_1

 # let's say we only support + - x /
oper_raw = input('Please enter the operator: ')) # op_1

while oper_raw != '+' or oper_raw != '-' or oper_raw != 'x' or oper_raw != '/':
    print('Operators only support +, -, *, /')
    oper_raw = input('Please enter the operator: '))

user_one = float(input('Please enter another number: '))

while True:
    oper_one = input('Please enter the operator or hit = to get the result')
    if oper_one == '=':
        result = eval(user_raw + oper_raw + user_one)
        print(result)
        break
    else:
        user_two = float(input('Please enter still another number: '))
        oper_two = 
        result = eval(user_raw + oper_raw + user_one + )

# I tried to emulate a caculator that can at least carry out 
# addition, deduction, multiple and division.
# Yet this approach is severely flawed since you will need 
# numberless vars to hold all the values, both operators and numbers
# before you finally evaluate the caculation
# I chose so because I wanted to see how far I can go without any use of list/dict.
# I even tried to avoid eval(), which is almost impossible in Python. 
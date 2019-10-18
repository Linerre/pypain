# usr/bin/python3
# -*- coding: utf-8 -*-

# let's say user does enter a number
num_one = input('Please enter a number: ') # num_1 

 # let's say we only support + - x /
op = input('Please enter the operator: ') # op_1

while op != '+' and op != '-' and op != '*' and op != '/': # infinite loop fixed
    print('Operators only support +, -, *, /')
    op = input('Please enter the operator: ')

num_two = input('Please enter another number: ') # num_2
result = str(eval(num_one + op + num_two)) # no float ever needed because of the introduction of eval
# but the eval statement will return a int/float value!
# not a string! Pay detailed attention to this!

while True:
    op = input('Please enter the operator or hit = to get the result: ')
    if op == '=':
        print(result)
        break
    else:
        num_one = result
        num_two = input('Please enter still another number: ')

        op = input('Please enter the operator: ')
        while op != '+' and op != '-' and op != '*' and op != '/': # infinite loop fixed
            print('Operators only support +, -, *, /')
            op = input('Please enter the operator: ')

        result = str(eval(num_one + op + num_two))
        continue




# Try to calculate each time after you get two numbers

# try this
# (3 + 4) / 5 * 6
# since this simple calculator just takes nums one by one 
# it will do the cal from right to left
# I use round brackets here for human reading purpoeses

# sth still causing bugs there:
# Please enter a number: 3
# Please enter the operator: +
# Please enter another number: 4
# Please enter the operator or hit = to get the result: /
# Please enter still another number: 5
# Please enter the operator: *
# Please enter the operator or hit = to get the result: =
# 35
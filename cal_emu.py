# usr/bin/python3
# -*- coding: utf-8 -*-

# let's say user does enter a number
num_one = float(input('Please enter a number: ')) # num_1

 # let's say we only support + - x /
op = input('Please enter the operator: ') # op_1

while op == '+' or op == '-' or op == '*' or op == '/':
    print('Operators only support +, -, *, /')
    op = input('Please enter the operator: ')

num_two = float(input('Please enter another number: ')) # num_2
result = eval(num_one + op + num_two)

while True:
    op = input('Please enter the operator or hit = to get the result')
    if op == '=':
        print(result)
        break
    else:
        num_one = result
        num_two = float(input('Please enter still another number: '))
        op = input('Please enter the operator')
        result = eval(num_one + op + num_two)
        continue




# Try to calculate each time after you get two numbers

# try this
# (3 + 4) / 5 * 6
# since this simple calculator just takes nums one by one 
# it will do the cal from right to left
# I use round brackets here for human reading purpoeses

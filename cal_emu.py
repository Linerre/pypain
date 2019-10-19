# usr/bin/python3
# -*- coding: utf-8 -*-

# let's say user does enter a number
num_one = input('Please enter a number: ') # num_1 

 # let's say we only support + - 8 /
op = input('Please enter the operator: ') # op_1

while op != '+' and op != '-' and op != '*' and op != '/': # decide operation
    print('Operators only support +, -, *, /')
    op = input('Please enter the operator: ')

num_two = input('Please enter another number: ') # num_2
result = str(eval(num_one + op + num_two)) #  the eval statement will return a int/float value! Not a string!
# so need to keep result a str for next eval if needed 
# Pay close attention to this!

while True:
    op = input('Please enter an operator or hit = to get the result: ') # continue or end?
    while op != '+' and op != '-' and op != '*' and op != '/' and op != '=': # go on and check it
            print('Operator must be one of +, -, *, /, =')
            op = input('Please enter the operator: ')
    if op == '=':
        print(result)
        break
    else:
        num_one = result # integrate the previous result into the new counting base
        num_two = input('Please enter still another number: ') # ask for a new number
        result = str(eval(num_one + op + num_two)) # here we go
        continue # start another round of loop





# since this simple calculator just takes nums one by one 
# it will do the cal from right to left
# I use round brackets here for human reading purpoeses

# try this
# (3 + 4) / 5 * 6
# 8.399999999999999

# it should be 8.4
# Need to find out why

# Explanations:
# Because the precison is different betweeen decimal fraction and base 2 bianry fraction
# See Python's official guide: https://docs.python.org/3/tutorial/floatingpoint.html
# or two explantions in Chinese: 
# https://www.zhihu.com/question/25457573
# https://justjavac.com/codepuzzle/2012/11/11/codepuzzle-float-who-stole-your-accuracy.html
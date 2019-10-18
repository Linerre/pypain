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
result = str(eval(num_one + op + num_two)) # keep result a str for next eval if needed
# but the eval statement will return a int/float value!
# not a string! Pay close attention to this!

while True:
    op = input('Please enter an operator or hit = to get the result: ') # continue or end?
    while op != '+' and op != '-' and op != '*' and op != '/' and op != '=': # go on and check it
            print('Operator must be one of +, -, *, /, =')
            op = input('Please enter the operator: ') # already an op here!
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
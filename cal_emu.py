# usr/bin/python3
# -*- coding: utf-8 -*-

# let's say user does enter a number
num_one = input('Please enter a number: ') # num_1 

 # let's say we only support + - x /
op = input('Please enter the operator: ') # op_1

while op != '+' and op != '-' and op != '*' and op != '/': # decide operation
    print('Operators only support +, -, *, /')
    op = input('Please enter the operator: ')

num_two = input('Please enter another number: ') # num_2
result = str(eval(num_one + op + num_two)) # keep result a str for next eval if needed
# but the eval statement will return a int/float value!
# not a string! Pay detailed attention to this!

while True:
    op = input('Please enter the operator or hit = to get the result: ')
    if op == '=':
        print(result)
        break
    else:
        num_one = result # integrate the previous result into the new counting base
        num_two = input('Please enter still another number: ') # ask for a new number
        op = input('Please enter the operator: ') # ask for a new op
        while op != '+' and op != '-' and op != '*' and op != '/': # check it
            print('Operators only support +, -, *, /')
            op = input('Please enter the operator: ')
        result = str(eval(num_one + op + num_two)) # here we go
        continue # start another round of loop




# Try to calculate each time after you get two numbers

# try this
# (3 + 4) / 5 * 6
# since this simple calculator just takes nums one by one 
# it will do the cal from right to left
# I use round brackets here for human reading purpoeses

# won't work after the 3rd number
# keep looping
# need to find out why
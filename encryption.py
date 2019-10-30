#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To test encription using python3
"""

# ==================== Encipher ===================
lower = 'qwertyuiopasdfghjklzxcvbnm'
upper = 'QWERTYUIOPASDFGHJKLZXCVBNM'
punc  = {' ': '\U0001F0CF',
         ',': '\U0001F313',
         '.': '\U0001F315',
        '\'': '\U0001F31B',
        '"' : '\U0001F31F'
}
source = []
deck   = []
cipher = []

symbol = {'spades'  : '♠',
        'clubs'   : '♣',
        'diamonds': '♦',
        'hearts'  : '♥'
}


for v in symbol.values():
    for i in range(1,14):
        deck.append(v+str(i))

def alphabet(str):
    for letter in str:
        source.append(letter)
    return source.sort()

alphabet(lower+upper)

for letter in source:
        cipher.append([letter, deck[source.index(letter)]]) #fix the bug, awkwardly

encrypt = dict(cipher).update(punc)
print(encrypt)

# ==================== decipher ===================
message = 'This takes a string, finds all occurrences of a number followed by an alphanumeric word, and returns a string wherein every such occurrence is decrementedby one.'

def enigma(str):
    encrypted = []
    for i in str:
        encrypted.append(encrypt[i])
    return ''.join(encrypted)

print(enigma(message))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To test encription using python3
"""

# ==================== Encipher ===================
lower = 'qwertyuiopasdfghjklzxcvbnm'
upper = 'QWERTYUIOPASDFGHJKLZXCVBNM'
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
    for card in deck:
        cipher.append([letter, card])

encrypt = dict(cipher)
print(encrypt)

# ==================== decipher ===================

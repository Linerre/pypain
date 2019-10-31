#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To test encription using python3
"""

# The encryption key should look like this:
# {'A': '♠1', 'B': '♠2', 'C': '♠3', 'D': '♠4', 'E': '♠5',
# 'F': '♠6', 'G': '♠7', 'H': '♠8', 'I': '♠9', 'J': '♠T',
# 'K': '♠J', 'L': '♠Q', 'M': '♠K', 'N': '♣1', 'O': '♣2',
# 'P': '♣3', 'Q': '♣4', 'R': '♣5', 'S': '♣6', 'T': '♣7',
# 'U': '♣8', 'V': '♣9', 'W': '♣T', 'X': '♣J', 'Y': '♣Q',
# 'Z': '♣K', 'a': '♦1', 'b': '♦2', 'c': '♦3', 'd': '♦4',
# 'e': '♦5', 'f': '♦6', 'g': '♦7', 'h': '♦8', 'i': '♦9',
# 'j': '♦T', 'k': '♦K', 'l': '♦Q', 'm': '♦K', 'n': '♥1',
# 'o': '♥2', 'p': '♥3', 'q': '♥4', 'r': '♥5', 's': '♥6',
# 't': '♥7', 'u': '♥8', 'v': '♥9', 'w': '♥T', 'x': '♥J',
# 'y': '♥Q', 'z': '♥K', ' ': '🃏'}


# ==================== Encryption ===================
import pprint

lower = 'qwertyuiopasdfghjklzxcvbnm'
upper = 'QWERTYUIOPASDFGHJKLZXCVBNM'
punc  = {' ': '🃏'  #'\U0001F0CF',
        #  ',': '\U0001F313',
        #  '.': '\U0001F315',
        # '\'': '\U0001F31B',
        # '"' : '\U0001F31F'
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
        if i < 10:
            deck.append(v+str(i))
        elif i == 10:
            deck.append(v+'T')
        elif i == 11:
            deck.append(v+'J')
        elif i == 12:
            deck.append(v+'Q')
        elif i == 13:
            deck.append(v+'K')


def alphabet(str):
    for letter in str:
        source.append(letter)
    return source.sort()

alphabet(lower+upper)

for letter in source:
        cipher.append([letter, deck[source.index(letter)]]) #fix the bug, awkwardly

encrypt = dict(cipher)
encrypt.update(punc)
pp = pprint.PrettyPrinter(indent=2, width=10)
pp.pprint(encrypt)

# ==================== encipher ===================
message = 'This takes a string finds all occurrences of a number followed by an alphanumeric word and returns a string wherein every such occurrence is decrementedby one'

def enigma(str):
    encrypted = []
    for i in str:
        encrypted.append(encrypt[i])
    return ''.join(encrypted)

print(enigma(message))


# ==================== decipher ===================
secret = '♣7♦8♦9♥6🃏♥7♦1♦J♦5♥6🃏♦1🃏♥6♥7♥5♦9♥1♦7🃏♦6♦9♥1♦4♥6🃏♦1♦Q♦Q🃏♥2♦3♦3♥8♥5♥5♦5♥1♦3♦5♥6🃏♥2♦6🃏♦1🃏♥1♥8♦K♦2♦5♥5🃏♦6♥2♦Q♦Q♥2♥T♦5♦4🃏♦2♥Q🃏♦1♥1🃏♦1♦Q♥3♦8♦1♥1♥8♦K♦5♥5♦9♦3🃏♥T♥2♥5♦4🃏♦1♥1♦4🃏♥5♦5♥7♥8♥5♥1♥6🃏♦1🃏♥6♥7♥5♦9♥1♦7🃏♥T♦8♦5♥5♦5♦9♥1🃏♦5♥9♦5♥5♥Q🃏♥6♥8♦3♦8🃏♥2♦3♦3♥8♥5♥5♦5♥1♦3♦5🃏♦9♥6🃏♦4♦5♦3♥5♦5♦K♦5♥1♥7♦5♦4♦2♥Q🃏♥2♥1♦5'

def decipher(str):
    reveal = []
    sep = []
    for i in str:
        if i in

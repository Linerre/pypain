#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To test encription using python3
"""

lower = 'qwertyuiopasdfghjklzxcvbnm'
upper = 'QWERTYUIOPASDFGHJKLZXCVBNM'
source = []

spades   = '♠'
clubs    = '♣'
diamonds = '♦'
hearts   = '♥'



def alphabet(str):
    for letter in str:
        source.append(letter)
    return source.sort()

alphabet(lower+upper)
encript = {}.fromkeys(source)
print(encript)

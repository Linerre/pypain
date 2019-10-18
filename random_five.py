# -*- coding: utf-8 -*-

# 1. selects 5 random words from a word list each time run
# 2. automatically deletes those 5 words from the list
# 3. put the selected word into a new working markdown file

from sys import argv
import random

script, filename = argv

# open the file and print the word
with open(filename, 'r') as original_file:
    content = original_file.read()
    words = content.split() # stripping '/n' to make the long str a list
    random.shuffle(words)
    picks = random.sample(words, 5)

    for pick in picks: #remove those five words from the list
        words.remove(pick)
    new_content = '\n'.join(words)

with open(filename, 'w') as new_file: # open the file again with write mode
    new_file.write(new_content)


with open('drill.md', 'w') as note: # put newly-selected word into the working file
    for pick in picks:
        pick = '- ' + pick + '\n'
        note.write(pick)

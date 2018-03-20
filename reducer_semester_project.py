#!/usr/bin/env python
#takes 
from operator import itemgetter
import sys

current_word = None
current_hate_count = 0
current_offensive_count = 0
current_neither_count = 0
hate_count = 0
offensive_count = 0
neither_count = 0
word = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    word, count = line.split('\t', 1)
    hate_count, offensive_count, neither_count = count.split(' ')
    #print '%s %s %s' % (hate_count, offensive_count, neither_count)
	
    # convert count (currently a string) to int
    try:
        hate_count = int(hate_count)
        offensive_count = int(offensive_count)
        neither_count = int(neither_count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:
        current_hate_count += hate_count
        current_offensive_count += offensive_count  
        current_neither_count += neither_count  
        
    else:
        if current_word:
            # write result to STDOUT
            print '%s\t%i %i %i' % (current_word,current_hate_count,current_offensive_count,current_neither_count)
        current_hate_count = hate_count
        current_offensive_count = offensive_count
        current_neither_count = neither_count
        current_word = word

# do not forget to output the last word if needed!
if current_word == word:
    print '%s\t%i %i %i' % (current_word, current_hate_count,current_offensive_count,current_neither_count)

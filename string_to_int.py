# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 19:10:12 2015

@author: James T. 
"""

def get_int(s):
# concatentates all integers in a string to a new string
# then returns the integer of the new string
    numb = ''
    for i in s:
        try:
            int(i)
            numb += i
        except ValueError:
           pass 
    return int(numb)

def letter_to_snumb(s):
# converts all 'o' to '0' and 'z' to '2'
    s = unicode(s) # converts to unicode to use .isnumeric()
    new_s = ''
    for i in s:
        if i.isnumeric():
            new_s += i
        elif i.lower() == 'o':
            new_s += '0'
        elif i.lower() == 'z':
            new_s += '2'
    return new_s
    
print letter_to_snumb('ZZ8\n\n')
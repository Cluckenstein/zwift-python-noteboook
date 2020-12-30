#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 15:37:11 2020

@author: maximilianreihn
"""

from calc import training
import os 
# print(os.getcwd())

e = training('30-12-2020-Grundlagen-Treppe', 'Das letzte Workout auf Zwift für dieses Jahr!', offline = True)



# e.add(600, [50,60])


# for i in range(4):
#     e.add(60, 80)
#     e.add(60, 70)
#     e.add(60, 90)
#     e.add(60, 70)
#     e.add(60, 100)
    
#     e.add(420, 60)

# e.interval(40, 30, 50, 20, 60)



# e.add(600, [60,50])


# e.text(1, 'Ein letztes mal  2020 ;)')

# e.text(2, 'Heute mal ein Treppe...')
# e.text(3, 'Entspannter als sonst :)')

e.add(60,60)
e.add(60,70)
e.add(60,80)
e.add(60,90)
e.add(60,60)
e.add(60,70)
e.add(60,80)
e.add(60,90)
e.add(60,60)
e.add(60,70)
e.add(60,80)
e.add(60,90)
e.add(60,60)
e.add(60,70)
e.add(60,80)
e.add(60,90)
e.add(60,60)

e.plot()

e.generate('yest')

'''
Test for online interface 


add(600, [50,60])


add(60, 80)
add(60, 70)
add(60, 90)
add(60, 70)
add(60, 100)

add(420, 60)

interval(40, 30, 50, 20, 60)



add(600, [60,50])


text(1, 'Ein letztes mal  2020 ;)')

text(2, 'Heute mal ein Treppe...')
text(3, 'Entspannter als sonst :)')


docker run -i -p 5000:5000 -v /Users/maximilianreihn/Documents/repos/zwift-python-noteboook/zwo_files/:/src/zwo_files/ --name work worker 
'''

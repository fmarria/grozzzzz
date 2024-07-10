#!/usr/bin/env python

import sys
from select import select

import termios
import tty

import time

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >

t : up (+z)
b : down (-z)

anything else : stop

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%

CTRL-C to quit
"""

speed_limit = 1
turn_limit = 1
norm = 0.1

moveBindings = {
        'i':(1,0),
        'o':(1,-1),
        'j':(0,1),
        'l':(0,-1),
        'u':(1,1),
        ',':(-1,0),
        '.':(-1,1),
        'm':(-1,-1),
        'k':(0, 0),
    }

speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
    }

def getKey(settings, timeout):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def saveTerminalSettings():
    return termios.tcgetattr(sys.stdin)

def restoreTerminalSettings(old_settings):
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def action(status):
    settings = saveTerminalSettings()
    try:
        print('Start interactive mode, press button!')
        while(1):
            key = getKey(settings, 0.5)
            print(status)

            if key in moveBindings:
                status['v'] = moveBindings[key][0] * norm
                status['w'] = moveBindings[key][1] * norm

            if key in speedBindings:
                status['v'] = min(speed_limit, status['v'] * speedBindings[key][0])
                status['w'] = min(turn_limit, status['w'] * speedBindings[key][1])
                if status['v'] == speed_limit:
                    print("Linear speed limit reached!")
                if status['w'] == turn_limit:
                    print("Angular speed limit reached!")

            if key == 'p':
                print('Press button "p"')
            
            if key == '\x03':
                break

            time.sleep(0.1)
            print(key)
        
    except Exception as e:
         print(e)
    finally:
        print('Interactive mode has been stopped!') 
        restoreTerminalSettings(settings)

def handler():
    pass


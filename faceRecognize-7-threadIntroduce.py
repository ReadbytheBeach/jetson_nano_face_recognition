# function can't make parallal moving camera, so we need 'threadings'
from threading import Thread
import time

def BigBox(color):
    while True:
        print(color, ' Box is Open')
        time.sleep(5)
        print(color, ' Box is Closed')
        time.sleep(5)

def SmallBox(color1):
    while True:
        print(color1, ' Box is Open')
        time.sleep(1)
        print(color1,' Box is Closed')
        time.sleep(1)

# BigBox()
# SmallBox()

# create the Threads

bigBoxThread = Thread(target=BigBox,args=('red',))
smallBoxThread = Thread(target=SmallBox,args=('blue',))

# kill the program that will kill the threads 
bigBoxThread.daemon = True
smallBoxThread.daemon = True

# lauch the threads 
bigBoxThread.start()
smallBoxThread.start()

while True:
    pass

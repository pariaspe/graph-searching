#! /usr/bin/env python

"""Implementation of Breadth First Search algorithm."""

import os

__author__ = "Juan G. Victores"


LOCAL_PATH = os.path.dirname(os.path.abspath(__file__)).split("base")[0]
FILE_NAME = LOCAL_PATH + "maps/map1/map1.csv"
START_X = 2
START_Y = 2
END_X = 7
END_Y = 2

class Node:
    def __init__(self, x, y, myId, parentId):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId))

nodes = []

init = Node(START_X, START_Y, 0, -2)
# init.dump()

nodes.append(init)

charMap = []

def dumpMap():
    for line in charMap:
        print(line)

with open(FILE_NAME) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        line = f.readline()

charMap[START_X][START_Y] = '3'
charMap[END_X][END_Y] = '4'

dumpMap()

done = False
goalParentId = -1

while not done:
    print("--------------------- number of nodes: "+str(len(nodes)))
    for node in nodes:
        node.dump()

        # up
        tmpX = node.x - 1
        tmpY = node.y
        if( charMap[tmpX][tmpY] == '4' ):
            print("up: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("up: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

        # down
        tmpX = node.x + 1
        tmpY = node.y
        if( charMap[tmpX][tmpY] == '4' ):
            print("down: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("down: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

        # right
        tmpX = node.x
        tmpY = node.y + 1
        if( charMap[tmpX][tmpY] == '4' ):
            print("right: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("right    : mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

        # left
        tmpX = node.x
        tmpY = node.y - 1
        if( charMap[tmpX][tmpY] == '4' ):
            print("left: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("left: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

        dumpMap()

print("%%%%%%%%%%%%%%%%%%%")
ok = False
while not ok:
    for node in nodes:
        if( node.myId == goalParentId ):
            node.dump()
            goalParentId = node.parentId
            if( goalParentId == -2):
                print("%%%%%%%%%%%%%%%%%2")
                ok = True

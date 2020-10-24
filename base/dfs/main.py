#! /usr/bin/env python

"""Implementation of Depth First Search algorithm."""

import os
from itertools import cycle

__author__ = "Pedro Arias Perez and Juan G. Victores"


LOCAL_PATH = os.path.dirname(os.path.abspath(__file__)).split("base")[0]
FILE_NAME = LOCAL_PATH + "maps/map1/map1.csv"
START_X = 2
START_Y = 2
END_X = 7
END_Y = 2


class CharMap:
    """
    A map that represents the C-Space.
    """

    def __init__(self, filename, start=None, end=None):
        self.charMap = []
        self.nodes = []
        self.aux = None

        self.read(filename)
        self.start = start
        self.end = end

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, s):
        if s is not None:
            self.charMap[s[0]][s[1]] = "3"
            self.nodes.append(Node(s[0], s[1], 0, -2))
        self.__start = s

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, e):
        if e is not None:
            self.charMap[e[0]][e[1]] = "4"
        self.__end = e

    def read(self, filename):
        """
        Reads map from file and save it at charMap attribute.

        filename: path to file.
        """

        with open(FILE_NAME) as f:
            line = f.readline()
            while line:
                charLine = line.strip().split(',')
                self.charMap.append(charLine)
                line = f.readline()

    def dump(self):
        """
        Prints colored map.
        """

        for line in self.charMap:
            l = ""
            for char in line:
                l += str(char)
            print(l)
        print()  # empty line behind map

    def check(self, cell, node):
        """
        Check if cell is end or not visited and add it to tree nodes.

        cell: current cell
        node: parent node

        return: parent id if end else -1
        """

        if( self.charMap[cell[0]][cell[1]] == '4' ):  # end
            return node.myId
        elif ( self.charMap[cell[0]][cell[1]] == '0' ):  # empty
            newNode = Node(cell[0], cell[1], len(self.nodes), node.myId)
            self.charMap[cell[0]][cell[1]] = "2"
            self.nodes.append(newNode)
        return -1


class Node:
    """
    Node: visited cell of the map.
    """

    def __init__(self, x, y, myId, parentId):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId

    def dump(self):
        print("---------- x", str(self.x), "| y", str(self.y), "| id",\
              str(self.myId), "| parentId", str(self.parentId))


def main():
    map = CharMap(FILE_NAME, [START_X, START_Y], [END_X, END_Y])

    map.dump()

    directions = cycle([[-1, 0], [0, 1], [1, 0], [0, -1]])  # up, right, down, left, up, right...
    # directions = cycle([[-1, 0], [0, -1], [1, 0], [0, 1]])  # up, left, down, right, up, left...
    current_direction = next(directions)

    done = False
    goalParentId = -1
    print("--------------------- number of nodes: ", len(map.nodes))

    while True:
        node = map.nodes[-1]

        tmpX = node.x + current_direction[0]
        tmpY = node.y + current_direction[1]
        if map.check([tmpX, tmpY], node) != -1:
            map.dump()
            goalParentId = node.myId
            break

        if node == map.nodes[-1]:
            current_direction = next(directions)
            if current_direction == first_direction:
                map.nodes.pop()
        else:
            first_direction = current_direction
            map.dump()


    print("%%%%%%%%%%%%%%%%%%%")
    ok = False
    while not ok:
        for node in map.nodes:
            if( node.myId == goalParentId ):
                node.dump()
                goalParentId = node.parentId
                if( goalParentId == -2):
                    print("%%%%%%%%%%%%%%%%%")
                    ok = True

if __name__ == "__main__":
    main()

#! /usr/bin/env python

"""Implementation of BFS algorithm with colored map."""

import os
import sys
import argparse
import time

sys.path.append('../')
from utils import Output, OUTPUT_MODE, UserInputException, Colors, CharMapCell,\
                    CharMap, Node, get_route

__author__ = "Pedro Arias Perez"


LOCAL_PATH = os.path.dirname(os.path.abspath(__file__)).split("extra")[0]
FILE_NAME = LOCAL_PATH + "maps/{0}/{0}.csv"
MAP = "map1"
START_X = 2
START_Y = 2
END_X = 7
END_Y = 2


def read_from_user(m, s, e):
    while True:
        try:
            map = input("Map ({}): ".format(m))
            if map == "":
                map = m
            charMap = CharMap(FILE_NAME.format(map))
            charMap.dump()
            break
        except EOFError:
            print("\nBye!")
            return None, None, None
        except UserInputException:
            pass

    while True:
        try:
            start_x = input("Start X ({}): ".format(s[0]))
            if start_x == "":
                start_x = s[0]
            start_y = input("Start Y ({}): ".format(s[1]))
            if start_y == "":
                start_y = s[1]
            start = [int(start_x), int(start_y)]

            charMap = CharMap(FILE_NAME.format(map), start)
            charMap.dump()
            break
        except EOFError:
            print("\nBye!")
            return None, None, None
        except UserInputException:
            pass

    while True:
        try:
            end_x = input("End X ({}): ".format(e[0]))
            if end_x == "":
                end_x = e[0]
            end_y = input("End Y ({}): ".format(e[1]))
            if end_y == "":
                end_y = e[1]
            end = [int(end_x), int(end_y)]

            charMap = CharMap(FILE_NAME.format(map), start, end)
            charMap.dump()
            break
        except EOFError:
            print("\nBye!")
            return None, None, None
        except UserInputException:
            pass

    return map, start, end


def bfs(map):
    done = False
    goalParentId = -1
    while not done:
        print("--------------------- number of nodes: ", len(map.nodes))
        for node in map.nodes:
            map.set_current([node.x, node.y])
            map.clear_news()
            node.dump()

            # up
            tmpX = node.x - 1
            tmpY = node.y
            if map.check([tmpX, tmpY], node) != -1:
                map.dump()
                done = True
                goalParentId = node.myId
                break

            # down
            tmpX = node.x + 1
            tmpY = node.y
            if map.check([tmpX, tmpY], node) != -1:
                map.dump()
                done = True
                goalParentId = node.myId
                break

            # right
            tmpX = node.x
            tmpY = node.y + 1
            if map.check([tmpX, tmpY], node) != -1:
                map.dump()
                done = True
                goalParentId = node.myId
                break

            # left
            tmpX = node.x
            tmpY = node.y - 1
            if map.check([tmpX, tmpY], node) != -1:
                map.dump()
                done = True
                goalParentId = node.myId
                break

            map.dump()
    return goalParentId


def main(filename, start, end):
    try:
        map = CharMap(filename, start, end)
    except UserInputException:
        print("[Error] Exiting..", file=stderr)
        return -1

    map.dump()

    goalParentId = bfs(map)
    route = get_route(map.nodes, goalParentId)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Breadth First Search Algorithm.")
    parser.add_argument('-m', '--map', metavar='MAP', dest='map', default=MAP, help='change map folder')
    parser.add_argument('-s', '--start', type=int, nargs=2, metavar='N', dest='start', default=[START_X, START_Y], help='change start point')
    parser.add_argument('-e', '--end', type=int, nargs=2, metavar='N', dest='end', default=[END_X, END_Y], help='change end point')
    parser.add_argument('-i', action='store_true', help='interactive mode (choose map, start, end...)')
    parser.add_argument('-o', type=Output, choices=Output, metavar='OUTPUT', dest='output', default=OUTPUT_MODE, help='output mode (choose from none, base, colored)')
    args = parser.parse_args()

    map = args.map
    OUTPUT_MODE = args.output
    if OUTPUT_MODE == Output.NONE:
        sys.stdout = open(os.devnull, 'w')  # silence
    start = args.start
    end = args.end
    if args.i:
        map, start, end = read_from_user(map, start, end)

    if map is not None and start is not None and end is not None:
        main(FILE_NAME.format(map), start, end)
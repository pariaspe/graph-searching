#! /usr/bin/env python

"""Implementation of DFS algorithm with colored map."""

import sys
import os
from itertools import cycle
import argparse

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
            return None, None, None, None
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
            return None, None, None, None
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
            return None, None, None, None
        except UserInputException:
            pass

    while True:
        try:
            str = input("Right-handed? (Yes or No) ")
            if str in ["Yes", "yes", "y", ""]:
                is_clockwise = True
                break
            elif str in ["No", "no", "n"]:
                is_clockwise = False
                break
        except EOFError:
            print("\nBye!")
            return None, None, None, None

    return map, start, end, is_clockwise


def dfs(map, is_clockwise=True):
    if is_clockwise:
        directions = cycle([[-1, 0], [0, 1], [1, 0], [0, -1]])  # up, right, down, left, up, right...
    else:
        directions = cycle([[-1, 0], [0, -1], [1, 0], [0, 1]])  # up, left, down, right, up, left...
    current_direction = next(directions)

    done = False
    goalParentId = -1
    first_direction = None
    ("--------------------- number of nodes: ", len(map.nodes))

    while True:
        map.clear_news()
        node = map.nodes[-1]
        map.set_current([node.x, node.y])

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
    return goalParentId


def main(filename, start, end, is_clockwise):
    try:
        map = CharMap(filename, start, end)
    except UserInputException:
        print("[Error] Exiting..", file=stderr)
        return -1

    map.dump()

    goalParentId = dfs(map, is_clockwise)
    route = get_route(map.nodes, goalParentId)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Depth First Search Algorithm.")
    parser.add_argument('-m', '--map', metavar='MAP', dest='map', default=MAP, help='change map folder')
    parser.add_argument('-s', '--start', type=int, nargs=2, metavar='N', dest='start', default=[START_X, START_Y], help='change start point')
    parser.add_argument('-e', '--end', type=int, nargs=2, metavar='N', dest='end', default=[END_X, END_Y], help='change end point')
    parser.add_argument('-i', action='store_true', help='interactive mode (choose map, start, end...)')
    parser.add_argument('-k', action='store_false', help='set counter clockwise (left-handed)')
    parser.add_argument('-o', type=Output, choices=Output, metavar='OUTPUT', dest='output', default=OUTPUT_MODE, help='output mode (choose from none, base, colored)')
    args = parser.parse_args()

    map = args.map
    OUTPUT_MODE = args.output
    if OUTPUT_MODE == Output.NONE:
        sys.stdout = open(os.devnull, 'w')  # silence
    start = args.start
    end = args.end
    is_clockwise = args.k
    if args.i:
        map, start, end, is_clockwise = read_from_user(map, start, end)

    if map is not None and start is not None and end is not None and is_clockwise is not None:
        main(FILE_NAME.format(map), start, end, is_clockwise)

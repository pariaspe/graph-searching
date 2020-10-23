#! /usr/bin/env python

"""Comparation of algorithms."""

import os
import sys
import time
from collections import Counter

from utils import CharMap, UserInputException, get_route, OUTPUT_MODE, Output
from bfs.bfs import bfs
from dfs.dfs import dfs

__author__ = "Pedro Arias Perez"


LOCAL_PATH = os.path.dirname(os.path.abspath(__file__)).split("extra")[0]
FILE_NAME = LOCAL_PATH + "maps/{0}/{0}.csv"

RESULTS = []
BFS_ACC = [0, 0, 0]
DFS_ACCR = [0, 0, 0]
DFS_ACCL = [0, 0, 0]


def run_bfs(map):
    sys.stdout = open(os.devnull, 'w')  # silence
    t0 = time.time()
    goalParentId = bfs(map)
    route = get_route(map.nodes, goalParentId)
    tf = time.time()
    sys.stdout = sys.__stdout__
    result = [len(route), map.n_checked, round((tf-t0), 5)]
    return result


def run_dfs(map, is_clockwise=True):
    sys.stdout = open(os.devnull, 'w')  # silence
    t0 = time.time()
    goalParentId = dfs(map, is_clockwise)
    route = get_route(map.nodes, goalParentId)
    tf = time.time()
    sys.stdout = sys.__stdout__
    result = [len(route), map.n_checked, round((tf-t0), 5)]
    return result


def do_compare(map_name, start, end):
    map = CharMap(FILE_NAME.format(map_name), start, end)

    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("%%\t\t{0}\t\t%%".format(map_name))
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print()
    print("    \tRoute \t Cells \t")
    print("Alg.\tLength\tChecked\t  Time")
    print("--------------------------------")

    bfs_result = run_bfs(map)
    print("{0}\t{1}\t{2}\t{3}".format("BFS", *bfs_result))
    BFS_ACC[0] += bfs_result[0]
    BFS_ACC[1] += bfs_result[1]
    BFS_ACC[2] += round(bfs_result[2], 5)

    # time.sleep(1)
    map.reset()

    dfsr_result = run_dfs(map)
    print("{0}\t{1}\t{2}\t{3}".format("DFSr", *dfsr_result))
    DFS_ACCR[0] += dfsr_result[0]
    DFS_ACCR[1] += dfsr_result[1]
    DFS_ACCR[2] += round(dfsr_result[2], 5)

    # time.sleep(1)
    map.reset()

    dfsl_result = run_dfs(map, False)
    print("{0}\t{1}\t{2}\t{3}".format("DFSl", *dfsl_result))
    DFS_ACCL[0] += dfsl_result[0]
    DFS_ACCL[1] += dfsl_result[1]
    DFS_ACCL[2] += round(dfsl_result[2], 5)

    map.reset()
    # time.sleep(1)

    shortest = "BFS" if 48 < 90 < 80 else "DFSr" if 90 < 80 else "DFSl"


    shortest = "BFS" if bfs_result[0] < min(dfsr_result[0], dfsl_result[0]) else "DFSr" if dfsr_result[0] < dfsl_result[0] else "DFSl"
    shortest_val = min(bfs_result[0], dfsr_result[0], dfsl_result[0])
    less_cell = "BFS" if bfs_result[1] < min(dfsr_result[1], dfsl_result[1]) else "DFSr" if dfsr_result[1] < dfsl_result[1] else "DFSl"
    less_cell_val = min(bfs_result[1], dfsr_result[1], dfsl_result[1])
    fastest = "BFS" if bfs_result[2] < min(dfsr_result[2], dfsl_result[2]) else "DFSr" if dfsr_result[2] < dfsl_result[2] else "DFSl"
    fastest_val = min(bfs_result[2], dfsr_result[2], dfsl_result[2])

    print()
    print("Shortest -------> {0} ({1})".format(shortest, shortest_val))
    print("Less checks ----> {0} ({1})".format(less_cell, less_cell_val))
    print("Fastest --------> {0} ({1})".format(fastest, fastest_val))
    print()

    RESULTS.append([map_name, shortest, less_cell, fastest])
    time.sleep(1)


def print_final_results():
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("%%           TOTAL              %%")
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print()
    print("    \tRoute \t Cells \t")
    print("Alg.\tLength\tChecked\t  Time")
    print("--------------------------------")
    print("{0}\t{1}\t{2}\t{3}".format("BFS", *BFS_ACC))
    print("{0}\t{1}\t{2}\t{3}".format("DFSR", *DFS_ACCR))
    print("{0}\t{1}\t{2}\t{3}".format("DFSL", *DFS_ACCL))
    print()
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("%%          RANKINGS            %%")
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print()
    print("                LESS")
    print("     SHORTEST  CHECKS  FASTEST")
    print("--------------------------------")

    shortests = []
    less_cells = []
    fastests = []
    for entry in RESULTS:
        shortests.append(entry[1])
        less_cells.append(entry[2])
        fastests.append(entry[3])
        print("{0}\t{1}\t{2}\t{3}".format(*entry))
    print("--------------------------------")
    print()

    short_rank = Counter(shortests).most_common(3)
    cells_rank = Counter(less_cells).most_common(3)
    fast_rank = Counter(fastests).most_common(3)

    print("\tSHORTEST ROUTE\t")
    print("--------------------------------")
    for i, entry in enumerate(short_rank):
        print("{0}º: {1} ({2})".format(i+1, *entry))
    print()

    print("\tLESS CELLS CHECKED")
    print("--------------------------------")
    for i, entry in enumerate(cells_rank):
        print("{0}º: {1} ({2})".format(i+1, *entry))
    print()

    print("\tFASTEST ALGORITHM")
    print("--------------------------------")
    for i, entry in enumerate(fast_rank):
        print("{0}º: {1} ({2})".format(i+1, *entry))
    print()


def main():
    maps = [["map1", [2, 2], [7, 2]],
            ["map2", [2, 2], [10, 7]],
            ["map3", [4, 10], [4, 14]],
            ["map4", [4, 10], [4, 14]],
            ["map5", [4, 15], [4, 9]],
            ["map6", [2, 2], [10, 17]],
            ["map7", [3, 9], [3, 15]],
            ["map8", [2, 2], [10, 17]],
            ["map9", [3, 9], [3, 15]],
            ["map10", [3, 9], [3, 15]],
            ["map11", [3, 15], [3, 9]]
            ]

    labs = [["lab1", [2, 2], [15, 15]]]

    for map in maps:
        do_compare(*map)

    print_final_results()


if __name__ == "__main__":
    main()

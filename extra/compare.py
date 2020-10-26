#! /usr/bin/env python

"""Comparison of algorithms.

Comparison of bfs, dfs (right and left handed), dijkstra and A* algorithms over
a list of maps. The comparison is made between the route lenght found, the
number of cells accessed over the map and the execution time.
"""

import os
import sys
import argparse
import time
from collections import Counter
from enum import Enum

from utils import CharMap, UserInputException, get_route, OUTPUT_MODE, Output
from bfs.bfs import bfs
from dfs.dfs import dfs
from dijkstra.dijkstra import dijkstra, CharMapCost
from astar.astar import astar
from astar.astar import CharMapCost as CharMapCost2

__author__ = "Pedro Arias Perez"


LOCAL_PATH = os.path.dirname(os.path.abspath(__file__)).split("extra")[0]
FILE_NAME = LOCAL_PATH + "maps/{0}/{0}.csv"

RESULTS = []
BFS_ACC = [0, 0, 0]
DFS_ACCR = [0, 0, 0]
DFS_ACCL = [0, 0, 0]
DIJK_ACC = [0, 0, 0]
A_ACC = [0, 0, 0]


class Algorithms(Enum):
    """Algorithms compared."""
    BFS = 0
    DFSr = 1
    DFSl = 2
    DIJK = 3
    ASTAR = 4

def run_bfs(map):
    """
    Execs bfs silenced (no output is printed) and registering start and end time.

    map: a map (CharMap)

    return: results: route length, number of cells accessed and time ([int, int, float])
    """
    sys.stdout = open(os.devnull, 'w')  # silence
    t0 = time.time()
    goalParentId = bfs(map)
    route = get_route(map.nodes, goalParentId)
    tf = time.time()
    sys.stdout = sys.__stdout__
    result = [len(route), map.n_checked, round((tf-t0), 5)]
    return result

def run_dfs(map, is_clockwise=True):
    """
    Execs dfs silenced (no output is printed) and registering start and end time.

    map: a map (CharMap)
    is_clockwise: right or left handed (bool)

    return: results: route length, number of cells accessed and time ([int, int, float])
    """
    sys.stdout = open(os.devnull, 'w')  # silence
    t0 = time.time()
    goalParentId = dfs(map, is_clockwise)
    route = get_route(map.nodes, goalParentId)
    tf = time.time()
    sys.stdout = sys.__stdout__
    result = [len(route), map.n_checked, round((tf-t0), 5)]
    return result

def run_dijkstra(map):
    """
    Execs dijkstra silenced (no output is printed) and registering start and end time.

    map: a map (CharMapCost)

    return: results: route length, number of cells accessed and time ([int, int, float])
    """
    sys.stdout = open(os.devnull, 'w')  # silence
    t0 = time.time()
    goalParentId = dijkstra(map)
    route = get_route(map.closed_nodes, goalParentId)
    tf = time.time()
    sys.stdout = sys.__stdout__
    result = [len(route), map.n_checked, round((tf-t0), 5)]
    return result

def run_astar(map):
    """
    Execs a* silenced (no output is printed) and registering start and end time.

    map: a map (CharMapCost)

    return: results: route length, number of cells accessed and time ([int, int, float])
    """
    sys.stdout = open(os.devnull, 'w')  # silence
    t0 = time.time()
    goalParentId = astar(map)
    route = get_route(map.closed_nodes, goalParentId)
    tf = time.time()
    sys.stdout = sys.__stdout__
    result = [len(route), map.n_checked, round((tf-t0), 5)]
    return result

def do_compare(map_name, start, end, only_uniform):
    """
    Compares the uninformed algorithms in a specific map and prints the partial results.

    map_name: the map name (str)
    start: start point ([int, int])
    end: end point ([int, int])
    only_uniform: true to only compare BFS and DFS (bool)
    """
    map = CharMap(FILE_NAME.format(map_name), start, end)

    results = []

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
    results.append(bfs_result)

    # time.sleep(1)
    map.reset()

    dfsr_result = run_dfs(map)
    print("{0}\t{1}\t{2}\t{3}".format("DFSr", *dfsr_result))
    DFS_ACCR[0] += dfsr_result[0]
    DFS_ACCR[1] += dfsr_result[1]
    DFS_ACCR[2] += round(dfsr_result[2], 5)
    results.append(dfsr_result)

    # time.sleep(1)
    map.reset()

    dfsl_result = run_dfs(map, False)
    print("{0}\t{1}\t{2}\t{3}".format("DFSl", *dfsl_result))
    DFS_ACCL[0] += dfsl_result[0]
    DFS_ACCL[1] += dfsl_result[1]
    DFS_ACCL[2] += round(dfsl_result[2], 5)
    results.append(dfsl_result)

    map.reset()
    # time.sleep(1)

    if not only_uniform:
        map_cost = CharMapCost(FILE_NAME.format(map_name), start, end)

        dijkstra_result = run_dijkstra(map_cost)
        print("{0}\t{1}\t{2}\t{3}".format("DIJK", *dijkstra_result))
        DIJK_ACC[0] += dijkstra_result[0]
        DIJK_ACC[1] += dijkstra_result[1]
        DIJK_ACC[2] += round(dijkstra_result[2], 5)
        results.append(dijkstra_result)

        map_cost.reset()
        # time.sleep(1)

        map_cost2 = CharMapCost2(FILE_NAME.format(map_name), start, end)

        astar_result = run_astar(map_cost2)
        print("{0}\t{1}\t{2}\t{3}".format("ASTAR", *astar_result))
        A_ACC[0] += astar_result[0]
        A_ACC[1] += astar_result[1]
        A_ACC[2] += round(astar_result[2], 5)
        results.append(astar_result)

        map_cost2.reset()
        # time.sleep(1)

    shortest, less_cell, fastest = get_best(results)

    print()
    print("Shortest -------> {0} ({1})".format(*shortest))
    print("Less checks ----> {0} ({1})".format(*less_cell))
    print("Fastest --------> {0} ({1})".format(*fastest))
    print()

    RESULTS.append([map_name, shortest[0], less_cell[0], fastest[0]])
    time.sleep(1)

def get_best(results):
    """
    Gets shortest route, less cells accessed and fastest algorithm.

    results: Nx3 matrix, being N number of algorithms compared. Each row is made up of route lenght (int), number of cells accessed (int) and execution time (float)

    return: [shortest alg (str), route lenght (int)], [less accessed alg (str), number of accesses (int)], [fastest alg (str), time (float)]
    """
    routes = [item[0] for item in results]  # get route lengths from results matrix
    cells = [item[1] for item in results]  # get number of accesses from results matrix
    times = [item[2] for item in results]  # get execution times from results matrix

    # get list of enums (alg) with min values and format it as csv
    shortest = ("".join(f"{i}, " for i in [Algorithms(i).name for i, val in enumerate(routes) if val == min(routes)])[:-2], min(routes))
    less_cell = ("".join(f"{i}, " for i in [Algorithms(i).name for i, val in enumerate(cells) if val == min(cells)])[:-2], min(cells))
    fastest = ("".join(f"{i}, " for i in [Algorithms(i).name for i, val in enumerate(times) if val == min(times)])[:-2], min(times))
    return shortest, less_cell, fastest

def print_final_results():
    """
    Prints final and accumulative results.
    """
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
    if DIJK_ACC:
        print("{0}\t{1}\t{2}\t{3}".format("DIJK", *DIJK_ACC))
    if A_ACC:
        print("{0}\t{1}\t{2}\t{3}".format("ASTAR", *A_ACC))
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


def main(only_uniform):
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
        do_compare(*map, only_uniform)

    print_final_results()


if __name__ == "__main__":
    # Command line argument parser, try: python3 compare.py -h
    parser = argparse.ArgumentParser(description="Algorithm Comparison.")
    parser.add_argument('-u', action='store_true', help='compare only uniform algorithms')
    args = parser.parse_args()

    main(args.u)

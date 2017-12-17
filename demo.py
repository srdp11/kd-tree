"""
    File name: demo.py
    License: MIT
    Author: Orlov Michael
    Date created: 03.10.2017
    Python Version: 3.5
    Description: demonstration of functionality of kd-tree
"""


import numpy as np

from kdtree import create
from visualization import visualize_2d_tree, visualize_2d_tree_by_levels
from algorithms import tracing_convex_hull_points, prune_tree, transform_tree
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import pickle

def check(points, templates):
    counts = [0 for x in templates]

    for point in points:
        belongs_to_convex_hull = point[1]

        idx = -1

        for i in range(len(templates)):
            founded = point[3].find(templates[i]) != -1

            if founded:
                idx = i
                counts[idx] += 1
                break

        if idx != -1 and belongs_to_convex_hull:
            return False, 0

    return True, counts


def test():
    points_num = [1000, 2000, 5000, 10000, 20000, 25000]
    templates = ['L R R R', 'R L L L', 'L L L L', 'R R R R']

    percents = []

    for num in points_num:
        size = (num, 2)

        data = np.random.uniform(0, 4, size)

        tree = create([x for x in map(tuple, data)], 2)

        points = tracing_convex_hull_points(tree)

        hull = ConvexHull(data)
        hull_indices = [x for x in hull.vertices]

        success, counts = check(points, templates)

        percent = sum(counts) / len(points) * 100
        percents.append(percent)

        print('========================')
        print("Points: " + str(num))
        print("hull size " + str(hull_indices.__len__()))
        print('success: ' + str(success))
        print("Summary removed: " + str(sum(counts)) + " from " + str(len(points)) + " (" + str(percent) + "%)")

    return points_num, percents


def convex_hull_test(data):
    ConvexHull(data)


def convex_hull_with_pruning(data):
    tree = create([x for x in map(tuple, data)], 2)
    pruned_tree = prune_tree(tree)

    ConvexHull([x.data for x in tree.level_order()])


if __name__ == '__main__':
    np.random.seed(12)

    size = (20, 2)

    data = np.random.uniform(0, 4, size)

    tree = create([x for x in map(tuple, data)], 2)
    # print(len([x for x in tree.level_order()]))
    # print("\n".join([str(x) for x in tree.level_order()]))

    # points_num, percents = test()
    #
    # plt.plot(points_num, percents)
    # plt.xlabel('points number')
    # plt.ylabel('points removed by algorithm, %')
    # plt.show()

    #pruned_tree = prune_tree(transform_tree(tree))

    # hull_original = ConvexHull(data)
    # hull_pruned = ConvexHull([x.data for x in pruned_tree.level_order()])
    #
    # hull_original_points = hull_original.points
    # hull_pruned_points = hull_pruned.points
    #
    # hull_original_points.sort(axis=0)
    # hull_pruned_points.sort(axis=0)
    #
    # print(len(hull_original_points))
    # print(len(hull_pruned_points))
    # print((hull_original_points == hull_pruned_points).all())

    #visualize_2d_tree(tree)
    visualize_2d_tree_by_levels(tree)
    #print(pruned_tree)
    #visualize_2d_tree_by_levels(pruned_tree)
    plt.show()


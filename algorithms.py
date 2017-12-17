from collections import deque
from scipy.spatial import ConvexHull
from kdtree import Node


def color2side(color):
    res = 'U'

    if color == 'r':
        res = 'L'
    elif color == 'b':
        res = 'R'

    return res


def transform_tree(node, curr_axis=0, up_left_direction=True):
    next_axis = (curr_axis + 1) % 2

    left = None
    right = None

    if curr_axis == 0 and up_left_direction:
        if node.left:
            left = transform_tree(node.left, next_axis, True)

        if node.right:
            right = transform_tree(node.right, next_axis, False)

    elif curr_axis == 0 and not up_left_direction:
        if node.left:
            right = transform_tree(node.left, next_axis, True)

        if node.right:
            left = transform_tree(node.right, next_axis, False)

    elif curr_axis == 1 and up_left_direction:
        if node.left:
            left = transform_tree(node.left, next_axis, False)

        if node.right:
            right = transform_tree(node.right, next_axis, True)

    elif curr_axis == 1 and not up_left_direction:
        if node.left:
            right = transform_tree(node.left, next_axis, False)

        if node.right:
            left = transform_tree(node.right, next_axis, True)

    return Node(node.data, left, right)


def create_paths(tree):
    result = []

    def iter(node, path):
        if node:
            result.append((node, path))

        if node.left:
            iter(node.left, path + ' L')

        if node.right:
            iter(node.right, path + ' R')

    iter(tree, '')
    return result


def tracing_convex_hull_points(tree):
    paths = create_paths(transform_tree(tree))
    points = [x[0].data for x in paths]

    hull = ConvexHull(points)
    hull_indices = [x for x in hull.vertices]

    results = []

    for i in range(len(points)):
        if i in hull_indices:
            path = '[' + str(i) + ']'
        else:
            path = '(' + str(i) + ')'

        results.append((i, i in hull_indices, points[i], paths[i][1]))

    return results

templates = ['LRRR', 'RLLL', 'LLLL', 'RRRR']


def prune_tree(tree, path=''):
    if path in templates:
        return None

    left = None
    right = None

    if tree.left:
        left = prune_tree(tree.left, path + 'L')

    if tree.right:
        right = prune_tree(tree.right, path + 'R')

    return Node(tree.data, left, right)

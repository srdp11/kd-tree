from collections import deque
from scipy.spatial import ConvexHull


def create_paths(tree):
    nodes_deque = deque()
    nodes_deque.append({'node': tree, 'path': ''})

    nodes_with_paths = []

    while nodes_deque:
        node = nodes_deque.popleft()

        nodes_with_paths.append(node)

        if node['node'].left:
            nodes_deque.append({'node': node['node'].left, 'path': node['path'] + ' L'})

        if node['node'].right:
            nodes_deque.append({'node': node['node'].right, 'path': node['path'] + ' R'})

    return nodes_with_paths


def tracing_convex_hull_points(tree):
    paths = create_paths(tree)
    points = [node_path_pair['node'].data for node_path_pair in paths]

    hull = ConvexHull(points)
    hull_indices = [x for x in hull.vertices]

    results = []

    for i in range(len(points)):
        if i in hull_indices:
            path = '[' + str(i) + ']'
        else:
            path = '(' + str(i) + ')'

        results.append(path + paths[i]['path'])

    return results

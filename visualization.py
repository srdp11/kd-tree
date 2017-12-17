"""
    File name: visualization.py
    License: MIT
    Author: Orlov Michael
    Date created: 12.10.2017
    Python Version: 3.5
    Description: visualization of kd-tree by levels
"""
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from math import floor
from discrete_slider import DiscreteSlider
from kdtree import Node
import numpy as np
from algorithms import transform_tree


def calculate_vector_coordinates(x, y):
    return (x[0], y[0]), (x[1] - x[0], y[1] - y[0])


def visualize_bound(bound_coordinate, curr_axis, up_left_direction, axes, x_lims, y_lims, width, color):
    bound_point = [bound_coordinate, bound_coordinate]

    if curr_axis == 0:
        x = bound_point
        y = y_lims
    else:
        x = x_lims
        y = bound_point

    if curr_axis == 0:
        y = sorted(y, reverse=not up_left_direction)
    else:
        x = sorted(x, reverse=up_left_direction)

    start_point, end_point = calculate_vector_coordinates(x, y)

    axes.quiver(*start_point, *end_point, angles='xy', scale_units='xy', scale=1, color=color)


def draw_area(axes, x_lims, y_lims, color):
    axes.add_patch(
        Rectangle((x_lims[0], y_lims[0]),
                  x_lims[1] - x_lims[0], y_lims[1] - y_lims[0],
                  color=color, alpha=0.4))


def visualize_2d_tree(tree):
    xlim, ylim = calculate_lims(tree)

    axes = plt.gca()

    axes.set_xlim(xlim)
    axes.set_ylim(ylim)

    visualization_tree = create_visualization_tree(tree)

    for node in visualization_tree.level_order():
        x_lims = node.data['x_lims']
        y_lims = node.data['y_lims']
        color = node.data['color']

        if not node:
            draw_area(axes, x_lims, y_lims, color)
        else:
            point = node.data['point']
            curr_axis = node.data['curr_axis']
            up_left_direction = node.data['up_left_direction']

            visualize_bound(point[curr_axis], curr_axis, up_left_direction,
                            axes, x_lims, y_lims, -1, color)

            axes.plot(*point, 'g*')

    plt.show()


def split_tree_by_levels(tree):
    nodes_info_map = {}

    def iter(node, level):
        if node:
            if level in nodes_info_map.keys():
                nodes_info_map[level].append(node.data)
            else:
                nodes_info_map[level] = [node.data]

        if node.left:
            iter(node.left, level + 1)

        if node.right:
            iter(node.right, level + 1)

    iter(tree, 1)

    return nodes_info_map


def calculate_lims(tree):
    if not tree:
        return None

    xmin = tree.data[0]
    xmax = tree.data[0]

    ymin = tree.data[1]
    ymax = tree.data[1]

    for node in tree.level_order():
        xmin = min(xmin, node.data[0])
        xmax = max(xmax, node.data[0])

        ymin = min(ymin, node.data[1])
        ymax = max(ymax, node.data[1])

    return (xmin - 0.3, xmax + 0.3), (ymin - 0.3, ymax + 0.3)


def plot_points(points, visualize_bounds, axes, style):
    for point in points:

        if len(point['point']) == 0:
            continue

        axes.plot(point['point'][0], point['point'][1], style)

        if visualize_bounds:
            point_data = point['point']
            curr_axis = point['curr_axis']
            up_left_direction = point['up_left_direction']
            x_lims = point['x_lims']
            y_lims = point['y_lims']
            color = point['color']

            visualize_bound(point_data[curr_axis], curr_axis, up_left_direction,
                            axes, x_lims, y_lims, -1, color)


def visualize_2d_tree_by_levels(tree):
    data = np.array([x.data for x in tree.level_order()])

    plt.subplots_adjust(left=0.15, bottom=0.25)

    axes_nodes = plt.axes()

    xlim, ylim = calculate_lims(tree)

    axes_nodes.set_xlim(xlim)
    axes_nodes.set_ylim(ylim)

    visualization_tree = create_visualization_tree(tree)

    nodes_info = split_tree_by_levels(visualization_tree)

    axes = plt.axes([0.15, 0.1, 0.2, 0.03])

    slider_levels = DiscreteSlider(axes, 'Levels number', 0, tree.height, valinit=0, valfmt='%d')

    axes_level_nodes = plt.axes()

    hull = ConvexHull(data)

    def update(value):
        axes_level_nodes.cla()

        for simplex in hull.simplices:
            plt.plot(data[simplex, 0], data[simplex, 1], 'k-')

        curr_level = floor(value)

        for i in range(1, max(nodes_info.keys()) + 1):
            if i < curr_level + 1:
                plot_points(nodes_info[i], True, axes_level_nodes, 'b*')
            else:
                plot_points(nodes_info[i], False, axes_level_nodes, 'r*')

        axes_nodes.set_xlim(xlim)
        axes_nodes.set_ylim(ylim)

        plt.draw()

    slider_levels.on_changed(update)
    plt.show()


def create_visualization_tree(tree):
    def create_visualization_node(node, x_lims, y_lims, curr_axis=0, is_left_node=True, color='r'):
        if not node:
            return Node({'point': tuple(), 'x_lims': x_lims, 'y_lims': y_lims,
                         'color': color}, None, None)

        x_lims_left = (x_lims[0], node.data[0])
        x_lims_right = (node.data[0], x_lims[1])

        y_lims_left = (y_lims[0], node.data[1])
        y_lims_right = (node.data[1], y_lims[1])

        if is_left_node:
            left_side_color = 'r'
            right_side_color = 'b'
        else:
            left_side_color = 'b'
            right_side_color = 'r'

        left_node_flag = curr_axis == 0

        if left_node_flag:
            next_left_x_lims = x_lims_left
            next_right_x_lims = x_lims_right
            next_left_y_lims = y_lims
            next_right_y_lims = y_lims
        else:
            next_left_x_lims = x_lims
            next_right_x_lims = x_lims
            next_left_y_lims = y_lims_left
            next_right_y_lims = y_lims_right

        next_axis = (curr_axis + 1) % 2

        left = create_visualization_node(node.left, next_left_x_lims, next_left_y_lims,
                                         next_axis, left_node_flag, left_side_color)
        right = create_visualization_node(node.right, next_right_x_lims, next_right_y_lims,
                                          next_axis, not left_node_flag, right_side_color)

        return Node({'point': node.data, 'up_left_direction': is_left_node, 'curr_axis': curr_axis,
                     'x_lims': x_lims, 'y_lims': y_lims, 'color': color},
                    left, right)

    xlim, ylim = calculate_lims(tree)

    return create_visualization_node(tree, xlim, ylim)

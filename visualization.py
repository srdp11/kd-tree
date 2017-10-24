"""
    File name: visualization.py
    License: MIT
    Author: Orlov Michael
    Date created: 12.10.2017
    Python Version: 3.5
    Description: visualization of kd-tree by levels
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from math import floor
from discrete_slider import DiscreteSlider


def visualize_2d_tree(tree):
    def visualize(node, axes, curr_axis, x_lims, y_lims, width, color, up_left_direction):
        def vector_coords(x, y):
            return (x[0], y[0]), (x[1] - x[0], y[1] - y[0])

        def visualize_bound():
            bound_coords = [node.data[curr_axis], node.data[curr_axis]]

            if curr_axis == 0:
                x = bound_coords
                y = y_lims
            else:
                x = x_lims
                y = bound_coords

            if curr_axis == 0:
                y = sorted(y, reverse=not up_left_direction)
            else:
                x = sorted(x, reverse=up_left_direction)

            start_point, end_point = vector_coords(x, y)

            axes.quiver(*start_point, *end_point, angles='xy', scale_units='xy', scale=1, color=color)

        def visualize_side(node, curr_axis, x_lims, y_lims, width, color, up_left_direction):
            if node.is_leaf:
                axes.add_patch(
                    Rectangle((x_lims[0], y_lims[0]),
                              x_lims[1] - x_lims[0], y_lims[1] - y_lims[0],
                              color=color, alpha=0.4))
            elif node:
                visualize(node, axes, curr_axis, x_lims, y_lims, width, color, up_left_direction)

        visualize_bound()

        x_lims_left = (x_lims[0], node.data[0])
        x_lims_right = (node.data[0], x_lims[1])

        y_lims_left = (y_lims[0], node.data[1])
        y_lims_right = (node.data[1], y_lims[1])

        left_side_flag = curr_axis == 0
        right_side_flag = not left_side_flag

        if up_left_direction:
            left_side_color = 'r'
            right_side_color = 'b'
        else:
            left_side_color = 'b'
            right_side_color = 'r'

        next_axis = (curr_axis + 1) % 2
        width -= 1

        if curr_axis == 0:
            visualize_side(node.left, next_axis, x_lims_left, y_lims, width, left_side_color, left_side_flag)
            visualize_side(node.right, next_axis, x_lims_right, y_lims, width, right_side_color, right_side_flag)
        else:
            visualize_side(node.left, next_axis, x_lims, y_lims_left, width, left_side_color, left_side_flag)
            visualize_side(node.right, next_axis, x_lims, y_lims_right, width, right_side_color, right_side_flag)

    # TODO: calculate xlims and ylims
    axes = plt.gca()

    axes.set_xlim([-5, 5])
    axes.set_ylim([-5, 5])

    visualize(tree, axes, 0, axes.get_xlim(), axes.get_ylim(), tree.height, 'r', True)

    plt.show()


def split_tree_by_levels(tree):
    nodes_info_map = {}
    leaf_points = []

    def iter(node, level):
        if not node.is_leaf:
            if level in nodes_info_map.keys():
                nodes_info_map[level].append(node.data)
            else:
                nodes_info_map[level] = [node.data]
        else:
            leaf_points.append(node.data)

        if node.left:
            iter(node.left, level + 1)

        if node.right:
            iter(node.right, level + 1)

    iter(tree, 1)

    return nodes_info_map, leaf_points


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


def plot_points(axes, points, style):
    axes.plot([node_info[0] for node_info in points],
              [node_info[1] for node_info in points],
              style)


def visualize_2d_tree_by_levels(tree):
    nodes_info, leaf_points = split_tree_by_levels(tree)

    plt.subplots_adjust(left=0.15, bottom=0.25)

    axes_nodes = plt.axes()

    xlim, ylim = calculate_lims(tree)

    axes_nodes.set_xlim(xlim)
    axes_nodes.set_ylim(ylim)

    for node in tree.level_order():
        axes_nodes.plot(node.data[0], node.data[1], 'r*')

    axes = plt.axes([0.15, 0.1, 0.2, 0.03])

    slider_levels = DiscreteSlider(axes, 'Levels number', 0, tree.height, valinit=0, valfmt='%d')

    axes_level_nodes = plt.axes()

    def update(value):
        axes_level_nodes.cla()

        curr_level = floor(value)

        plot_points(axes_level_nodes, leaf_points, 'r*')

        for i in range(1, max(nodes_info.keys()) + 1):
            if i < curr_level + 1:
                plot_points(axes_level_nodes, nodes_info[i], 'b*')
            else:
                plot_points(axes_level_nodes, nodes_info[i], 'r*')

        axes_nodes.set_xlim(xlim)
        axes_nodes.set_ylim(ylim)

        plt.draw()

    slider_levels.on_changed(update)

    plt.show()

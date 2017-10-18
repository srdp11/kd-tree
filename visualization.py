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

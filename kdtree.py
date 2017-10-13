from collections import deque
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class Node(object):
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def __repr__(self):
        return '<%(cls)s - %(data)s>' % \
               dict(cls=self.__class__.__name__, data=repr(self.data))

    def __nonzero__(self):
        return self.data is not None

    __bool__ = __nonzero__

    @property
    def is_leaf(self):
        return (not self.data) or (not self.left and not self.right)

    @property
    def height(self):
        if self.is_leaf:
            return 1
        else:
            return 1 + max(self.left.height, self.right.height)

    def children(self):
        if self.left and self.left.data is not None:
            yield self.left, 0

        if self.right and self.right.data is not None:
            yield self.right, 1

    @property
    def is_balanced(self):
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0

        if abs(left_height - right_height) > 1:
            return False

        return all(c.is_balanced for c, _ in self.children())

    def level_order(self):
        nodes_deque = deque()
        nodes_deque.append(self)

        while nodes_deque:
            node = nodes_deque.popleft()

            yield node

            if node.left:
                nodes_deque.append(node.left)

            if node.right:
                nodes_deque.append(node.right)

    def __median_split__(points, axis=0):
        points = list(points)
        points.sort(key=lambda point: point[axis])
        median = len(points) // 2

        return points[:median], points[median], points[median + 1:]

    @staticmethod
    def create(points, dimension, axis=0, splitter=__median_split__):
        if points is None or not points:
            return Node()

        left_points, loc, right_points = splitter(points, axis)

        left = Node.create(left_points, dimension, axis=(axis + 1) % dimension)
        right = Node.create(right_points, dimension, axis=(axis + 1) % dimension)
        return Node(loc, left, right)

    # TODO: move to separate class
    @staticmethod
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

from collections import deque


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

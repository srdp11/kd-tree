"""
    File name: kdtree.py
    License: MIT
    Author: Orlov Michael
    Date created: 03.10.2017
    Python Version: 3.5
    Description: python implementation of a kd-tree
"""


from collections import deque
from splitters import median_split


class Node(object):
    """
    A Node in a kd-tree

    A tree is represented by its root node, and every node represents
    its subtree.
    """

    def __init__(self, data=None, left=None, right=None):
        """
        Creates a new node for a kd-tree
        """

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
        """
        Returns True if a Node has no subnodes

        >>> Node().is_leaf
        True

        >>> Node(1, left=Node(2)).is_leaf
        False
        """

        return (not self.data) or (all(not bool(c) for c, p in self.children))

    @property
    def height(self):
        """
        Returns height of the (sub)tree, without considering
        empty leaf-nodes

        >>> create().height()
        0

        >>> create([ (1, 2) ]).height()
        1

        >>> create([ (1, 2), (2, 3) ]).height()
        2
        """
        try:
            if self.is_leaf:
                return 1
            else:
                return 1 + max(self.left.height, self.right.height)
        except AttributeError:
            return 0

    def inorder(self):
        """ iterator for nodes: left, root, right """

        if not self:
            return

        if self.left:
            for x in self.left.inorder():
                yield x

        yield self

        if self.right:
            for x in self.right.inorder():
                yield x

    def rebalance(self):
        """
        Returns the (possibly new) root of the rebalanced tree
        """

        return create([x.data for x in self.inorder()], dimension=2)

    @property
    def children(self):
        """
        Returns an iterator for the non-empty children of the Node
        The children are returned as (Node, pos) tuples where pos is 0 for the
        left subnode and 1 for the right.

        >>> len(list(create(dimensions=2).children))
        0

        >>> len(list(create([ (1, 2) ]).children))
        0

        >>> len(list(create([ (2, 2), (2, 1), (2, 3) ]).children))
        2
        """

        if self.left and self.left.data is not None:
            yield self.left, 0

        if self.right and self.right.data is not None:
            yield self.right, 1

    @property
    def is_balanced(self):
        """
        Returns True if the (sub)tree is balanced

        The tree is balanced if the heights of both subtrees differ at most by 1
        """

        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0

        if abs(left_height - right_height) > 1:
            return False

        return all(c.is_balanced for c, _ in self.children())

    def level_order(self):
        """
        Returns an iterator over the tree in level-order
        """

        nodes_deque = deque()
        nodes_deque.append(self)

        while nodes_deque:
            node = nodes_deque.popleft()

            yield node

            if node.left:
                nodes_deque.append(node.left)

            if node.right:
                nodes_deque.append(node.right)


def create(points, dimension, axis=0, splitter=median_split):
    """
    Creates a kd-tree from a list of points

    All points in the list must be of the same dimensionality.

    If no point_list is given, an empty tree is created.

    Axis is the axis on which the root-node should split.

    Splitter is a condition that splits the sample into two parts.
    """

    if points is None or not points:
        return Node()

    left_points, loc, right_points = splitter(points, axis)

    left = create(left_points, dimension, axis=(axis + 1) % dimension)
    right = create(right_points, dimension, axis=(axis + 1) % dimension)
    return Node(loc, left, right)

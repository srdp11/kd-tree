import unittest
import pickle
import logging
import scipy
import numpy as np

import kdtree
import visualization
from algorithms import transform_tree, prune_tree, create_paths
from visualization import visualize_2d_tree_by_levels


def get_test_points():
    source = [(1.8849191130000564, 3.2646731921841075),
              (1.239590337960117, 2.6858105808480106),
              (2.8104894210209852, 1.3102779050536921),
              (1.0532600607405387, 2.134957573521191),
              (1.1583471341222142, 2.9325039104506825),
              (3.602859416468049, 0.13368571050537836),
              (3.0699026024819549, 3.3000370128590939),
              (0.0090369340740541482, 2.0849041088811715),
              (1.1353134118317834, 2.4243327374353156),
              (0.058299849941678694, 3.6749880323995399),
              (1.3385901164242231, 3.9122323160660755),
              (3.0725366162576893, 0.6428670125022804),
              (3.8277973451004672, 0.54883728542430577),
              (2.4983284469414095, 3.8012540987981014),
              (3.7769005442121686, 3.4109421644371398),
              (0.54084071347646745, 0.46509206960675931),
              (0.61665136951868949, 2.960198786061619),
              (3.058241801355515, 0.083239191808264668),
              (2.2081505330582663, 1.9415096546508388)]

    return source


def get_transformed_points():
    transformed = [(1.8849191130000564, 3.2646731921841075),
                   (1.239590337960117, 2.6858105808480106),
                   (2.8104894210209852, 1.3102779050536921),
                   (1.0532600607405387, 2.134957573521191),
                   (1.1583471341222142, 2.9325039104506825),
                   (3.602859416468049, 0.13368571050537836),
                   (3.0699026024819549, 3.3000370128590939),
                   (0.0090369340740541482, 2.0849041088811715),
                   (1.1353134118317834, 2.4243327374353156),
                   (0.058299849941678694, 3.6749880323995399),
                   (1.3385901164242231, 3.9122323160660755),
                   (3.0725366162576893, 0.6428670125022804),
                   (3.8277973451004672, 0.54883728542430577),
                   (2.4983284469414095, 3.8012540987981014),
                   (3.7769005442121686, 3.4109421644371398),
                   (0.54084071347646745, 0.46509206960675931),
                   (0.61665136951868949, 2.960198786061619),
                   (3.058241801355515, 0.083239191808264668),
                   (2.2081505330582663, 1.9415096546508388)]

    return transformed


def load_test_tree():
    file_with_tree = open("test_tree.data", "rb")
    tree = pickle.load(file_with_tree)
    file_with_tree.close()

    return tree


def are_equal_trees(lhs, rhs):
    lhs_nodes = [x for x in lhs.level_order()]
    rhs_nodes = [x for x in rhs.level_order()]

    assert len(lhs_nodes) == len(rhs_nodes)

    for i in range(len(lhs_nodes)):
        if not are_equal_nodes(lhs_nodes[i], rhs_nodes[i]):
            return False

    return True


def are_equal_nodes(lhs, rhs):
    lhs_data = lhs.data
    rhs_data = rhs.data

    if len(lhs_data['point']) == 0 and len(rhs_data['point']) == 0:
        are_equal_points = True
    else:
        are_equal_points = are_equal_double_tuple(lhs_data['point'], rhs_data['point'])

    return are_equal_points and lhs_data['color'] == rhs_data['color'] and\
        are_equal_double_tuple(lhs_data['x_lims'], rhs_data['x_lims']) and\
        are_equal_double_tuple(lhs_data['y_lims'], rhs_data['y_lims'])


def are_equal_double_tuple(lhs, rhs, eps=1e-10):
    return abs(lhs[0] - rhs[0]) < eps and abs(lhs[1] - rhs[1]) < eps


def are_equal_double_lists(lhs, rhs, eps=1e-10):
    if len(lhs) != len(rhs):
        return False

    for i in range(len(lhs)):
        if abs(lhs[i][0] - rhs[i][0]) >= eps or abs(lhs[i][1] - rhs[i][1]) >= eps:
            return False

    return True


class TestTree(unittest.TestCase):

    # def setUp(self):
    #     self.log = logging.getLogger("Logger")

    def test_visualization_tree(self):
        tree = kdtree.create(points=get_test_points(), dimension=2)

        visualization_tree = visualization.create_visualization_tree(tree)
        test_tree = load_test_tree()

        self.assertTrue(are_equal_trees(visualization_tree, test_tree))

    # def test_transform_tree(self):
    #     tree = kdtree.create(points=get_test_points(), dimension=2)
    #
    #     transformed_data = [x.data for x in transform_tree(tree).level_order()]
    #     transformed_test_data = get_transformed_points()
    #
    #     self.assertEqual(len(transformed_test_data), len(transformed_data))
    #
    #     for i in range(len(transformed_data)):
    #         self.assertTrue(are_equal_double_tuple(transformed_test_data[i], transformed_data[i]))

    def test_foo(self):
        tree = transform_tree(kdtree.create(points=get_test_points(), dimension=2))

        #print("\n".join([str(x) for x in create_paths(tree)]))

        # for x in visualization_tree.level_order():
        #     print(x.data['point'])

        #assert False

    def test_pruned_tree_hull(self):
        np.random.seed(12)
        points_count = 20

        points = generate_points(points_count)

        source_tree = transform_tree(kdtree.create([x for x in map(tuple, points)], 2))
        pruned_tree = prune_tree(source_tree)

        hull_source_ndarray = points[get_hull_indices(points)]
        hull_source = [tuple(hull_source_ndarray[i].tolist()) for i in range(len(hull_source_ndarray))]

        hull_tree = create_convex_hull(source_tree)
        hull_pruned_tree = create_convex_hull(pruned_tree)

        sorted(hull_source, key=lambda x: (x[0], x[1]))
        sorted(hull_tree, key=lambda x: (x[0], x[1]))
        sorted(hull_pruned_tree, key=lambda x: (x[0], x[1]))

        self.assertTrue(are_equal_double_lists(hull_source, hull_tree))
        self.assertTrue(are_equal_double_lists(hull_source, hull_pruned_tree))
        self.assertTrue(are_equal_double_lists(hull_tree, hull_pruned_tree))


def print_source_and_pruned(source_tree, pruned_tree):
    source_tree_data = [x for x in source_tree.level_order()]
    pruned_tree_data = [x for x in pruned_tree.level_order()]

    print("source tree: {}".format(len(source_tree_data)))
    print("\n".join([str(x) for x in source_tree_data]))

    print("--------------------------------------------------------")

    print("pruned tree: {}".format(len(pruned_tree_data)))
    print("\n".join([str(x) for x in pruned_tree_data]))


def generate_points(points_count):
    size = (points_count, 2)
    return np.random.uniform(0, 4, size)


def create_convex_hull(tree):
    data = np.array([x.data for x in tree.level_order()], dtype='double')

    convex_hull_list = data[get_hull_indices(data)]

    result = [tuple(convex_hull_list[i].tolist()) for i in range(len(convex_hull_list))]

    return result


def get_hull_indices(data):
    hull = scipy.spatial.ConvexHull(data)
    return hull.vertices

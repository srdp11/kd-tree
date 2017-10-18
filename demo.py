import numpy as np

from kdtree import create
from visualization import visualize_2d_tree


if __name__ == '__main__':
    np.random.seed(12)

    size = (18, 2)

    data = np.random.uniform(0, 4, size)

    tree = create([x for x in map(tuple, data)], 2)

    visualize_2d_tree(tree)

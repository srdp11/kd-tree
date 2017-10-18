"""
    File name: splitters.py
    License: MIT
    Author: Orlov Michael
    Date created: 18.10.2017
    Python Version: 3.5
    Description: set of functions for splitting data in each node of kd-tree
"""


def median_split(points, axis=0):
    points = list(points)
    points.sort(key=lambda point: point[axis])
    median = len(points) // 2

    return points[:median], points[median], points[median + 1:]

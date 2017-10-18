def median_split(points, axis=0):
    points = list(points)
    points.sort(key=lambda point: point[axis])
    median = len(points) // 2

    return points[:median], points[median], points[median + 1:]

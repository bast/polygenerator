"""
Generates random simple polygons.

The generated polygon is made to fit the bounding box (0.0, 0.0) ... (1.0, 1.0)
and you can then scale and translate it to where you need it.
"""


import random
import math
import sys
from collections import defaultdict


__all__ = ["random_polygon", "random_convex_polygon", "random_star_shaped_polygon"]
__version__ = "0.2.0"


def recombine_edges(edges):
    d = defaultdict(set)

    for (a, b) in edges:
        assert a != b, "edge cannot start and end at same vertex"
        d[a].add(b)
        d[b].add(a)

    # every vertex should appear exactly twice
    assert all([len(v) == 2 for (_, v) in d.items()]), "the edges do not form a cycle"

    polygon = []

    # we start with the smallest one
    first_index = sorted(d.keys())[0]
    polygon.append(first_index)

    last_index = polygon[-1]
    while True:
        next_index = d[last_index].pop()

        # we need to remove this also from the other vertex
        # to make sure we don't loop right back
        d[next_index].remove(last_index)

        if next_index == first_index:
            break
        polygon.append(next_index)
        last_index = next_index

    return polygon


def orientation(u, v, w) -> float:
    uw_x = u[0] - w[0]
    uw_y = u[1] - w[1]

    vw_x = v[0] - w[0]
    vw_y = v[1] - w[1]

    return uw_x * vw_y - uw_y * vw_x


def projections_intersect(a, b, c, d) -> bool:
    if max(a[0], b[0]) < min(c[0], d[0]):
        return False

    if max(c[0], d[0]) < min(a[0], b[0]):
        return False

    if max(a[1], b[1]) < min(c[1], d[1]):
        return False

    if max(c[1], d[1]) < min(a[1], b[1]):
        return False

    return True


def segments_cross(a, b, c, d) -> bool:
    epsilon = sys.float_info.epsilon
    if abs(orientation(a, b, c)) < epsilon and abs(orientation(a, b, d)) < epsilon:
        # segments are collinear
        # check whether both x and y projections intersect
        return projections_intersect(a, b, c, d)
    else:
        # segments are not collinear
        # FIXME: not handling the case where segments touch "in T shape"
        # if the other two points are both on the same side, segments do not cross
        if orientation(a, b, c) * orientation(a, b, d) > 0.0:
            return False
        if orientation(c, d, a) * orientation(c, d, b) > 0.0:
            return False
    return True


def ordered(i, j):
    if i > j:
        return (j, i)
    else:
        return (i, j)


def generate_random_lists(num_points):
    xs = [random.uniform(0.0, 1.0) for _ in range(num_points)]
    ys = [random.uniform(0.0, 1.0) for _ in range(num_points)]
    return xs, ys


def sort_and_divide(l):
    l = sorted(l)

    l_without_endpoints = l[1:-1]

    n = len(l_without_endpoints)
    indices = range(n)
    indices1 = set(random.sample(indices, k=(n // 2)))
    indices2 = set(indices).difference(indices1)

    indices1_middle = list(map(lambda i: l[i + 1], indices1))
    indices2_middle = list(map(lambda i: l[i + 1], indices2))

    l1 = [l[0]] + indices1_middle + [l[-1]]
    l2 = [l[0]] + indices2_middle + [l[-1]]

    return l1, l2


def get_vector_elements(l1, l2):
    vec = []
    for (a, b) in zip(l1, l1[1:]):
        vec.append(b - a)
    for (a, b) in zip(l2, l2[1:]):
        vec.append(a - b)
    return vec


def angle(v):
    (x, y) = v
    return math.atan2(y, x)


def get_bbox(points):
    huge = sys.float_info.max
    x_min = huge
    x_max = -huge
    y_min = huge
    y_max = -huge
    for (x, y) in points:
        x_min = min(x_min, x)
        x_max = max(x_max, x)
        y_min = min(y_min, y)
        y_max = max(y_max, y)
    return x_min, x_max, y_min, y_max


def polygon_from_vectors(vs):
    xs = [0.0]
    ys = [0.0]
    for (vx, vy) in vs[:-1]:
        xs.append(xs[-1] + vx)
        ys.append(ys[-1] + vy)
    return list(zip(xs, ys))


def fit_to_bbox(points):
    x_min, x_max, y_min, y_max = get_bbox(points)

    scale_x = 1.0 / (x_max - x_min)
    scale_y = 1.0 / (y_max - y_min)

    return [((x - x_min) * scale_x, (y - y_min) * scale_y) for (x, y) in points]


def random_convex_polygon(num_points):
    """
    According to https://stackoverflow.com/a/47358689.
    """
    assert num_points > 2

    xs, ys = generate_random_lists(num_points)

    x1, x2 = sort_and_divide(xs)
    y1, y2 = sort_and_divide(ys)

    vx = get_vector_elements(x1, x2)
    vy = get_vector_elements(y1, y2)

    random.shuffle(vy)
    vs = list(zip(vx, vy))

    vs_sorted = sorted(vs, key=angle)

    polygon = polygon_from_vectors(vs_sorted)

    if polygon_is_clockwise(polygon):
        polygon = list(reversed(polygon))

    return fit_to_bbox(polygon)


def random_star_shaped_polygon(num_points):
    assert num_points > 2

    angles = [random.uniform(0.0, math.pi * 2.0) for _ in range(num_points)]

    polygon = []
    for angle in sorted(angles):
        r = random.uniform(0.2, 1.0)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        polygon.append((x, y))

    if polygon_is_clockwise(polygon):
        polygon = list(reversed(polygon))

    return fit_to_bbox(polygon)


def find_intersecting_edges(edge, edges, points, only_first):
    intersecting_edges = []
    (a, b) = edge
    pa = points[a]
    pb = points[b]
    for (c, d) in edges:
        if not a in (c, d):
            if not b in (c, d):
                pc = points[c]
                pd = points[d]
                if segments_cross(pa, pb, pc, pd):
                    intersecting_edges.append((c, d))
                    if only_first:
                        break
    return intersecting_edges


def edges_are_connected(edges) -> bool:
    d = defaultdict(set)
    for (a, b) in edges:
        assert a != b, "edge cannot start and end at same vertex"
        d[a].add(b)
        d[b].add(a)

    if not all([len(v) == 2 for (_, v) in d.items()]):
        return False

    vertices_to_visit = set(d.keys())
    vertices_visited = set()

    # start somewhere
    v = list(d.keys())[0]

    while True:
        vertices_visited.add(v)
        a = d[v].pop()
        b = d[v].pop()
        if a in vertices_visited and b in vertices_visited:
            break
        if not a in vertices_visited:
            v = a
        if not b in vertices_visited:
            v = b

    return vertices_to_visit == vertices_visited


def test_edges_are_connected():
    edges = {
        (0, 1),
        (1, 2),
        (2, 0),
    }
    assert edges_are_connected(edges)

    edges = {
        (0, 1),
        (1, 2),
        (2, 0),
        (5, 6),
        (6, 7),
        (7, 5),
    }
    assert not edges_are_connected(edges)


def no_edges_intersect(polygon) -> bool:
    num_points = len(polygon)

    edges = set()
    for i in range(num_points):
        edges.add((i, (i + 1) % num_points))

    for (a, b) in edges:
        pa = polygon[a]
        pb = polygon[b]
        for (c, d) in edges:
            if a not in [c, d]:
                if b not in [c, d]:
                    pc = polygon[c]
                    pd = polygon[d]
                    if segments_cross(pa, pb, pc, pd):
                        return False
    return True


def polygon_is_clockwise(polygon) -> bool:
    num_points = len(polygon)
    s = 0.0
    for i in range(num_points):
        j = (i + 1) % num_points
        s += (polygon[j][0] - polygon[i][0]) * (polygon[j][1] + polygon[i][1])
    return s > 0.0


def random_polygon(num_points):
    """
    "repair" random sequence by 2-opt moves.
    Auer, Held, "RPG - Heuristics for the Generation of Random Polygons", 1996

    Algorithms with better scaling exist but this was good enough for me.
    """
    assert num_points > 2

    points = [
        (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)) for _ in range(num_points)
    ]

    edges_to_check = set()
    for i in range(num_points):
        edges_to_check.add(ordered(i, (i + 1) % num_points))

    non_intersecting_edges = set()
    while len(edges_to_check) > 0:
        (a, b) = edges_to_check.pop()
        intersecting_edges = find_intersecting_edges(
            (a, b), edges_to_check, points, only_first=True
        )

        if intersecting_edges == []:
            non_intersecting_edges.add(ordered(a, b))
        else:
            (c, d) = intersecting_edges[0]
            edges_to_check.remove((c, d))

            # don't split the polygon into two
            graph = edges_to_check.union(non_intersecting_edges)
            graph.add(ordered(c, a))
            graph.add(ordered(d, b))
            if edges_are_connected(graph):
                new_edges = [ordered(c, a), ordered(d, b)]
            else:
                new_edges = [ordered(c, b), ordered(d, a)]

            # check whether a new edge intersects with an edge which we have
            # previously found as non-intersecting
            for edge in new_edges:
                edges_to_check.add(edge)
                for intersecting_edge in find_intersecting_edges(
                    edge, non_intersecting_edges, points, only_first=False
                ):
                    if intersecting_edge in non_intersecting_edges:
                        edges_to_check.add(intersecting_edge)
                        non_intersecting_edges.remove(intersecting_edge)

    vertices = recombine_edges(non_intersecting_edges)

    polygon = list(map(lambda v: points[v], vertices))

    if polygon_is_clockwise(polygon):
        polygon = list(reversed(polygon))

    return fit_to_bbox(polygon)


def test_random_polygon():
    for _ in range(100):
        for num_points in [5, 15, 30, 60]:
            polygon = random_polygon(num_points)
            assert no_edges_intersect(polygon)

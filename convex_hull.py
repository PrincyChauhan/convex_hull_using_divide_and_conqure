from functools import cmp_to_key

# Center of the polygon
origin = [0, 0]

def quadrant(p):
    # Return quadrant number (1, 2, 3, or 4) based on the point's position
    if p[0] >= 0 and p[1] >= 0:
        return 1
    if p[0] <= 0 and p[1] >= 0:
        return 2
    if p[0] <= 0 and p[1] <= 0:
        return 3
    return 4


def orientation(a, b, c):
    # Calculate the orientation of three points (a, b, c)
    result = (b[1] - a[1]) * (c[0] - b[0]) - (c[1] - b[1]) * (b[0] - a[0])
    if result == 0:
        return 0  # Collinear
    if result > 0:
        return 1  # Counter-clockwise
    return -1  # Clockwise


def compare(p1, q1):
    # Comparison function for sorting points based on their quadrants and orientations
    p = [p1[0] - origin[0], p1[1] - origin[1]]
    q = [q1[0] - origin[0], q1[1] - origin[1]]
    one = quadrant(p)
    two = quadrant(q)

    if one != two:
        if one < two:
            return -1
        return 1

    if p[1] * q[0] < q[1] * p[0]:
        return -1
    return 1


def upper_tangent(a, b):
    # Find the upper tangent between two convex hulls 'a' and 'b'
    n1, n2 = len(a), len(b)
    ia, ib = 0, 0

    # Find the rightmost point of 'a' and the leftmost point of 'b'
    for i in range(1, n1):
        if a[i][0] > a[ia][0]:
            ia = i

    for i in range(1, n2):
        if b[i][0] < b[ib][0]:
            ib = i

    inda, indb = ia, ib
    done = 0
    while not done:
        done = 1
        while orientation(b[indb], a[inda], a[(inda + 1) % n1]) >= 0:
            inda = (inda + 1) % n1

        while orientation(a[inda], b[indb], b[(n2 + indb - 1) % n2]) <= 0:
            indb = (indb - 1) % n2
            done = 0

    return inda, indb


def lower_tangent(a, b):
    # Find the lower tangent between two convex hulls 'a' and 'b'
    n1, n2 = len(a), len(b)
    ia, ib = 0, 0

    # Find the rightmost point of 'a' and the leftmost point of 'b'
    for i in range(1, n1):
        if a[i][0] > a[ia][0]:
            ia = i

    for i in range(1, n2):
        if b[i][0] < b[ib][0]:
            ib = i

    inda, indb = ia, ib
    done = 0
    while not done:
        done = 1
        while orientation(a[inda], b[indb], b[(indb + 1) % n2]) >= 0:
            indb = (indb + 1) % n2

        while orientation(b[indb], a[inda], a[(n1 + inda - 1) % n1]) <= 0:
            inda = (inda - 1) % n1
            done = 0

    return inda, indb


def merge_convex_hulls(a, b):
    # Merge two convex hulls 'a' and 'b' to obtain the convex hull of their union
    uppera, upperb = upper_tangent(a, b)
    lowera, lowerb = lower_tangent(a, b)

    ret = []
    ind = uppera
    ret.append(a[uppera])
    while ind != lowera:
        ind = (ind + 1) % len(a)
        ret.append(a[ind])

    ind = lowerb
    ret.append(b[lowerb])
    while ind != upperb:
        ind = (ind + 1) % len(b)
        ret.append(b[ind])

    return ret


def brute_hull(a):
    # Brute force algorithm to find the convex hull for a set of less than 6 points
    global origin
    s = set()
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            x1, x2 = a[i][0], a[j][0]
            y1, y2 = a[i][1], a[j][1]
            a1, b1, c1 = y1 - y2, x2 - x1, x1 * y2 - y1 * x2
            pos, neg = 0, 0
            for k in range(len(a)):
                if (k == i) or (k == j) or (a1 * a[k][0] + b1 * a[k][1] + c1 <= 0):
                    neg += 1
                if (k == i) or (k == j) or (a1 * a[k][0] + b1 * a[k][1] + c1 >= 0):
                    pos += 1
            if pos == len(a) or neg == len(a):
                s.add(tuple(a[i]))
                s.add(tuple(a[j]))

    ret = []
    for x in s:
        ret.append(list(x))

    # Sorting the points in anti-clockwise order
    origin = [0, 0]
    n = len(ret)
    for i in range(n):
        origin[0] += ret[i][0]
        origin[1] += ret[i][1]
        ret[i][0] *= n
        ret[i][1] *= n
    ret = sorted(ret, key=cmp_to_key(compare))
    for i in range(n):
        ret[i] = [ret[i][0] / n, ret[i][1] / n]
    return ret


def convex_hull(points):
    # Returns the convex hull for the given set of points
    if len(points) <= 5:
        return brute_hull(points)

    left, right = [], []
    start = int(len(points) / 2)
    for i in range(start):
        left.append(points[i])
    for i in range(start, len(points)):
        right.append(points[i])

    left_hull = convex_hull(left)
    right_hull = convex_hull(right)

    return merge_convex_hulls(left_hull, right_hull)


if __name__ == '__main__':
    points = []
    points.append([1, 1])
    points.append([1, -1])
    points.append([-1, -1])
    points.append([6, 1])
    points.append([-2, -2])
    points.append([-7, 4])

    points.sort()
    convex_hull_points = convex_hull(points)

    print('Convex Hull:')
    for x in convex_hull_points:
        print(int(x[0]), int(x[1]))

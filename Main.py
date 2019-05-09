from sympy import Symbol, nsolve
from scipy.optimize import least_squares
import numpy as np




anchors = [(1, 1), (-1, 1), (-1, -1), (1, -1)]


with open("python_zadanie_2.txt", "r") as task_file:
    task_file_lines = task_file.readlines()

tag2anchs_dist = []

tags_data = {'tag_id': [], 'dist_to_anchors': [], 'tag_xy': []}
blank_count = 0;
for line in task_file_lines[task_file_lines.index('2. Pomiary odległości obiektów od anchorów\n') + 6:]:
    if line != '\n':
        str_line = line.strip('\n').split(' ')
        num_line = [float(i) for i in str_line]
        num_line[0] = int(num_line[0])
        tags_data['tag_id'].append(num_line[0])
        tags_data['dist_to_anchors'].append(num_line[1:])
        tag2anchs_dist.append(num_line)
        blank_count = 0;
    else:
        blank_count += 1
    if blank_count > 1:
        break

print(tags_data)

blank_count = 0
polys_data = {'poly_id': [], 'nodes_id': []}
for line in task_file_lines[task_file_lines.index('3. Opis wielokątów\n') + 6:]:
    if line != '\n':
        str_line = line.strip('\n').replace('[', '').replace(']', '').split(' ')
        num_line = [int(i) for i in str_line]
        polys_data['poly_id'].append(num_line[0])
        polys_data['nodes_id'].append(num_line[1:])
        blank_count = 0
    else:
        blank_count += 1
    if blank_count > 1:
        break

print(polys_data)

blank_count = 0

nodes_data = {'node_id': [], 'node_xy': []}
for line in task_file_lines[task_file_lines.index('4. Położenia wierzchołków wielokątów\n') + 6:]:
    if line != '\n':
        str_line = line.strip('\n').split(' ')
        num_line = [float(i) for i in str_line]
        num_line[0] = int(num_line[0])
        nodes_data['node_id'].append(num_line[0])
        nodes_data['node_xy'].append(tuple(num_line[1:3]))
        blank_count = 0
    else:
        blank_count += 1
    if blank_count > 1:
        break

print(nodes_data)

def equations(X_vec, **kwargs):
    F = []
    for i in range(4):
        F.append((kwargs['anchors'][i][0] - X_vec[0]) ** 2 + (kwargs['anchors'][i][1] - X_vec[1]) ** 2
                 - kwargs['distances'][i] ** 2)
    return np.array(F)

def getTagPosition(anchors, distances):
    X_vec_0 = np.array([1, 1])
    tag_data = {'anchors': anchors, 'distances': distances}
    res1 = least_squares(equations, X_vec_0, method='lm', kwargs=tag_data)
    return tuple(res1.x)

# def getTagPositionNSolve(anchors, distances):
#     x, y = Symbol('x'), Symbol('y')
#     F = []
#     for i in range(4):
#         F.append((anchors[i][0] - x) ** 2 + (anchors[i][1] - y) ** 2 - distances[i] ** 2)
#     prim_approx = [0, 0]
#     ans = nsolve(F, [x, y], prim_approx, verify=False)
#     for i in range(4):
#         print((anchors[i][0] - ans[0]) ** 2 + (anchors[i][1] - ans[1]) ** 2 - distances[i] ** 2)
#
#     print('\n')
#     return tuple(ans)

# for i in range(4):
#     print((anchors[i][0] - res1.x[0]) ** 2 + (anchors[i][1] - res1.x[1]) ** 2 - distances[i] ** 2)

for el in tags_data['dist_to_anchors']:
    tags_data['tag_xy'].append(getTagPosition(anchors, el))
print(tags_data)

def getLineEquationCoeffs(seg):
    x1, y1 = seg[0][0], seg[0][1]
    x2, y2 = seg[1][0], seg[1][1]

    A = y2 - y1
    B = x1 - x2
    C = (x2 * y1) - (x1 * y2)

    return A, B, C

def doSegmentsIntersect(segA, segB):
    xA_1, yA_1 = segA[0][0], segA[0][1]
    xA_2, yA_2 = segA[1][0], segA[1][1]

    xB_1, yB_1 = segB[0][0], segB[0][1]
    xB_2, yB_2 = segB[1][0], segB[1][1]

    # seg1 as inf line
    # equation of line1 as Ax + By + C = 0

    a1, b1, c1 = getLineEquationCoeffs(segA)

    # check equation for values of seg2 coords
    dB_1 = a1 * xB_1 + b1 * yB_1 + c1
    dB_2 = a1 * xB_2 + b1 * yB_2 + c1

    #if both seg2 points are on the same side of line1 - no intersection
    if dB_1 * dB_2 > 0:
        return False

    a2, b2, c2 = getLineEquationCoeffs(segB)

    dA_1 = a2 * xA_1 + b2 * yA_1 + c2
    dA_2 = a2 * xA_2 + b2 * yA_2 + c2

    if dA_1 * dA_2 > 0:
        return False

    # if segments are collinear
    if (a1 * b2) - (a2 * b1) == 0.:
        return False

    return True

def isTagInPoligon(tag_xy, poly_xy):

    poly_min_x, poly_max_x = min([pnt[0] for pnt in poly_xy]), max([pnt[0] for pnt in poly_xy])
    poly_min_y, poly_max_y = min([pnt[1] for pnt in poly_xy]), max([pnt[1] for pnt in poly_xy])

    # polygon bounding box check
    if tag_xy[0] > poly_max_x or tag_xy[0] < poly_min_x:
        return False
    if tag_xy[1] > poly_max_y or tag_xy[1] < poly_min_y:
        return False

    # create reference point which together with tag will create segment to check intersections
    eps = 0.2
    refPoint = (poly_max_x + eps * abs(poly_max_x), poly_max_y + eps * abs(poly_max_y))
    refPoints = [refPoint, (refPoint[0] + eps / 4, refPoint[1]), (refPoint[0], refPoint[1] - eps / 4),
                 (refPoint[0] - eps / 4, refPoint[1]), (refPoint[0], refPoint[1] + eps / 4)]

    for refPnt in refPoints:
        tag_seg = [tag_xy, refPnt]
        intersects_count = 0
        for poly_nod in enumerate(poly_xy):
            poly_seg = [poly_nod[1], poly_xy[poly_nod[0] - 1]]

            if doSegmentsIntersect(tag_seg, poly_seg):
                intersects_count += 1

        if intersects_count % 2 == 1:
            return True
        else:
            continue
    return False

P1 = (1, 0.99999)
poly = [(1., 1.), (0., -2.), (-1., 1.)]
print(isTagInPoligon(P1, poly))




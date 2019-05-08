from sympy import Symbol, nsolve
from scipy.optimize import least_squares
import numpy as np


anchors = [(1, 1), (-1, 1), (-1, -1), (1, -1)]


with open("python_zadanie_2.txt", "r") as task_file:
    task_file_lines = task_file.readlines()

tag2anchs_dist = []

blank_count = 0;
for line in task_file_lines[task_file_lines.index('2. Pomiary odległości obiektów od anchorów\n') + 6:]:
    if line != '\n':
        str_line = line.strip('\n').split(' ')
        num_lin = [float(i) for i in str_line]
        num_lin[0] = int(num_lin[0])
        tag2anchs_dist.append(num_lin)
        blank_count = 0;
    else:
        blank_count += 1
    if blank_count > 1:
        break

print(tag2anchs_dist)

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

tags_data = []
for el in tag2anchs_dist:
    tags_data.append([el[0], getTagPosition(anchors, el[1:])])
print(tags_data)

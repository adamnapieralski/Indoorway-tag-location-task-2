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
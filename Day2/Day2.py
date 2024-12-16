def is_diff_valid(diff, is_increasing):
    # check the difference is valid
    if (abs(diff) == 0 or abs(diff) > 3):
        # difference if invalid
        return False
    else:
        # difference if valid
        # ensure the whole line in increasing or decreasing
        if ((is_increasing and diff < 0)
            or (is_increasing == False and diff > 0)):
            return False
        else:
            return True

def is_line_safe(line):
    count = len(line)
    index = 0
    is_increasing = False

    while index < count - 1:
        diff = (line[index + 1]) - (line[index])

        if (index == 0):
            if (diff > 0):
                is_increasing = True

        valid = is_diff_valid(diff, is_increasing)
        if (valid == False):
            return False
        
        index += 1
    return True

def part_1(matrix):
    global part1_safe
    part1_safe = 0
    unsafe_lines = []

    for line in matrix:
        # check if line is safe
        if (is_line_safe(line)):
            part1_safe += 1
        else:
            unsafe_lines.append(line)

    print("Part 1 number safe = ", part1_safe)
    return unsafe_lines

def part_2(matrix):
    global part2_safe
    part2_safe = 0

    # know that all the lines coming in are unsafe. Need to find out if the removal of one level will make the line safe - brute force
    for list in matrix:
        count = len(list)
        i = 0

        while i < count:
            # remove the number from the list and test if it is valid
            list_copy = list.copy()
            list_copy.pop(i)
            if (is_line_safe(list_copy)):
                part2_safe += 1
                is_safe = True
                break
            i += 1           

    print("Part 2 number safe = ", part2_safe)

##########################################

with open('C:\SourceCode\AdventOfCode24\Day2\puzzle_input.txt', 'r') as f:
    lines = f.readlines()

matrix = []
for line in lines:
    numbers = line.split()
    num_list = []

    for number in numbers:
        num_list.append((int)(number))
    
    matrix.append(num_list)

unsafe_lines = part_1(matrix)
part_2(unsafe_lines)
print("Total number of safe lines = ", part1_safe + part2_safe)
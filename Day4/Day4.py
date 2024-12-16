def part1(num_rows, num_cols):
    total_xmas = 0

    # iterate through each line to find an 'X'
    row = 0
    for line in lines:
        list = ([pos for pos, char in enumerate(line) if char == 'X'])
        
        for col in list:
            if row >= 3: # up
                total_xmas += lines[row - 1][col] == 'M' and lines[row - 2][col] == 'A' and lines[row - 3][col] == 'S'

            if row <= (num_rows - 4): # down
                total_xmas += lines[row + 1][col] == 'M' and lines[row + 2][col] == 'A' and lines[row + 3][col] == 'S'

            if col >= 3: # left
                total_xmas += lines[row][col - 1] == 'M' and lines[row][col - 2] == 'A' and lines[row][col - 3] == 'S'

            if col <= (num_cols - 4): # right
                total_xmas += lines[row][col + 1] == 'M' and lines[row][col + 2] == 'A' and lines[row][col + 3] == 'S'

            if row >= 3 and col <= (num_cols - 4): # north east
                total_xmas += lines[row - 1][col + 1] == 'M' and lines[row - 2][col + 2] == 'A' and lines[row - 3][col + 3] == 'S'

            if row >= 3 and col >= 3: # north west
                total_xmas += lines[row - 1][col - 1] == 'M' and lines[row - 2][col - 2] == 'A' and lines[row - 3][col - 3] == 'S'

            if row <= (num_rows - 4) and col <= (num_cols - 4): # south east
                total_xmas += lines[row + 1][col + 1] == 'M' and lines[row + 2][col + 2] == 'A' and lines[row + 3][col + 3] == 'S'

            if row <= (num_rows - 4) and col >= 3: # south west
                total_xmas += lines[row + 1][col - 1] == 'M' and lines[row + 2][col - 2] == 'A' and lines[row + 3][col - 3] == 'S'

        row += 1
    print("Part 1: ", total_xmas)

def part2(num_rows, num_cols):
    total_xmas = 0

    # iterate through each line to find an 'A'
    row = 0
    for line in lines:
        list = ([pos for pos, char in enumerate(line) if char == 'A'])
        
        for col in list:
            if row > 0 and row <= (num_rows - 2) and col > 0 and col <= (num_cols - 2):

                # check the north_east/south west direction
                if ((lines[row + 1][col - 1] == 'M' and lines[row - 1][col + 1] == 'S') 
                    or (lines[row + 1][col - 1] == 'S' and lines[row - 1][col + 1] == 'M')):

                    # check north west/south east direction
                    if ((lines[row - 1][col - 1] == 'M' and lines[row + 1][col + 1] == 'S') 
                        or (lines[row - 1][col - 1] == 'S' and lines[row + 1][col + 1] == 'M')):

                        total_xmas += 1
        row += 1

    print("Part 2: ", total_xmas)

#######################################################################
with open('C:\SourceCode\AdventOfCode24\Day4\puzzle_input.txt', 'r') as f:
    lines = f.readlines()

num_rows = len(lines)
num_cols = len(lines[0])
part1(num_rows, num_cols) #2530
part2(num_rows, num_cols) #1921
from time import perf_counter

class Solution:
    def __init__(self):
        self.obstacles = []
        self.distinct_pos = []
        self.guard_path = {}
        self.num_rows = 0
        self.num_cols = 0
        self.starting_pos = (0,0)

    def parse_input(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        # go through the input file and identify obstacles and current pos
        row = 0

        for line in lines:
            for col in range(len(line)):
                if line[col] == '#':
                    self.obstacles.append((row, col))
                elif line[col] == '^':
                    self.starting_pos = (row, col)
            row += 1

        self.num_rows = row
        self.num_cols = len(line)


    def part_one(self):
        self.find_exit_or_loop(self.obstacles, self.guard_path)
        return len(self.guard_path)

    
    def part_two(self):
        # to find number of ways to make a loop, for each step in the guards path, add an obstacle and check if loop or exit is found
        num_obstruction_positions = 0

        for step in self.guard_path:
            if step != self.starting_pos:
                # add new obstruction, test, remove obstruction
                self.obstacles.append(step)
                test_path = {}
                num_obstruction_positions += self.find_exit_or_loop(self.obstacles, test_path)
                self.obstacles.remove(step)
        
        return num_obstruction_positions


    def find_exit_or_loop(self, obstacles, path_map):
        # return 0 if exit is found. return 1 if loop is found

        pos = self.starting_pos
        dir = 'u'   # directions can be 'u', 'd, 'l', 'r'
        path_map[pos] = [dir]
        
        next_pos = (0,0)
        next_dir = ''
        loop_found = False

        while (1):
            # determine next action - rotate 90 degrees or take a step forward
            if dir == 'u':
                next_pos = (pos[0] - 1, pos[1])
                next_dir = 'r'
            elif dir == 'r':
                next_pos = (pos[0], pos[1] + 1)
                next_dir = 'd'
            elif dir == 'd':
                next_pos = (pos[0] + 1, pos[1])
                next_dir = 'l'
            elif dir == 'l':
                next_pos = (pos[0], pos[1] - 1)
                next_dir = 'u'

            if self.is_out_of_map(next_pos):
                return 0
            elif next_pos in obstacles:
                dir = next_dir
            else:
                pos = next_pos

            loop_found = self.add_pos_to_path_map(path_map, pos, dir)
            if loop_found:
                return 1


    def add_pos_to_path_map(self, path_map, pos, dir):
        loop_found = False
        values = path_map.get(pos)

        if values is not None:
            if (dir in values):
                loop_found = True
            else:
                values.append(dir)
        else:
            values = [dir]
        
        # update dictionary
        path_map[pos] = values

        return loop_found


    def is_out_of_map(self, pos):
        if pos[0] < 0 or pos[0] > self.num_rows - 1:
            return True
        if pos[1] < 0 or pos[1] > self.num_cols - 1:
            return True
        return False
    

#######################################################################
solution = Solution()
solution.parse_input('C:\SourceCode\AdventOfCode24\Day6\puzzle_input.txt')

start = perf_counter()
answer_part_one = solution.part_one()
print("Part 1 = ", answer_part_one)
answer_part_two = solution.part_two()
print("Part 2 = ", answer_part_two)
end = perf_counter()
print(f"Duration = {end - start}")
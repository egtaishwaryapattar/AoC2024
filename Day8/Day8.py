from time import perf_counter
from operator import sub
from operator import add
import os
import math

class Solution:
    def __init__(self):
        self.lines = []
        self.total_rows = 0
        self.total_cols = 0
        self.antenna_locations = {}     # key is antenna type, value is list a location coordinates as tuples (x,y)
        self.antinode_locations = []

    def parse_input(self, filename):
        with open(filename, 'r') as f:
            self.lines = f.readlines()

        row = 0
        for line in self.lines:
            line = line.replace("\n", "")

            # find column positions of all antenna in this line
            cols = ([pos for pos, char in enumerate(line) if char != '.'])
            for col in cols:
                self.add_antenna_to_dict(line[col], row, col)
            row += 1
    
        self.total_rows = row
        self.total_cols = len(line) 


    def add_antenna_to_dict(self, antenna, row, col):
        coords = self.antenna_locations.get(antenna)
        if coords is None:
            coords = [(row, col)]
        else:
            coords.append((row, col))
        self.antenna_locations[antenna] = coords


    def part_one(self):
        self.antinode_locations = []
        for antenna in self.antenna_locations:
            self.find_antinodes_for_antenna_type(antenna, 1)
        return len(self.antinode_locations)
        

    def part_two(self):
        self.antinode_locations = []

        for antenna in self.antenna_locations:
            antenna_locations = self.antenna_locations.get(antenna)
            if (len(antenna_locations) > 1): 
                self.find_antinodes_for_antenna_type(antenna, math.inf)
                
                for location in antenna_locations:
                    self.add_antinode(location)

        return len(self.antinode_locations)


    def find_antinodes_for_antenna_type(self, antenna, num_iterations):
        locations = self.antenna_locations.get(antenna)
        num_locations = len(locations)

        for i in range(num_locations - 1):
            j = i + 1
            while j < num_locations:
                # find distance between the antenna at i and antenna at j (directin: going from i to j). then propogate in direction
                diff = tuple(map(sub, locations[j], locations[i]))
                self.propogate_antinodes(locations[i], diff, num_iterations, sub)
                self.propogate_antinodes(locations[j], diff, num_iterations, add)

                j += 1


    def propogate_antinodes(self, start_pos, diff, num_iterations, operator):
        iter = 0
        pos = start_pos
        while iter < num_iterations:
            node = tuple(map(operator, pos, diff))
            if self.is_in_grid(node):
                self.add_antinode(node)

                # update pos and iterator
                pos = node
                iter += 1
            else:
                break

    
    def add_antinode(self, antinode):
        if antinode not in self.antinode_locations:
            self.antinode_locations.append(antinode)


    def is_in_grid(self, pos):
        if pos[0] < 0 or pos[0] > self.total_rows - 1:
            return False
        if pos[1] < 0 or pos[1] > self.total_cols - 1:
            return False
        return True


    def print_grid_with_antinodes(self):
        lines = self.lines.copy()
        for antinode in self.antinode_locations:
            row = antinode[0]
            col = antinode[1]
            line = lines[row]
            string_list = list(line)
            string_list[col] = '#'
            lines[row] = "".join(string_list)
        
        for line in lines:
            print(line)


#######################################################################
solution = Solution()
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'puzzle_input.txt')
solution.parse_input(filename)

start = perf_counter()
answer_part1 = solution.part_one()
print("Part1 = ", answer_part1)
answer_part2 = solution.part_two()
print("Part2 = ", answer_part2)
end = perf_counter()
print(f"Duration = {end - start}")
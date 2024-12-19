from time import perf_counter
import os

class Solution:
    def __init__(self):
        self.patterns = set()
        self.designs = []
    

    def parse_input(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        line_number = 0
        for line in lines:
            line = line.replace("\n", "")

            if line_number == 0:
                patterns = line.split(', ')
                for pattern in patterns:
                    self.patterns.add(pattern)

            elif line_number > 1:
                self.designs.append(line)

            line_number += 1

    
    def part_one(self):
        self.add_new_patterns_to_cache(self.patterns)

        # get possible designs
        possible_designs = 0
        for design in self.designs:
            if self.is_design_possible(design):
                possible_designs += 1

        return possible_designs


    def part_two(self):
        return 0
    

    def is_design_possible(self, design):
        # check if we have already encountered this design
        if design in self.patterns:
            return True
        
        sub_patterns = []
        substr = design
        design_possible = True

        while len(substr) > 0:
            sub_pattern = self.find_first_pattern_in_string(substr)

            if sub_pattern == None:
                design_possible = False
                break
            else:
                sub_patterns.append(sub_pattern)
                # test the next substring
                strs = substr.split(sub_pattern)
                substr = strs[1]

        # add new sub patterns to cache
        self.add_new_patterns_to_cache(sub_patterns)
        if design_possible:
            self.patterns.add(design)

        return design_possible
        
        
    def add_new_patterns_to_cache(self, patterns):
        # pad out the patterns with additional combos
        new_patterns = []
        for pattern1 in patterns:
            for pattern2 in patterns:
                new_patterns.append(pattern1 + pattern2)

        # add to cache
        for pattern in new_patterns:
            self.patterns.add(pattern)


    def find_first_pattern_in_string(self, str):
        # test for i = 0
        if str in self.patterns:
            return str

        for i in range(1, len(str)):
            substr = str[:-i]
            if substr in self.patterns:
                return substr
        return None


###################################################################################
solution = Solution()
dir_name = os.path.dirname(__file__)
filename = os.path.join(dir_name, 'puzzle_input.txt')
solution.parse_input(filename)

start = perf_counter()
part1 = solution.part_one()
part2 = solution.part_two()
end = perf_counter()
print(f"Part 1 = {part1}")  # answer of 334 is too low
print(f"Part 2 = {part2}")         
print(f"Duration = {end - start}s")
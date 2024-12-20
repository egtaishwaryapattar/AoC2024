from time import perf_counter
import os

class Solution:
    def __init__(self):
        self.patterns = {}
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
                    first_letter = pattern[0]
                    values = self.patterns.get(first_letter)
                    if values is None:
                        values = [pattern]
                    else:
                        values.append(pattern)
                    self.patterns[first_letter] = values
            elif line_number > 1:
                self.designs.append(line)

            line_number += 1

        # sort the pattern arrays 
        for key in self.patterns:
            values = self.patterns[key]
            values.sort(key=len)
            self.patterns[key] = values[::-1]

    
    def part_one(self):
        possible_designs = 0
        for design in self.designs:
            if self.is_design_possible(design):
                possible_designs += 1

        return possible_designs


    def part_two(self):
        return 0
    

    def is_design_possible(self, design_substr):
        # iterate through pattern list and see if a match can be found for the substring
        first_letter = design_substr[0]
        pattern_list = self.patterns.get(first_letter)
        
        if pattern_list == None:
            return False

        for pattern in pattern_list:
            if len(pattern) > len(design_substr):
                continue

            if pattern == design_substr:
                return True
            
            if design_substr.startswith(pattern):
                # get the remainder of the substring with the pattern removed and search the remainder for more patterns that match
                if self.is_design_possible(design_substr[len(pattern):]):
                    return True

        # no patterns found that match the substring
        return False


###################################################################################
solution = Solution()
dir_name = os.path.dirname(__file__)
filename = os.path.join(dir_name, 'test2.txt')
solution.parse_input(filename)

start = perf_counter()
part1 = solution.part_one()
part2 = solution.part_two()
end = perf_counter()
print(f"Part 1 = {part1}")  # answer of 334 is too low. 400 is too high (400 is all the results...)
print(f"Part 2 = {part2}")         
print(f"Duration = {end - start}s")
from time import perf_counter
import os

class Solution:
    def __init__(self):
        self.line_dict = {} # key = unique number in the line. value = occurrence of number in the line

    
    def parse_input(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        line = lines[0]
        values = line.split(' ')
        for value in values:
            self.add_value_to_dict(self.line_dict, value, 1)

    
    def part_one(self):
        self.apply_rules(25)
        return self.get_line_length(self.line_dict)


    def part_two(self):
        self.apply_rules(50)        # apply rules 50 more times so it's run 75 times
        return self.get_line_length(self.line_dict)
    

    def apply_rules(self, num_times):
        for i in range(num_times):
            temp_dict = {}

            for key in self.line_dict:
                occurence = self.line_dict.get(key)
                
                if key == '0':
                    self.add_value_to_dict(temp_dict, '1', occurence)

                elif len(key) % 2 == 0:
                    #split string in two and append each half
                    half = int(len(key)/2)
                    first_num = int(key[:half])
                    second_num = int(key[half:])

                    self.add_value_to_dict(temp_dict, str(first_num), occurence)
                    self.add_value_to_dict(temp_dict, str(second_num), occurence)

                else:
                    new_key = int(key) * 2024
                    self.add_value_to_dict(temp_dict, str(new_key), occurence)
            
            self.line_dict = temp_dict


    def add_value_to_dict(self, dict, key, value):
        dict[key] = dict.get(key, 0) + value

    
    def get_line_length(self, dict):
        occurrences = dict.values()
        return sum(occurrences)


###################################################################################
solution = Solution()
dir_name = os.path.dirname(__file__)
filename = os.path.join(dir_name, 'puzzle_input.txt')
solution.parse_input(filename)

start = perf_counter()
part1 = solution.part_one()
part2 = solution.part_two()
end = perf_counter()
print(f"Part 1 = {part1}")
print(f"Part 2 = {part2}")
print(f"Duration = {end - start}s")
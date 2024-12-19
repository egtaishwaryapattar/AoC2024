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
                    self.add_pattern_to_cache(pattern)

            elif line_number > 1:
                self.designs.append(line)

            line_number += 1

    
    def part_one(self):

        # get possible designs
        possible_designs = 0
        for design in self.designs:
            if self.is_design_possible(design):
                possible_designs += 1

        return possible_designs


    def part_two(self):
        return 0
    

    def is_design_possible(self, design):
        # solve using a* search - heuristic is number of letters away from the end
        # node is (cost, array of substrings)
        node = (0, [design])
        q = [node]
        solution_found = False

        while len(q) > 0:
            node = q.pop(0)

            arr = node[1]
            substr = arr[-1]
            first_letter = substr[0]
            cache = self.patterns.get(first_letter)

            if cache is not None:
                # check if substr exists in the cache - break when one (of possible multiple) solution is found
                if substr in cache:
                    solution_found = True
                    break
                
                # else see what values in the cache match the beginning of the substring and add to front of queue
                next_nodes = []
                for value in cache:
                    if substr.startswith(value):
                        # discard the last element of the node array and add the new split substring 
                        next_arr = arr[:-1]
                        next_arr.append(value)
                        next_arr.append(substr[len(value):])

                        cost = self.get_heuristic(next_arr)
                        next_node = (cost, next_arr)
                        next_nodes.append(next_node)
                
                q = next_nodes + q
                q.sort()

        # forget adding to cache as it'll build up too much
        '''
        if solution_found:
            # add all substrs to cache
            new_pattern = ''
            for str in reversed(node):
                new_pattern = str + new_pattern
                self.add_pattern_to_cache(new_pattern)
        '''
        return solution_found
    

    def get_heuristic(self, next_arr):
        steps_so_far = len(next_arr[:-1])
        letters_left = len(next_arr[-1])
        return steps_so_far + letters_left

    def add_pattern_to_cache(self, pattern):
        key = pattern[0]

        values = self.patterns.get(key)
        if values is None:
            values = set()
        
        values.add(pattern)
        self.patterns[key] = values


###################################################################################
solution = Solution()
dir_name = os.path.dirname(__file__)
filename = os.path.join(dir_name, 'test.txt')
solution.parse_input(filename)

start = perf_counter()
part1 = solution.part_one()
part2 = solution.part_two()
end = perf_counter()
print(f"Part 1 = {part1}")  # answer of 334 is too low
print(f"Part 2 = {part2}")         
print(f"Duration = {end - start}s")
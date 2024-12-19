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
        # solve using depth-first search and caching the nodes that lead to the solution
        # node is array of substrings as the design string is broken up
        node = [design]
        q = [node]
        solution_found = False

        while len(q) > 0:
            node = q.pop(0)

            substr = node[-1]
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
                        next_node = node[:-1]
                        next_node.append(value)
                        next_node.append(substr[len(value):])

                        next_nodes.append(next_node)
                
                q = next_nodes + q

        if solution_found:
            # add all substrs to cache
            new_pattern = ''
            for str in reversed(node):
                new_pattern = str + new_pattern
                self.add_pattern_to_cache(new_pattern)

        return solution_found
        

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
filename = os.path.join(dir_name, 'puzzle_input.txt')
solution.parse_input(filename)

start = perf_counter()
part1 = solution.part_one()
part2 = solution.part_two()
end = perf_counter()
print(f"Part 1 = {part1}")  # answer of 334 is too low
print(f"Part 2 = {part2}")         
print(f"Duration = {end - start}s")
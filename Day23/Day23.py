from time import perf_counter
import os

class Solution:
    def __init__(self):
        self.connections = {}
    

    def parse_input(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.replace("\n", "")
            computers = line.split('-')
            self.add_computer_connections_to_dict(computers[0], computers[1])

    
    def part_one(self):
        computer_sets = self.find_three_interconnected_computers()

        found_set_with_t = 0
        for set in computer_sets:
            computers = set.split(',')
            for computer in computers:
                if computer[0] == 't':
                    found_set_with_t += 1
                    break

        return found_set_with_t


    def part_two(self):
        return 0
    

    def add_computer_connections_to_dict(self, computer1, computer2):
        comp1_values = self.connections.get(computer1)
        comp2_values = self.connections.get(computer2)

        if comp1_values is None:
            comp1_values = set()
        if comp2_values is None:
            comp2_values = set()

        comp1_values.add(computer2)
        self.connections[computer1] = comp1_values
        comp2_values.add(computer1)
        self.connections[computer2] = comp2_values


    def find_three_interconnected_computers(self):
        computer_sets = set()

        for computer1 in self.connections:
            connections = self.connections.get(computer1)
            for computer2 in connections:
                if computer2 != computer1:
                    connections2 = self.connections.get(computer2)
                    for computer3 in connections2:
                        connections3 = self.connections.get(computer3)
                        if computer1 in connections3:

                            # found a set of 3 - arrange in alphabetical order to prevent duplicates from being added
                            arr = [computer1, computer2, computer3]
                            arr.sort()
                            computer_sets.add(','.join(arr))

        return computer_sets


###################################################################################
solution = Solution()
dir_name = os.path.dirname(__file__)
filename = os.path.join(dir_name, 'puzzle_input.txt')
solution.parse_input(filename)
cheat_saving = 100   # for test = 50, for puzzle input = 100

start = perf_counter()
part1 = solution.part_one()
print(f"Part 1 = {part1}") 
part2 = solution.part_two()
print(f"Part 2 = {part2}")  
end = perf_counter()       
print(f"Duration = {end - start}s")
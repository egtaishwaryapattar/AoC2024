from time import perf_counter
import os
import re
import math

class Solution:
    def __init__(self):
        self.fallen_bytes = []       # ordering is the order in which they fall
        self.corrupted_memory = set()
        self.start = (0,0)
        self.end = (0,0)
    

    def parse_input(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        p = re.compile(r'\d+')
        for line in lines:
            nums = p.findall(line)
            self.fallen_bytes.append( (int(nums[0]), int(nums[1])) )  # x,y coordinate appended

    
    def part_one(self, max_coordinate, num_bytes_fallen):
        self.end = (max_coordinate, max_coordinate)

        for byte in self.fallen_bytes[0:num_bytes_fallen]:
            self.corrupted_memory.add(byte)
        
        return self.a_star_search()


    def part_two(self, num_bytes_fallen):
        # somewhere between num_bytes_fallen - end of fallen bytes, one additional coordinate will mean a path can't be found. return the coordinate
        # TODO: ideally I should binary search between 1024-end(3450)
        for byte in self.fallen_bytes[num_bytes_fallen : -1]:
            # add byte to set
            self.corrupted_memory.add(byte)
            steps_to_end = self.a_star_search()
            if steps_to_end == None:
                break
        return byte
    

    def a_star_search(self):
        # define the node as (cost, steps, coordinate)
        start_cost = self.get_heuristic(self.start, 0)
        start_node = (start_cost, 0, self.start)

        visited = set()
        priority_q = [start_node]

        while len(priority_q) > 0:
            node = priority_q.pop(0)

            # check if the end has been reached
            if node[2] == self.end:
                return node[1]  # return the number of steps it took to get there
            
            visited.add(node[2])    # add the coordinate to the visited set

            # get next nodes and add to the priority queue
            next_nodes = self.get_next_nodes(node)
            if len(next_nodes) > 0:
                for next_node in next_nodes:
                    if next_node[2] not in visited and next_node not in priority_q:
                        # duplicates not added to priority_q - will only find one shortest path (not multiple options)
                        priority_q.append(next_node)

                priority_q.sort()

        return None
            

    def get_next_nodes(self, node):
        next_nodes = []
        current_pos = node[2]

        up = (current_pos[0], current_pos[1] - 1)
        down = (current_pos[0], current_pos[1] + 1)
        left = (current_pos[0] - 1, current_pos[1])
        right = (current_pos[0] + 1, current_pos[1])
        neighbours = [up, down, left, right]

        for new_pos in neighbours:
            if self.is_in_map(new_pos) and new_pos not in self.corrupted_memory:
                steps = node[1] + 1
                next_nodes.append( (self.get_heuristic(new_pos, steps), steps, new_pos))

        return next_nodes


    def get_heuristic(self, pos, num_steps_to_pos):
        return math.dist(pos, self.end) + num_steps_to_pos


    def is_in_map(self, coord):
        if coord[0] < 0 or coord[1] < 0 or coord[0] > self.end[0] or coord[1] > self.end[1]:
            return False
        return True


###################################################################################
solution = Solution()
dir_name = os.path.dirname(__file__)
filename = os.path.join(dir_name, 'puzzle_input.txt')
max_coordinate = 70      # test grid size = 0-6, puzzle input grid size = 0-70 (inclusive)
num_bytes_fallen = 1024   # 12 for test, 1024 for puzzle input
solution.parse_input(filename)

start = perf_counter()
part1 = solution.part_one(max_coordinate, num_bytes_fallen)
part2 = solution.part_two(num_bytes_fallen)
end = perf_counter()
print(f"Part 1 = {part1}")
print(f"Part 2 = {part2}")         
print(f"Duration = {end - start}s")
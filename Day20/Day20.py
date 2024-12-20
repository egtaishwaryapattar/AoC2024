from time import perf_counter
import os

class Solution:
    def __init__(self):
        self.walls = set()
        self.start = (0,0)  # (x,y)
        self.end = (0,0)    # (x,y)
        self.max_y = 0
        self.max_x = 0
        self.path = []
        self.cheats = {}
    

    def parse_input(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        y = 0
        for line in lines:
            line = line.replace("\n", "")
            x = 0

            for c in line:
                if c == '#':
                    self.walls.add((x,y))
                elif c == 'S':
                    self.start = (x,y)
                elif c == 'E':
                    self.end = (x,y)
                x += 1
            y += 1
        
        self.max_y = y - 1
        self.max_x = x - 1

    
    def part_one(self):
        # find all the ways to cheat
        index = 0
        for pos in self.path:
            self.try_cheating_2_spaces(pos, index)
            index += 1

        # return number of cheats that save at least 100s
        num_cheats = 0
        for time_saved in self.cheats:
            if time_saved >= 100:
                num_cheats += self.cheats.get(time_saved)
        return num_cheats


    def part_two(self, cheat_saving):
        self.cheats.clear()      

        # for point a and b on the path, where index(b) - index(a) > cheat_saving, is there a cheat path that gets from a to b in 20 steps
        max_a = len(self.path) - cheat_saving
        for a in range(0, max_a):
            for b in range(a + cheat_saving, len(self.path)):
                pos_a = self.path[a]
                pos_b = self.path[b]

                diff_x = abs(pos_b[0] - pos_a[0])
                diff_y = abs(pos_b[1] - pos_a[1])
                new_diff = diff_x + diff_y

                if new_diff <= 20:
                    # found a quicker route - calculate the time saving
                    original_diff = b - a
                    time_saved = original_diff - new_diff
                    if time_saved >= cheat_saving:
                        self.cheats[time_saved] = self.cheats.get(time_saved, 0) + 1

        return sum(self.cheats.values())


    def find_path_without_cheating(self):
        # there is a single path to the end - no branching options
        pos = self.start
        prev_pos = self.start
        self.path.append(pos)

        while pos != self.end:
            next_pos = self.get_next_space(pos, prev_pos)
            prev_pos = pos
            pos = next_pos
            self.path.append(pos)


    def get_next_space(self, pos, prev_pos):
        up =    (pos[0], pos[1] - 1)
        down =  (pos[0], pos[1] + 1)
        left =  (pos[0] - 1, pos[1])
        right = (pos[0] + 1, pos[1])
        dirs =  [up, down, left, right]

        for dir in dirs:
            if dir not in self.walls and dir != prev_pos:
                return dir  
        return None


    def try_cheating_2_spaces(self, pos, index_of_pos):
        up =    [ (pos[0], pos[1] - 1), (pos[0], pos[1] - 2) ]
        down =  [ (pos[0], pos[1] + 1), (pos[0], pos[1] + 2) ]
        left =  [ (pos[0] - 1, pos[1]), (pos[0] - 2, pos[1]) ]
        right = [ (pos[0] + 1, pos[1]), (pos[0] + 2, pos[1]) ]
        dirs = [up, down, left, right]

        # find where we can pass through the wall and join back onto the path
        for dir in dirs:
            if dir[0] in self.walls:
                if self.is_in_map(dir[1]) and dir[1] not in self.walls:
                    cheat_index = self.path.index(dir[1])

                    if cheat_index > index_of_pos:
                        # find how many steps are skipped and add to dict
                        time_saved = cheat_index - index_of_pos - 2     # do diff - 2 because we still have to take two steps to get into the new position
                        self.cheats[time_saved] = self.cheats.get(time_saved, 0) + 1


    def is_in_map(self, pos):
        if pos[0] < 0 or pos[0] > self.max_x:
            return False
        if pos[1] < 0 or pos[1] > self.max_y:
            return False
        return True

###################################################################################
solution = Solution()
dir_name = os.path.dirname(__file__)
filename = os.path.join(dir_name, 'puzzle_input.txt')
solution.parse_input(filename)
cheat_saving = 100   # for test = 50, for puzzle input = 100

start = perf_counter()
solution.find_path_without_cheating()
print(f"Duration for path without cheating is {len(solution.path) - 1}ms") # -1 to exclude the start position
part1 = solution.part_one()
print(f"Part 1 = {part1}") 
part2 = solution.part_two(cheat_saving)
print(f"Part 2 = {part2}")  
end = perf_counter()       
print(f"Duration = {end - start}s")
from time import perf_counter
import os
import re
import math

class Robot:
    def __init__(self, pos, velocity):
        # (x,y) where x is num steps to right, y is num steps down
        self.pos = pos
        self.velocity = velocity

class Solution:
    def __init__(self):
        self.robots = []
        self.quadrants = {}

    
    def parse_input(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            # one robot per line
            p = re.compile(r'-?\d+')
            vals = p.findall(line)

            robot = Robot( (int(vals[0]), int(vals[1])) , (int(vals[2]), int(vals[3])) )
            self.robots.append(robot)

    
    def part_one(self, width, height):
        iterations = 100
        quadrant_horizontal_boundary = (height - 1) / 2
        quadrant_vertical_boundary = (width - 1) / 2

        for robot in self.robots:
            # for each robot, determine where it'll be after the number of iterations
            x = ( robot.pos[0] + (iterations * robot.velocity[0]) ) % width
            y = ( robot.pos[1] + iterations * robot.velocity[1] ) % height

            # determine which quadrant that the new pos belongs to
            quadrant = 0
            if x < quadrant_vertical_boundary and y < quadrant_horizontal_boundary:
                quadrant = 1
            elif x > quadrant_vertical_boundary and y < quadrant_horizontal_boundary:
                quadrant = 2
            elif x < quadrant_vertical_boundary and y > quadrant_horizontal_boundary:
                quadrant = 3
            elif x > quadrant_vertical_boundary and y > quadrant_horizontal_boundary:
                quadrant = 4
                
            if quadrant != 0:
                self.quadrants[quadrant] = self.quadrants.get(quadrant, 0) + 1

        values = self.quadrants.values()
        return math.prod(values)


    def part_two(self, width, height, start_val):
        # hate vague requirements - attempt of a vague solution
        # for each second, check for a vertical line where there are a lot consecutive robots together
        for i in range(start_val, 10000):
            robots_in_col = {} # key = col number, value = list of row numbers of the robots

            # find robot's positions at time i
            for robot in self.robots:
                if i == start_val:
                    # get the robots in the position we want them to start in - not assessing this position
                    x = ( robot.pos[0] + start_val * robot.velocity[0] ) % width
                    y = ( robot.pos[1] + start_val * robot.velocity[1] ) % height
                    robot.pos = (x,y)

                else:
                    # robot moves to its next position
                    x = ( robot.pos[0] + robot.velocity[0] ) % width
                    y = ( robot.pos[1] + robot.velocity[1] ) % height
                    robot.pos = (x,y)

                    rows = robots_in_col.get(x)
                    if rows is None:
                        rows = [y]
                    else:
                        rows.append(y)
                    robots_in_col[x] = rows

            if len(robots_in_col) > 0:
                if self.find_max_consecutive_robots_in_col(robots_in_col) > 20:
                    print(f"Num seconds = {i}")
                    break
        
        return i
    
    
    def find_max_consecutive_robots_in_col(self, robots_in_col):
        max_consecutive_per_col = []

        for col_num in robots_in_col:
            # sort values in col in ascending order
            values = robots_in_col.get(col_num)
            values.sort()

            num_consecutives = []
            consecutive = 0
            for i in range(1, len(values)):
                if values[i] - values[i-1] == 1:
                    consecutive += 1
                else: 
                    num_consecutives.append(consecutive)
                    consecutive = 0 # reset the count

            if len(num_consecutives) > 0:
                max_consecutive_per_col.append(max(num_consecutives))
        
        if len(max_consecutive_per_col) == 0:
            return 0
        return max(max_consecutive_per_col)


###################################################################################
solution = Solution()
dir_name = os.path.dirname(__file__)
filename = os.path.join(dir_name, 'puzzle_input.txt')
solution.parse_input(filename)

# test grid is (11, 7). puzzle_input is (101, 103)
width = 101
height = 103

start = perf_counter()
part1 = solution.part_one(width, height)
part2 = solution.part_two(width, height, 0)
end = perf_counter()
print(f"Part 1 = {part1}")
print(f"Part 2 = {part2}")         
print(f"Duration = {end - start}s")
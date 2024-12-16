from time import perf_counter
import os

class WideObstacle:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Solution:
    def __init__(self):
        self.robot_pos = (0,0)
        self.obstacles = []     # list of coordinates
        self.walls = []         # list of coordinates
        self.instructions = ''
    

    def parse_input(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        # go through file and file robot (@), obtstacles (O) and walls (#) and instructions. IGNORE NEW LINES
        parse_instructions = False
        row = 0

        for line in lines:
            if line == '\n':
                parse_instructions = True
            else:
                if parse_instructions == False:
                    # process the map
                    col = 0
                    for c in line:
                        if c == '#':
                            self.walls.append( (row, col ))
                        elif c == 'O':
                            self.obstacles.append( (row, col) )
                        elif c == '@':
                            self.robot_pos = (row, col)
                        col += 1
                else:
                    # store the instructions
                    self.instructions = self.instructions + line
            row += 1

    
    def part_one(self):
        new_obstacle_positions = self.follow_instructions(1)
        return self.calculate_gps(new_obstacle_positions)


    def part_two(self):
        self.expand_map()
        wide_obstacle_positions = self.follow_instructions(2)

        # convert obstacle positions which are [WideObstacle] into [(coords)] containing just the lefts
        converted_obstacles = []
        for obstacle in wide_obstacle_positions:
            converted_obstacles.append(obstacle.left)
        return self.calculate_gps(converted_obstacles)


    def follow_instructions(self, problem_part):
        pos = self.robot_pos
        obstacles = self.obstacles.copy()

        for instruction in self.instructions:
            new_pos = pos
            if instruction == '^':
                new_pos = (pos[0] - 1, pos[1])
            elif instruction == 'v':
                new_pos = (pos[0] + 1, pos[1])
            elif instruction == '<':
                new_pos = (pos[0], pos[1] - 1)
            elif instruction == '>':
                new_pos = (pos[0], pos[1] + 1)

            if new_pos != pos:
                # position has changed so determine if it's possible to move there and if obstacles need to move
                if new_pos not in self.walls and self.is_obstacle_in_pos(new_pos, obstacles, problem_part) == False:
                    # space is clear to move into
                    pos = new_pos

                elif self.is_obstacle_in_pos(new_pos, obstacles, problem_part): 
                    # see if it's possible for obstacle(s) to be moved one place so that the robot can move
                    if problem_part == 1:
                        obstacle_moved = self.move_obstacle(new_pos, instruction, obstacles)
                    else:
                        obstacle_moved = self.move_wide_obstacle(new_pos, instruction, obstacles)

                    if obstacle_moved:
                        pos = new_pos

        return obstacles


    def calculate_gps(self, obstacles):
        gps_sum = 0
        for obstacle in obstacles:
            gps_sum += 100 * obstacle[0] + obstacle[1]
        return gps_sum
    

    def move_obstacle(self, obstacle_pos, direction, obstacles):
        obstacles_to_move = [obstacle_pos]
        free_space_found = False
        free_space = (0,0)

        while free_space_found == False:
            # check if next space is free of obstacles
            cur_pos = obstacles_to_move[-1]
            if direction == '^':
                new_pos = (cur_pos[0] - 1, cur_pos[1])
            elif direction == 'v':
                new_pos = (cur_pos[0] + 1, cur_pos[1])
            elif direction == '<':
                new_pos = (cur_pos[0], cur_pos[1] - 1)
            elif direction == '>':
                new_pos = (cur_pos[0], cur_pos[1] + 1)

            if new_pos in self.walls:
                break
            elif new_pos in obstacles:
                # add to obstacles that need moving and continue loop to search in the direction
                obstacles_to_move.append(new_pos)
            else:
                # free space found
                free_space_found = True
                free_space = new_pos

        if free_space_found:
            # shuffle all the obstacles across one. Essentially, the first obstalce_pos is deleted and a new one put in new_pos
            obstacles.remove(obstacle_pos)
            obstacles.append(free_space)

        return free_space_found


    def move_wide_obstacle(self, obstacle_pos, direction, obstacles):
        # find obstacle to move
        obstacle = self.get_wide_obstacle(obstacle_pos, obstacles)
        obstacles_to_move = [obstacle]
        free_space_found = False
        cur_obstacles = [obstacle]
        wall_found = False

        while free_space_found == False:
            # check if both space above existing obstacle is free of obstacles
            next_positions = []

            for cur_ob in cur_obstacles:
                if direction == '^':
                    next_positions.append( (cur_ob.left[0] - 1, cur_ob.left[1]) ) 
                    next_positions.append( (cur_ob.right[0] - 1, cur_ob.right[1]) )
                elif direction == 'v':
                    next_positions.append( (cur_ob.left[0] + 1, cur_ob.left[1]) )
                    next_positions.append( (cur_ob.right[0] + 1, cur_ob.right[1]) )
                elif direction == '<':
                    next_positions.append( (cur_ob.left[0], cur_ob.left[1] - 1) )
                    next_positions.append( (cur_ob.right[0], cur_ob.right[1] - 1) )
                elif direction == '>':
                    next_positions.append( (cur_ob.left[0], cur_ob.left[1] + 1) )
                    next_positions.append( (cur_ob.right[0], cur_ob.right[1] + 1) )

            cur_obstacles.clear()

            # if any next position hits a wall, cannot move obstacles
            for next_pos in next_positions:
                if next_pos in self.walls:
                    wall_found = True
                    break
                else:
                    # if any next position hits a obstacle, need to check if that obstacle can move so loop back round
                    next_obstacle = self.get_wide_obstacle(next_pos, obstacles)
                    if next_obstacle is not None and next_obstacle not in obstacles_to_move:
                        # add next obstacle once to list
                        obstacles_to_move.append(next_obstacle)
                        cur_obstacles.append(next_obstacle)     # loop back using this list

            if wall_found:
                break

            if len(cur_obstacles) == 0:
                # no obstacles or walls found in all the next positions
                free_space_found = True


        if free_space_found:
            # shuffle all the obstacles one space
            for obstacle in obstacles_to_move:
                if direction == '^':
                    obstacle.left = (obstacle.left[0] - 1, obstacle.left[1]) 
                    obstacle.right = (obstacle.right[0] - 1, obstacle.right[1]) 
                elif direction == 'v':
                    obstacle.left = (obstacle.left[0] + 1, obstacle.left[1]) 
                    obstacle.right = (obstacle.right[0] + 1, obstacle.right[1]) 
                elif direction == '<':
                    obstacle.left = (obstacle.left[0], obstacle.left[1] - 1) 
                    obstacle.right = (obstacle.right[0], obstacle.right[1] - 1) 
                elif direction == '>':
                    obstacle.left = (obstacle.left[0], obstacle.left[1] + 1) 
                    obstacle.right = (obstacle.right[0], obstacle.right[1] + 1) 

        return free_space_found
        

    def expand_map(self):
        original_walls = self.walls.copy()
        original_obstalces = self.obstacles.copy()
        self.walls.clear()
        self.obstacles.clear()

        for wall in original_walls:
            self.walls.append( (wall[0], wall[1] * 2) )
            self.walls.append( (wall[0], wall[1] * 2 + 1) )

        for obstacle in original_obstalces:
            left = (obstacle[0], obstacle[1] * 2)
            right = (obstacle[0], obstacle[1] * 2 + 1)
            new_obstacle = WideObstacle(left, right)
            self.obstacles.append(new_obstacle)

        self.robot_pos = (self.robot_pos[0], self.robot_pos[1] * 2)


    def is_obstacle_in_pos(self, pos, obstacles, problem_part):
        if problem_part == 1:
            return pos in obstacles
        
        if problem_part == 2:
            for obstacle in obstacles:
                if pos == obstacle.left:
                    return True
                if pos == obstacle.right:
                    return True
            return False


    def get_wide_obstacle(self, obstacle_pos, obstacles):
        for obstacle in obstacles:
            if obstacle_pos == obstacle.left or obstacle_pos == obstacle.right:
                return obstacle
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
print(f"Part 1 = {part1}")
print(f"Part 2 = {part2}")         
print(f"Duration = {end - start}s")
from time import perf_counter
import os
import queue

class Solution:
    def __init__(self):
        self.walls = set()
        self.start_pos = (0,0)
        self.end_pos = (0,0)
        self.north_dir = '^'
        self.south_dir = 'v'
        self.east_dir = '>'
        self.west_dir = '<'


    def parse_input(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        # go through file and find walls, start pos, end pos
        row = 0
        for line in lines:
            col = 0
            for c in line:
                if c == '#':
                    self.walls.add( (row, col) )
                elif c == 'S':
                    self.start_pos = (row, col)
                elif c == 'E':
                    self.end_pos = (row, col)
                col += 1
            row += 1

    
    def run(self):
        nodes = self.get_shortest_paths()
        cost = nodes[0][0]

        # get unique tiles from all best paths (nodes)
        tiles = set()
        for node in nodes:
            tiles.update(node[1])

        return cost, len(tiles)
    

    def get_shortest_paths(self):
        # use Dijkstra's Algorithm to search for the shortest path
        # node is a tuple defined as (cost, path, current_direction)
        # use a priority queue to determine where to search first - priority is sorted by the cost

        start_node = (0, [self.start_pos], '>')
        priority_q = queue.PriorityQueue()
        priority_q.put(start_node)
        visited = set()
        best_paths = []

        while not priority_q.empty():
            node = priority_q.get()

            # check if the last coordinate in path is the end point. else add to visited coordinates & direction
            if node[1][-1] == self.end_pos:
                best_paths.append(node)
                break
            
            visited.add( (node[1][-1], node[2]) )

            # check where it can go next and the cost of this
            next_nodes = self.get_next_nodes(node)
            for next_node in next_nodes:
                if (next_node[1][-1], next_node[2]) not in visited:
                    priority_q.put(next_node)


        # find all paths with the same cost that have reached end point. these are all the best paths
        cost = node[0]
        all_paths_found = False

        while all_paths_found == False:
            node = priority_q.get()
            if node[0] == cost and node[1][-1] == self.end_pos:
                best_paths.append(node)
            else:
                all_paths_found = True

        return best_paths
    

    def get_next_nodes(self, current_node):
        next_nodes = []
        cost = current_node[0]
        coord = current_node[1][-1]
        dir = current_node[2]
        east = (coord[0], coord[1] + 1)
        west = (coord[0], coord[1] - 1)
        north = (coord[0] - 1, coord[1])
        south = (coord[0] + 1, coord[1])

        # check the three possible directions do not have a wall
        # if the next coord is a valid place to go, create a node with the new cost, coord and direction

        # east
        if dir == self.east_dir:
            if east not in self.walls:
                path = current_node[1].copy()
                path.append(east)
                next_nodes.append( (cost + 1, path, dir) )                      # same direction
            if north not in self.walls:
                path = current_node[1].copy()
                path.append(north)
                next_nodes.append( (cost + 1001, path, self.north_dir) )       # perpendicular
            if south not in self.walls:
                path = current_node[1].copy()
                path.append(south)
                next_nodes.append( (cost + 1001, path, self.south_dir) )       # perpendicular

        # south
        elif dir == self.south_dir:
            if south not in self.walls:
                path = current_node[1].copy()
                path.append(south)
                next_nodes.append( (cost + 1, path, dir) )                     # same direction
            if east not in self.walls:
                path = current_node[1].copy()
                path.append(east)
                next_nodes.append( (cost + 1001, path, self.east_dir) )         # perpendicular
            if west not in self.walls:
                path = current_node[1].copy()
                path.append(west)
                next_nodes.append( (cost + 1001, path, self.west_dir) )         # perpendicular

        # west
        elif dir == self.west_dir:
            if west not in self.walls:
                path = current_node[1].copy()
                path.append(west)
                next_nodes.append( (cost + 1, path, dir) )                      # same direction
            if north not in self.walls:
                path = current_node[1].copy()
                path.append(north)
                next_nodes.append( (cost + 1001, path, self.north_dir) )       # perpendicular
            if south not in self.walls:
                path = current_node[1].copy()
                path.append(south)
                next_nodes.append( (cost + 1001, path, self.south_dir) )       # perpendicular

        # north
        elif dir == self.north_dir:
            if north not in self.walls:
                path = current_node[1].copy()
                path.append(north)
                next_nodes.append( (cost + 1, path, dir) )                     # same direction
            if east not in self.walls:
                path = current_node[1].copy()
                path.append(east)
                next_nodes.append( (cost + 1001, path, self.east_dir) )         # perpendicular
            if west not in self.walls:
                path = current_node[1].copy()
                path.append(west)
                next_nodes.append( (cost + 1001, path, self.west_dir) )         # perpendicular

        return next_nodes


###################################################################################
solution = Solution()
dir_name = os.path.dirname(__file__)
filename = os.path.join(dir_name, 'puzzle_input.txt')
solution.parse_input(filename)

start = perf_counter()
part1, part2 = solution.run()
end = perf_counter()
print(f"Part 1 = {part1}")
print(f"Part 2 = {part2}")         
print(f"Duration = {end - start}s")
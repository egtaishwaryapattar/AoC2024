from time import perf_counter
import os

class Solution:
    def __init__(self):
        self.num_rows = 0
        self.num_cols = 0
        self.plant_dict = {}    # dictionary where key is letter and value is coord position
        self.plot_dict = {} # dictionary with key = Letter, value = list of list of coordinates (each list representing a unique plot)


    def parse_input(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        self.add_to_plant_dict(lines)
        self.sort_plants_into_plots()

    
    def run(self):
        result1 = 0
        result2 = 0

        for plant_type in self.plot_dict:
            plots = self.plot_dict.get(plant_type)
            for plot in plots:
                area = len(plot)
                perimeter = self.get_perimeter_of_plot(plot)
                num_sides = self.get_sides_of_plot(plot)
                result1 += area * perimeter
                result2 += area * num_sides

        return (result1, result2)


    def add_to_plant_dict(self, lines):
        row_number = 0
        for line in lines:
            col_number = 0
            for c in line:
                if c != "\n":
                    values = self.plant_dict.get(c)
                    if values is None:
                        values = [(row_number, col_number)]
                    else:
                        values.append((row_number, col_number))
                    self.plant_dict[c] = values
                col_number += 1
            row_number += 1
        
        self.num_rows = row_number
        self.num_cols = col_number

    
    def sort_plants_into_plots(self):
        # for each flower coords
        # starts from the first one and make a q
        # search all neighbours and add to plot_dict the new neighbours (remove from old dict), then add to q 
        # go along q and find more neighbours. repeat

        for plant_type in self.plant_dict:
            positions = self.plant_dict.get(plant_type)
            self.plot_dict[plant_type] = []

            while len(positions) > 0:
                coord = positions.pop(0)
                q = [coord]
                plot = [coord]

                while len(q) > 0:
                    curr_pos = q.pop(0)
                    neighbours = self.find_neighbours(curr_pos, positions)

                    if len(neighbours) > 0:
                        q = neighbours + q

                        for neighbour in neighbours:
                            positions.remove(neighbour)
                            plot.append(neighbour)
                        
                        if len(positions) == 0:
                            break
                
                plots = self.plot_dict.get(plant_type)
                if plots is None:
                    plots = [plot]
                else:
                    plots.append(plot)
                self.plot_dict[plant_type] = plots


    def find_neighbours(self, coord, positions):
        directions = [  (coord[0] - 1, coord[1]), # north 
                        (coord[0], coord[1] + 1), # east
                        (coord[0] + 1, coord[1]), # south
                        (coord[0], coord[1] - 1)] # west
        
        neighbours = []
        for new_pos in directions:
            if self.is_in_map(new_pos) and new_pos in positions:
                neighbours.append(new_pos)

        return neighbours


    def is_in_map(self, coord):
        if coord[0] < 0 or coord[0] > self.num_rows - 1:
            return False
        if coord[1] < 0 or coord[1] > self.num_cols - 1:
            return False
        return True
    

    def get_perimeter_of_plot(self, plot):
        # to find perimeter, go through each position in plot and check if it has a side that it doesn't share with another point in the plot
        perimeter = 0

        for pos in plot:
            neighbours = []
            directions = [  (pos[0] - 1, pos[1]), # north 
                            (pos[0], pos[1] + 1), # east
                            (pos[0] + 1, pos[1]), # south
                            (pos[0], pos[1] - 1)] # west
            
            for dir in directions:
                if dir not in plot:
                    perimeter += 1
                    neighbours.append(dir)

        return perimeter


    def get_sides_of_plot(self, plot):
        # can get the sides by counting the corners - look out for concave and convex corners
        num_corners = 0
        
        for pos in plot:
            # for each plot point, check the 4 corners to see how many corners it has

            # check NE corner
            ne_points = [   (pos[0] - 1, pos[1]),       # north
                            (pos[0] - 1, pos[1] + 1),   # north east
                            (pos[0], pos[1] + 1)]       # east
            num_corners += self.is_corner(pos, ne_points, plot)

            # check NW corner
            nw_points = [   (pos[0] - 1, pos[1]),       # north
                            (pos[0] - 1, pos[1] - 1),   # north west
                            (pos[0], pos[1] - 1)]       # west
            num_corners += self.is_corner(pos, nw_points, plot)

            # check SE corner
            se_points = [   (pos[0] + 1, pos[1]),       # south
                            (pos[0] + 1, pos[1] + 1),   # south east
                            (pos[0], pos[1] + 1)]       # east
            num_corners += self.is_corner(pos, se_points, plot)

            # check SW corner
            sw_points = [   (pos[0] + 1, pos[1]),       # south
                            (pos[0] + 1, pos[1] - 1),   # south west
                            (pos[0], pos[1] - 1)]       # west
            num_corners += self.is_corner(pos, sw_points, plot)

        return num_corners
    

    def is_corner(self, pos, surrounding_points, plot):
        # in surrounding points, make sure the diagonal is in index [1]

        # check if it is a convex corner 
        if (surrounding_points[0] not in plot
            and surrounding_points[2] not in plot):
            return 1

        # check for concanve corners
        if (surrounding_points[0] in plot
            and surrounding_points[1] not in plot
            and surrounding_points[2] in plot):
            return 1
        
        return 0


###################################################################################
solution = Solution()
dir_name = os.path.dirname(__file__)
filename = os.path.join(dir_name, 'puzzle_input.txt')

start = perf_counter()
solution.parse_input(filename)
(part1, part2) = solution.run()     
end = perf_counter()
print(f"Part 1 = {part1}")
print(f"Part 2 = {part2}")
print(f"Duration = {end - start}s")
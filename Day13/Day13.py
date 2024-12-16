from time import perf_counter
import os
import re

class ClawGameParams:
    def __init__(self, coord_A, coord_B, coord_prize):
        self.A = coord_A
        self.B = coord_B
        self.prize = coord_prize

class Solution:
    def __init__(self):
        self.claw_games = []
    
    def parse_input(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        # extract claw game params from the file
        values = []
        for line in lines:
            if line == "\n":
                # create a ClawGameParams
                claw_game = ClawGameParams((values[0], values[1]), (values[2], values[3]), (values[4], values[5]))
                self.claw_games.append(claw_game)
                values.clear()
            else:
                p = re.compile(r'\d+')
                found = p.findall(line)
                for val in found:
                    values.append(int(val))

        # create a ClawGameParams
        claw_game = ClawGameParams((values[0], values[1]), (values[2], values[3]), (values[4], values[5]))
        self.claw_games.append(claw_game)

    
    def part_one(self):
        total_tokens = 0
        for game in self.claw_games:
            total_tokens += self.play_game(game)
        return total_tokens


    def part_two(self):
        total_tokens = 0
        for game in self.claw_games:
            # first modify target
            game.prize = (10000000000000 + game.prize[0], 10000000000000 + game.prize[1])
            total_tokens += self.play_game(game)
        return total_tokens
    

    def play_game(self, game):
        # return the least number of tokens used - always only one token. Solve as simultaneous equation
        tokens = 0
        
        # solve for b
        numerator = game.prize[0] - ( game.prize[1] * game.A[0] ) / game.A[1]
        denominator = game.B[0] - ( game.B[1] * game.A[0] ) / game.A[1]
        b = numerator / denominator

        # check for rounding errors in float representation
        if abs(round(b) - b) < 0.0001:
            b = round(b)

        if b == int(b):
            # b is a whole number - find a
            a = ( game.prize[0] - game.B[0] * b ) / game.A[0]
            if abs(round(a) - a) < 0.000001:
                a = round(a)
                tokens = a * 3 + b
                 
        return tokens


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
from time import perf_counter
import math
import os

class Solution:
    def __init__(self):
        self.equations = {}
        self.failed_targets = []
        self.part1_sum = 0
        

    def parse_input(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            parts = line.split(': ')
            target = int(parts[0])
            values = parts[1].split(' ')
            nums = []
            for value in values:
                nums.append(int(value))

            # not sure if this situation occurs in the puzzle input...
            if (self.equations.get(target) is not None):
                raise Exception("Scenario where two equations need to result in the same number")

            self.equations[target] = nums


    def part_one(self):
        sum = 0
        for target in self.equations:
            if self.is_equation_valid(target, self.equations.get(target), ['+', '*']):
                sum += target
            else:
                self.failed_targets.append(target)
        self.part1_sum = sum
        return sum


    def part_two(self):
        sum = 0
        for target in self.failed_targets:
            if self.is_equation_valid(target, self.equations.get(target), ['+', '*', '||']):
                sum += target
        return self.part1_sum + sum
    

    def is_equation_valid(self, target, nums, operators):
        len_nums = len(nums)
        arr = []
        
        for i in range(len_nums):
            if i == 0:
                arr.append(nums[i])
            else:
                temp = arr.copy()
                arr.clear()
                for val in temp:
                    # the array size keeps increasing with each calculation - each time creating branch - one for each operation
                    for operator in operators:
                        if operator == '+':
                            arr.append(val + nums[i])
                        elif operator == '*':
                            arr.append(val * nums[i])
                        elif operator == '||':
                            arr.append(int(str(val)+str(nums[i])))
        return target in arr

#######################################################################
solution = Solution()
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'puzzle_input.txt')
solution.parse_input(filename)

start = perf_counter()
answer_part_one = solution.part_one()
print("Part 1 = ", answer_part_one)
answer_part_two = solution.part_two()
print("Part 2 = ", answer_part_two)
end = perf_counter()
print(f"Duration = {end - start}")

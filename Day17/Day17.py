from time import perf_counter
import os
import re

class Solution:
    def __init__(self):
        self.registerA = 0
        self.registerB = 0
        self.registerC = 0
        self.program = []
        self.output = []

    
    def parse_input(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        p = re.compile(r'\d+')
        self.registerA = int(p.findall(lines[0])[0])
        self.registerB = int(p.findall(lines[1])[0])
        self.registerC = int(p.findall(lines[2])[0])
        program = p.findall(lines[4])
        self.program = [int(item) for item in program]

    
    def part_one(self):
        instruction_pointer = 0
        
        while instruction_pointer < len(self.program) - 1:
            opcode = self.program[instruction_pointer]              # instruction
            literal_operand = self.program[instruction_pointer + 1] # input to instruction
            update_instruction_pointer = True

            # execute opcode instruction
            if opcode == 0:
                self.adv_instruction(literal_operand)
            elif opcode == 1:
                self.bxl_instruction(literal_operand)
            elif opcode == 2:
                self.bst_instruction(literal_operand)
            elif opcode == 3:
                jumped, new_instruction_pointer = self.jnz_instruction(literal_operand)
                if jumped:
                    update_instruction_pointer = False
                    instruction_pointer = new_instruction_pointer
            elif opcode == 4:
                self.bxc_instruction(literal_operand)
            elif opcode == 5:
                value = self.out_instruction(literal_operand)
                self.output.append(value)
            elif opcode == 6:
                self.bdv_instruction(literal_operand)
            elif opcode == 7:
                self.cdv_instruction(literal_operand)

            # jump to next position
            if update_instruction_pointer:
                instruction_pointer += 2

        # write the output values as a comma separated string
        print(f"A = {self.registerA}")
        print(f"B = {self.registerB}")
        print(f"C = {self.registerC}")
        return ','.join(map(str, self.output)) 


    def part_two(self):
        return 0
    

    def get_combo_operand(self, literal_operand):
        if literal_operand == 4:
            literal_operand = self.registerA
        elif literal_operand == 5:
            literal_operand = self.registerB
        elif literal_operand == 6:
            literal_operand = self.registerC

        return literal_operand          

    def adv_instruction(self, literal_operand):
        self.registerA = self.dv_instruction(literal_operand)

    def bxl_instruction(self, literal_operand):
        self.registerB = self.registerB ^ literal_operand   # bitwise XOR operation

    def bst_instruction(self, literal_operand):
        combo_operand = self.get_combo_operand(literal_operand)
        self.registerB = combo_operand % 8

    def jnz_instruction(self, literal_operand):
        jumped = False
        if self.registerA != 0:
            jumped = True
        return jumped, literal_operand

    def bxc_instruction(self, literal_operand):
        self.registerB = self.registerB ^ self.registerC   # bitwise XOR operation

    def out_instruction(self, literal_operand):
        combo_operand = self.get_combo_operand(literal_operand)
        return combo_operand % 8

    def bdv_instruction(self, literal_operand):
        self.registerB = self.dv_instruction(literal_operand)

    def cdv_instruction(self, literal_operand):
        self.registerC = self.dv_instruction(literal_operand)

    def dv_instruction(self, literal_operand):
        combo_operand = self.get_combo_operand(literal_operand)
        numerator = self.registerA
        denominator = pow(2, combo_operand)
        div = numerator//denominator        # floor division
        return div
    

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
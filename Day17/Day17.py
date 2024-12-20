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
        return ','.join(map(str, self.output)) 


    def part_two(self):
        last_op_code_index = len(self.program) - 2
        instruction_pointer = last_op_code_index
        program_index = len(self.program) - 1       # last index of the program code to iterate through in reverse
        value_a_found = False

        # TODO: think b and c need initial values when recursing backwards...
        # the tests only test using register A and instructions 0,5 4, Probably need to write my own tests to test the other instructions
        
        while value_a_found == False:

            opcode = self.program[instruction_pointer]              # instruction
            literal_operand = self.program[instruction_pointer + 1] # input to instruction

            # execute opcode instruction
            if opcode == 0:
                self.opp_adv_instruction(literal_operand)
            elif opcode == 1:
                self.bxl_instruction(literal_operand)
            elif opcode == 2:
                self.opp_bst_instruction(literal_operand)
            elif opcode == 3:
                # analysed the puzzle input - there are no jumping op codes except at the end to loop back to the beginning
                # check if the whole program has been iterated through backwards and used
                if program_index < 0:
                    break
            elif opcode == 4:
                self.bxc_instruction(literal_operand)
            elif opcode == 5:
                self.opp_out_instruction(literal_operand, self.program[program_index])
                program_index -= 1
            elif opcode == 6:
                self.opp_bdv_instruction(literal_operand)
            elif opcode == 7:
                self.opp_cdv_instruction(literal_operand)

            # jump to next position
            if instruction_pointer == 0:
                # loop back to end
                instruction_pointer = last_op_code_index
            else:
                instruction_pointer -= 2

        # write the output values as a comma separated string
        return self.registerA
    

    def get_combo_operand(self, literal_operand):
        if literal_operand == 4:
            literal_operand = self.registerA
        elif literal_operand == 5:
            literal_operand = self.registerB
        elif literal_operand == 6:
            literal_operand = self.registerC

        return literal_operand          

    # 0
    def adv_instruction(self, literal_operand):
        self.registerA = self.dv_instruction(literal_operand)

    def opp_adv_instruction(self, literal_operand):
        self.registerA = self.opp_dv_instruction(literal_operand)

    # 1 - inverse of XOR is XOR
    def bxl_instruction(self, literal_operand):
        self.registerB = self.registerB ^ literal_operand   # bitwise XOR operation

    # 2
    def bst_instruction(self, literal_operand):
        combo_operand = self.get_combo_operand(literal_operand)
        self.registerB = combo_operand & 7  # modulo 8 is same as AND 7

    def opp_bst_instruction(self, literal_operand):
        # self.registerB was overwritten in bst_instruction. No way to get what it was back
        self.registerB = 0

    #3 
    def jnz_instruction(self, literal_operand):
        jumped = False
        if self.registerA != 0:
            jumped = True
        return jumped, literal_operand

    # 4 - inverse of XOR is XOR
    def bxc_instruction(self, literal_operand):
        self.registerB = self.registerB ^ self.registerC   # bitwise XOR operation

    # 5
    def out_instruction(self, literal_operand):
        combo_operand = self.get_combo_operand(literal_operand)
        return combo_operand & 7 # modulo 8 is same as AND 7

    def opp_out_instruction(self, literal_operand, remainder):
        # the inverse would be to OR the remainder back to the value
        if literal_operand == 4:
            self.registerA = self.registerA | remainder
        elif literal_operand == 5:
            self.registerB = self.registerB | remainder
        if literal_operand == 6:
            self.registerC = self.registerC | remainder

    # 6
    def bdv_instruction(self, literal_operand):
        self.registerB = self.dv_instruction(literal_operand)

    def opp_bdv_instruction(self, literal_operand):
        self.registerB = self.opp_dv_instruction(literal_operand)

    # 7
    def cdv_instruction(self, literal_operand):
        self.registerC = self.dv_instruction(literal_operand)

    def opp_cdv_instruction(self, literal_operand):
        self.registerC = self.opp_dv_instruction(literal_operand)

    def dv_instruction(self, literal_operand):
        # dividing by 2^(combo_operand) and flooring the result is a bit shift right combo_operand number of times
        combo_operand = self.get_combo_operand(literal_operand)
        return self.registerA >> combo_operand
    
    def opp_dv_instruction(self, literal_operand):
        combo_operand = self.get_combo_operand(literal_operand)
        return self.registerA << combo_operand

###################################################################################
solution = Solution()
dir_name = os.path.dirname(__file__)
filename = os.path.join(dir_name, 'test2.txt')
solution.parse_input(filename)

start = perf_counter()
part1 = solution.part_one()
part2 = solution.part_two()
end = perf_counter()
print(f"Part 1 = {part1}")
print(f"Part 2 = {part2}")         
print(f"Duration = {end - start}s")


start = perf_counter()
diff = pow(2,48) - pow(2,45)
print(diff)
count = 0
for i in range(diff):
    count += 1

end = perf_counter()
print(f"Duration = {end - start}s")
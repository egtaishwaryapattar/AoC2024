
from time import perf_counter
import os

class Solution:
    def __init__(self):
        self.disk_map = ""
        self.blocks = {}    # key = the index, value = value stored at that index position
        self.blocks_copy = {}

    def parse_input(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            
        # the input is only one line  
        self.disk_map = lines[0]
        self.get_blocks(self.disk_map)
        self.blocks_copy = self.blocks.copy()
        
    def part_one(self):
        self.compact_files()
        return self.calculate_checksum()
        

    def part_two(self):
        # reset block dictionary from part 1
        self.blocks = self.blocks_copy.copy()
        self.compact_files_2()
        return self.calculate_checksum()
    

    def get_blocks(self, disk_map):
        # translate the disk map into the individual blocks
        disk_map_index = 0
        block_index = 0
        block_value = 0     # value to fill in the block

        while disk_map_index < len(disk_map):
            if disk_map_index % 2 == 0:
                value = block_value
                block_value += 1
            else:                   # modulo returns 1
                value = '.'
            
            for i in range(int(disk_map[disk_map_index])):
                self.blocks[block_index] = value
                block_index += 1

            disk_map_index += 1


    def compact_files(self):
        forward_index = 0
        reverse_index = len(self.blocks) - 1

        while forward_index < reverse_index:
            if self.blocks.get(forward_index) == '.':
                
                # find end value
                found_value = False
                while found_value == False:
                    end_value = self.blocks.get(reverse_index)
                    if end_value != '.':
                        found_value = True
                    else:
                        reverse_index -= 1
                        if reverse_index <= forward_index:
                            break
                
                if found_value:
                    # swap '.' and end value
                    self.blocks[forward_index] = end_value
                    self.blocks[reverse_index] = '.'
                    reverse_index -= 1

            forward_index += 1
    

    def compact_files_2(self):
        value_space_sizes = []
        disk_map_index = 0

        while disk_map_index < len(self.disk_map):
            if disk_map_index % 2 == 0:
                value_space_sizes.append(int(self.disk_map[disk_map_index]))
            disk_map_index += 1

        value = len(value_space_sizes) - 1        # NOTE: the VALUE also corresponds to the index to use for value_space_sizes to get how many times VALUE was outputted
        reverse_index = len(self.blocks) - 1

        # iterate backwards through the blocks
        while reverse_index > 0:

            # find index which has the value we are looking for
            block_value = self.blocks.get(reverse_index)
            while block_value != value:
                reverse_index -=1
                if reverse_index <= 0:
                    break
                else:
                    block_value = self.blocks.get(reverse_index)
            
            # get number of spaces the value occupies
            num_spaces = value_space_sizes[value]

            # iterate forwards through block, unit reverse_index, until a space block that fits is found
            i = 0
            consecutive_spaces = 0
            values_swapped = False
            while i < reverse_index:
                if self.blocks.get(i) == '.':
                    consecutive_spaces += 1

                    if consecutive_spaces == num_spaces:
                        # found a space block that would fit the values. Swap the value and '.'
                        for j in range(num_spaces):
                            self.blocks[i-j] = value
                            self.blocks[reverse_index] = '.'
                            reverse_index -=1
                        
                        values_swapped = True
                        break
                else:
                    consecutive_spaces = 0
                i += 1

            # if value is not found so reverse the index by the number of spaces it occupied
            if values_swapped == False:
                reverse_index = reverse_index - num_spaces
            
            # decrement the value to look for the next value
            value -= 1


    def calculate_checksum(self):
        checksum = 0

        for i in range(len(self.blocks)):
            value = self.blocks.get(i)
            if value == '.':
                value = 0
            
            checksum += value * i

        return checksum
        

#######################################################################
solution = Solution()
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'puzzle_input.txt')
solution.parse_input(filename)

start = perf_counter()
answer_part1 = solution.part_one()
print("Part1 = ", answer_part1)
answer_part2 = solution.part_two()
print("Part2 = ", answer_part2) 
end = perf_counter()
print(f"Duration = {end - start}")
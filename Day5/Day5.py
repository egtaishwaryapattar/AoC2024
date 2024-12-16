def check_element_safety(page_order_dict, nums, index):
    # if safe, return j = 0. else return the index it fails at
    nums_len = len(nums)
    values = page_order_dict.get(int(nums[index]))
    j = index + 1
    while j < nums_len:
        if (values is None) or (int(nums[j]) not in values):
            return j
        j += 1
    return 0

def check_line_safety(nums, start_index):
    nums_len = len(nums)
    i = start_index

    while i < nums_len - 1:
        unsafe_index = check_element_safety(page_order_dict, nums, i)
        if unsafe_index != 0:
            return [i, unsafe_index]
        i += 1
    
    return []

def get_middle_number(nums):
    middle_index = int((len(nums) + 1) / 2)
    return int(nums[middle_index - 1])

def get_corrected_line(nums, index1, index2):
    # swap the incorrect values
    value1 = nums[index1]
    value2 = nums[index2]
    nums[index1] = value2
    nums[index2] = value1

    # check if it is valid
    unsafe_indices = check_line_safety(nums, index1)
    safe = len(unsafe_indices) == 0
    if (safe):
        return nums
    else:
        return get_corrected_line(nums, unsafe_indices[0], unsafe_indices[1])

#######################################################################
with open('C:\SourceCode\AdventOfCode24\Day5\puzzle_input.txt', 'r') as f:
    lines = f.readlines()

populate_dictionary_complete = False
page_order_dict = {}
sum = 0
corrections = 0

for line in lines:
    if populate_dictionary_complete == False:

        if line == "\n":
            populate_dictionary_complete = True
        else:
            # populate the dictionary
            nums = line.split('|')
            num1 = int(nums[0])
            num2 = int(nums[1])

            values = page_order_dict.get(num1)
            if (values is not None):
                values.append(num2)
            else:
                values = [num2]
            
            # update dictionary
            page_order_dict[num1] = values

    else:
        # check which updates are in the correct order
        nums = line.split(',')
        unsafe_indices = check_line_safety(nums, 0)
        safe = len(unsafe_indices) == 0
        
        # if the whole line is safe, find the middle number
        if (safe):
            sum += get_middle_number(nums)
        else:
            corrected_line = get_corrected_line(nums, unsafe_indices[0], unsafe_indices[1])
            corrections += get_middle_number(corrected_line)
        
print("Part 1 = ", sum)
print("Part 2 = ", corrections)
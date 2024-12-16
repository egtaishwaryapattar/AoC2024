# open file
with open('C:\SourceCode\AdventOfCode24\Day1\sample.txt', 'r') as f:
    lines = f.readlines()

col1 = []
col2 = []

# parse contents into two lists
for line in lines:
    nums = line.split()
    col1.append(int(nums[0]))
    col2.append(int(nums[1]))

# sort lists in order
col1.sort()
col2.sort()

'''
### part 1
# find difference
sum = 0
count = len(col1)
index = 0

while index < count:
    sum += abs(col1[index] - col2[index])
    index = index + 1

# result
print(sum)
'''

# part 2
sum = 0
prevNum = 0;
prevMultiplier = 0

for num in col1:
    if (num == prevNum):
        sum += prevMultiplier
    else:
        # iterate through col2 and find num matches
        count = 0
        for num2 in col2:
            if (num2 == num):
                count += 1
        
        prevNum = num
        prevMultiplier = num * count
        sum += prevMultiplier

print(sum)
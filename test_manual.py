import os

print(os.environ)
print(f"we are just testing the manual vs the generated code effects")

# All things loking good so far. 

def two_sum(nums: list[int], target: int):
    lookup = {}
    for i, num in enumerate(nums):
        if target - num in lookup:
            return [lookup[target - num], i]
    lookup[num] = i
    return None

print(two_sum([2, 7, 11, 15], 9))



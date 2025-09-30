class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:
        curr_sum = 0
        result = [ ]
        for i in range(len(nums)):
            curr_sum = curr_sum + nums[i]
            result.append(curr_sum)
        return result
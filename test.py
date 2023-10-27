class Solution:
    def plusOne(self, digits: list[int]) -> list[int]:
        if len(digits) <= 1:
            int_1 = digits[0] + 1
            list_1 = []
            if int_1 >= 9:
                for i in str(int_1):
                    list_1.append(int(i))
                   
            
                list_1.append(int_1)

                list_1.pop(2)
                return 
            
            
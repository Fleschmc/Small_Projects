# I watched a youtube video on how to test new programmers practically
# They mentioned this test: Code the game FizzBuzz
# With a partner take turns counting numbers but if the number is
# Divisible by 3 instead say Fizz, if divisible by 5 say buzz, if both FizzBuzz
# 105 seems to be a good number for the second two attempts 

# First attempt going for speed rather than future proofing / cleanliness

def FizzBuzz(length = 15):
    for num in range(1, length + 1):
        if num % 3 == 0 and num % 5 == 0:
            print('FizzBuzz')
        elif num % 3 == 0:
            print('Fizz')
        elif num % 5 == 0:
            print('Buzz')
        else:
            print(num)


# Second Attempt working much more towards future proofing
# This would be easier to do with dictionaries but I figured the challenge
# Would be more difficult with lists 
# Not bothering to check for equality of list length

def FizzBuzz_list(length = 15, nums = [3, 5, 7, 9], words = ['Fizz', 'Buzz', 'Bizz', 'Fuzz']):
    output = ''
    for num in range(1, length + 1):
        output = ''.join([words[index] for index in [nums.index(_) for _ in nums if num % _ == 0]])
        if output: 
            print(output)
        else: 
            print(num)

# Third attempt just rewriting second attempt but with a dictionary instead of a list

def FizzBuzz_dict(length = 15, num_words = {3 : 'Fizz', 5 : 'Buzz', 7 : 'Bizz', 9 : 'Fuzz'}):
    output = ''
    for num in range(1, length + 1):
        output = ''.join([num_words[key] for key in num_words.keys() if num % key == 0])
        if output:
            print(output)
        else:
            print(num)
# Write a program that can map() to make a list whose elements are squares of numbers between 1 and 20 (both included).

# Lambda is an anonymous (nameless) function in Python, written using the lambda keyword instead of def.
# Syntax we use -> lambda arguments: expression
# Points to note:
# 1. lambda functions are one-liners i.e. no loops, no multiple statements.
# 2. it is used for short, throwaway functions.


nums_list = [i for i in range(1,21)]
squared_list = list(map(lambda x: x*x, nums_list))

print(f'Original list: {nums_list}')
print(f'Original list: {squared_list}')

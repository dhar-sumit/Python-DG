# Write a program using generator to print the numbers which can be divisible by 5 and 7 between 0 and n in comma separated form while n is input by console.

# a generator is a special type of function that allows us to produce values one at a time instead of creating them all at once in memory.
# it is like a lazy iterator, instead of returning with return, a generator uses yield.
# print_using_generator is a generator function because it uses yield, every time Python sees yield i, it pauses the function and returns that value to the caller.
# when we use list(print_using_generator(n)) Python automatically calls next(gen) in a loop until the generator is exhausted.

def print_using_generator(n):
    for i in range(n+1):
        if i % 5 == 0 and i % 7 == 0:
            yield i

n = int(input("Enter the value of 'n':"))

numbers = list(print_using_generator(n))

print(f"Values divisible by 5 and 7 are: \n{', '.join(map(str, numbers))}")


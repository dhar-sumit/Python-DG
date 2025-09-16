# Write an iterator class ReverseIter, that takes a list and iterates it from the reverse direction.

# an iterator is any object in Python that has an __iter__() method (returns the iterator object itself) and has a __next__() method (returns the next item, or raises StopIteration when done).
# python internally keeps calling __next__() until StopIteration is raised.

class ReverseIter:
    def __init__(self, given_list):
        self.given_list = given_list
        self.curr = len(given_list) - 1

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.curr >= 0:
            val = self.given_list[self.curr]
            self.curr -= 1
            return val
        else:
            raise StopIteration
    
my_list = [i for i in range(1, 16)]
final_list = ReverseIter(my_list)

print(', '.join(map(str, final_list)))
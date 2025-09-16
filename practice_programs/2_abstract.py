# ABC prevents misuse (creating meaningless base objects) and ensures the base class only serves as a template.
# @abstractmethod is a contract: it says any subclass of an abstract class must implement this method.

from abc import ABC, abstractmethod

class Person(ABC):
    @abstractmethod
    def get_gender(self): # this abstract method must be implemented by the child classes.
        pass

class Male(Person):
    def get_gender(self):
        return 'Male'

class Female(Person):
    def get_gender(self):
        return 'Female'

m = Male()
print(f'Child class "Male" returns get_gender: {m.get_gender()}\n')

f = Female()
print(f'Child class "Female" returns get_gender: {f.get_gender()}\n')

print(f'Throws error when we try to create obj of abstract class:')
try:
    p = Person()
except TypeError as e:
    print(f"Error: {e}")
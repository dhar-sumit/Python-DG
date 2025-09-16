# Write a program to generate a 3*5*8 3D array whose each element is 0.

# We are usng numpy for speed and performance.
import numpy as np

multi_dim_arr = np.zeros((3,5,8), dtype=int)
print(f"A 3*5*8 3D array:\n{multi_dim_arr}")

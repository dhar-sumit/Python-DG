# Write a binary search function which searches an item in a sorted list. The function should return the index of the element to be searched in the list.

def binary_search(given_list: list, choice: int, left: int, right: int):
    if left > right:
        return -1
    mid = (right-left)//2 + left

    if given_list[mid] == choice:
        return mid
    elif given_list[mid] > choice:
        return binary_search(given_list, choice, left, mid-1)
    else:
        return binary_search(given_list, choice, mid+1, right)

given_list = [int(i) for i in range(1, 11)]

choice = int(input("Enter the number to seach in between 1 to 10 (inclusively):"))

index = binary_search(given_list, choice, 0, len(given_list)-1)

print(f"For the list: {given_list}")
if index == -1:
    print(f"Item was not found for choice: {choice}.")
else:
    print(f"Item was found at index-'{index}' (0-based index), for choice {choice}.")
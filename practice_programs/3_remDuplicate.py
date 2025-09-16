# We are using set, so that we can keep track of visited numbers,
# and only appending the first occurance of any number.
# Thus the original order is reserved.

given_list = [12,24,35,24,88,120,155,88,120,155]

filter_list = []
visited = set()

for item in given_list:
    if item not in visited:
        visited.add(item)
        filter_list.append(item)

print(f'Original List: {given_list}')
print(f'After removing duplicates: {filter_list}')
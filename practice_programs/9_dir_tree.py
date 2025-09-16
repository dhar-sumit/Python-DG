# Implement a program dir_tree.py that takes a directory as argument and prints all the files in that directory recursively as a tree.
# Hint: Use os.listdir and os.path.isdir functions.

# We will be using 'os.path.isdir' to check whether it is a valid dir, then 'os.listdir' to get all the files and os.path.join(path, item) to join path with respective files.

import os

def extraxt_files_in_dir_and_print(path, indent=""):
    if not os.path.isdir(path):
        return
    
    items = os.listdir(path)

    for index, item in enumerate(items):
        itemPath = os.path.join(path, item)
        isLast = index==len(items)-1
        prefix = "└── " if isLast else "├── "
        print(indent + prefix + item)

        if os.path.isdir(itemPath):
            new_indent = indent + "    " if isLast else "│    "
            extraxt_files_in_dir_and_print(itemPath, new_indent)
    

dir_link = input("Enter the dir link, to see all the files present in it:")
extraxt_files_in_dir_and_print(dir_link)

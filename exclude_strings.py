"""
This script is written for bash function 'find_git_files'.
It is supposed to take arguments all_files, ignored, and unchanged;
then exclude the other two from all_files and print it.
"""

import sys

# Get the arguments from temporary files
all_files_file = sys.argv[1]
ignored_file = sys.argv[2]
unchanged_file = sys.argv[3]

# Read the contents of the temporary files
with open(all_files_file, 'r') as file:
    all_files_str = file.read().strip()

with open(ignored_file, 'r') as file:
    ignored_str = file.read().strip()

with open(unchanged_file, 'r') as file:
    unchanged_str = file.read().strip()

# Convert the newline-separated strings to sets
all_files = set(all_files_str.split("\n"))
ignored = set(ignored_str.split("|"))
unchanged = set(unchanged_str.split("|"))

# Remove ignored and unchanged elements from all_files
filtered_files = all_files - ignored - unchanged

# Convert the resulting set back to a newline-separated string
result_str = "\n".join(filtered_files)

# Print the resulting string
print(result_str)

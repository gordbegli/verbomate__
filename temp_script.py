import os
import re

# Current working directory
cwd = os.getcwd()

# Regular expression to match files that start with a number
pattern = re.compile(r"^\d")

# Iterate through the files in the current working directory
for filename in os.listdir(cwd):
    # Check if the file name starts with a number
    if pattern.match(filename):
        # Construct the full file path
        file_path = os.path.join(cwd, filename)
        # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            try:
                # Delete the file
                os.remove(file_path)
                print(f"Deleted file: {filename}")
            except Exception as e:
                print(f"Failed to delete file: {filename}. Reason: {e}")
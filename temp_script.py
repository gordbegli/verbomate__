import os

# Specify the file name
file_name = "hello_world.txt"

# Check if file exists
if os.path.isfile(file_name):
    # Delete the file
    os.remove(file_name)
    print(f"The file '{file_name}' has been deleted.")
else:
    # The file does not exist
    print(f"The file '{file_name}' does not exist.")
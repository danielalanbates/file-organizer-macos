import os
os.chdir("/Users/daniel/Documents/Code/Python/9.25")

# Change to the desired directory and create a new directory
try:
    target_dir = "/Users/daniel/Documents/Code/Python/9.25"
except FileNotFoundError:
    print(f"Directory does not exist.")
    
file_name = "test.txt"
file_content = "This is a test file."

# Create directories if they don't exist
try:
    os.mkdir("new_dir")
except FileExistsError:
    print(f"Directory already exists.")
except OSError as e:
    print(f"An error occurred: {e}")

try:
    with open(file_name, "w") as f:
        f.write(file_content)
    print(f"File '{file_name}' created.")
except OSError as e:
    print(f"An error occurred: {e}")

# List all files and directories in the specified path
for name in os.listdir(target_dir):
    fullname = os.path.join(target_dir, name)
    if os.path.isdir(fullname):
        print("{} is a directory.".format(fullname))
    else:
         print("{} is a file".format(fullname))
import sys

try:
    input_file = sys.argv[1]
except IndexError:
    print("please provide a file")
    exit(1)

try:
    file = open(input_file, 'r')
except FileNotFoundError:
    print("File doesn't exists")
    exit(404)
except IsADirectoryError:
    print("Not a file, it is a directory")
    exit(1)

Lines = file.readlines()
count = 0
linecount = 0
for line in Lines:
    count += len(line.strip())
    linecount += 1

print(f"Word Count: {count}")
print(f"Line Count: {linecount}")
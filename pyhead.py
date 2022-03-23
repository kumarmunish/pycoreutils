import sys

line_count = 10
try:
    input_file = sys.argv[1]
except IndexError:
    print("please provide a file")
    exit(1)

if len(sys.argv) == 3:
    try:
        line_count = int(sys.argv[1])
    except ValueError:
        print("provide a valid number")

    input_file = sys.argv[2]
try:
    file = open(input_file, 'r')
except FileNotFoundError:
    print("file doesn't exist")
    exit(1)

lines = file.readlines()

for i in range(line_count):
    print(lines[i], end='')







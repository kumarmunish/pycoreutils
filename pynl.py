import sys

try:
    input_file = sys.argv[1]
except IndexError:
    print("please provide a file")
    exit(1)

file = open(input_file, 'r')

lines = file.readlines()

number = 1
for line in lines:
    if line != "\n":
        print('\t' + str(number) + " " + line.strip())
        number += 1
    else:
        print(line.strip())

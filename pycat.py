import sys

try:
    input_file = sys.argv[1]
except IndexError:
    print("please provide a file")
    exit(1)

file = open(input_file, 'r')
lines = file.readlines()

text = ''
for line in lines:
    text += line

print(text)

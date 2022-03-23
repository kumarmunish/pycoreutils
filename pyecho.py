import sys

try:
    text = sys.argv[1]
except:
    print("")
    exit(1)


if len(sys.argv) > 2:
    text = ''.join(string for string in sys.argv[1:])

print(text)
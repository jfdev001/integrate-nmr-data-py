s = "c/path/to/file.txt"

ss = "".join(reversed(s[-1:s.rfind("/"):-1]))

print("Output:")
print(s)
print()
print(ss)
print()
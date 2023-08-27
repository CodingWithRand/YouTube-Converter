import re

file_name = "FARCRY4 - ผจญภัย (หรือว่าผจญมารหว่า)"
escaped_file_name = re.escape(file_name)
print(escaped_file_name)
text = "This is a test ไทย string"
match = re.search(escaped_file_name, text, re.UNICODE)
print(match)
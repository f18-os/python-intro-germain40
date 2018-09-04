import re

d = {}
words = []
fileIn = open("speech.txt", 'r')
# makes everything lower case for case-insensitive
lfile = fileIn.read().lower()
# clean the file
words = re.sub('[^a-zA-Z0-9]', ' ', lfile).split()
words.sort()
fileIn.close()
for w in words:
    if w not in d:
        d[w] = 1
    else:
        d[w] += 1
fileOut = open("outPut.txt", 'w')
for k, v in d.items():
    fileOut.write(k + " " + str(v) + "\n")
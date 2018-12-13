import os

moduleFileList = os.listdir("./util")
moduleMap = {}

for file in moduleFileList:
    name = file[:file.index(".glsl")]
    f = open("./util/" + file, "r")
    moduleMap[name] = f.read()
    f.close()

print(moduleMap)

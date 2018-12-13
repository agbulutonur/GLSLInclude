import os
import re
import pathlib
import sys
import getopt


def getOptionVars():
    baseDirectory = "."
    baseModuleDirectory = "./util"

    options, remainder = getopt.getopt(sys.argv[1:], 'o:v', [ 'base=', 'module=' ])

    for opt, arg in options:
        if opt == "--base":
            baseDirectory = arg
        if opt == "--module":
            baseModuleDirectory = arg

    return baseDirectory, baseModuleDirectory


def load_modules(module_files, dir):
    moduleMap = {}
    for file in module_files:
        name = file[:file.index(".glsl")]
        f = open(os.path.normpath(dir + "/" + file), "r")
        moduleMap[name] = f.read()
        f.close()

    return moduleMap


if __name__ == "__main__":

    baseDirectory, baseModuleDirectory = getOptionVars()

    moduleFileList = os.listdir(baseModuleDirectory)
    moduleMap = load_modules(moduleFileList, baseModuleDirectory)

    outputFile = "output"
    pathlib.Path(outputFile).mkdir(exist_ok=True)

    fileList = os.listdir()
    shaderList = [f for f in fileList if f.endswith(".glsl")]
    regex_word="\#include\s+(.*)$"
    for shader in shaderList:
        with open(shader) as fh:
            newFile = open(outputFile + "/" + shader, "w")
            for line in fh:
                toWrite = line
                if line.startswith("#include"):
                    m = re.search(regex_word, line)
                    module = m.group(1)
                    line = moduleMap[module]
                newFile.write(line)
            newFile.close()
            fh.close()

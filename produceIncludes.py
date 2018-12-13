import os
import re
import pathlib
import sys
import getopt


def get_option_vars():
    base_dir = "."
    module_dir = "./util"

    options, remainder = getopt.getopt(sys.argv[1:], 'o:v', [ 'base=', 'module=' ])

    for opt, arg in options:
        if opt == "--base":
            base_dir = arg
        if opt == "--module":
            module_dir = arg

    return base_dir, module_dir


def load_modules(module_files, directory):
    modules = {}
    for file in module_files:
        name = file[:file.index(".glsl")]
        f = open(os.path.normpath(directory + "/" + file), "r")
        modules[name] = f.read()
        f.close()

    return modules


if __name__ == "__main__":

    baseDirectory, baseModuleDirectory = get_option_vars()

    moduleFileList = os.listdir(baseModuleDirectory)
    modulesMap = load_modules(moduleFileList, baseModuleDirectory)

    outputFile = "output"
    pathlib.Path(outputFile).mkdir(exist_ok=True)

    fileList = os.listdir()
    shaderList = [f for f in fileList if f.endswith(".glsl")]
    regexWord = "\#include\s+(.*)$"

    for shader in shaderList:
        with open(shader) as sh:
            newFile = open(outputFile + "/" + shader, "w")
            for line in sh:
                toWrite = line
                if line.startswith("#include"):
                    m = re.search(regexWord, line)
                    module = m.group(1)
                    line = modulesMap[module]
                newFile.write(line)
            newFile.close()
            sh.close()

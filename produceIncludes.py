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


def find_folders(path):
    for fname in os.listdir(path):
        dirToCheck = os.path.join(path, fname)
        if os.path.isdir(dirToCheck):
            yield dirToCheck


def produce_output_folders(folder_list, out_folder):
    for f in folder_list:
        new_folder = out_folder + "/" + f
        pathlib.Path(new_folder).mkdir(exist_ok=True)


if __name__ == "__main__":

    baseDirectory, baseModuleDirectory = get_option_vars()

    moduleFileList = os.listdir(baseModuleDirectory)
    modulesMap = load_modules(moduleFileList, baseModuleDirectory)

    outputFolder = "output"
    pathlib.Path(outputFolder).mkdir(exist_ok=True)

    # fileList = os.listdir(baseDirectory)
    fileList = [baseDirectory] + list(find_folders(baseDirectory))
    fileList = [f for f in fileList if not (f.endswith(baseModuleDirectory) or f.endswith(outputFolder))]

    regexWord = "\#include\s+(.*)$"

    produce_output_folders(fileList, outputFolder)

    for folder in fileList:
        fList = os.listdir(folder)
        shaderList = [os.path.normpath(folder + '/' + f) for f in fList if f.endswith(".glsl")]
        for shader in shaderList:
            with open(shader) as shaderFile:
                newFile = open(outputFolder + "/" + shader, "w")
                for line in shaderFile:
                    toWrite = line
                    if line.startswith("#include"):
                        m = re.search(regexWord, line)
                        module = m.group(1)
                        line = modulesMap[module]
                    newFile.write(line)
                newFile.close()
                shaderFile.close()

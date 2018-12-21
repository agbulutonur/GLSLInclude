#!/usr/bin/python

import os
import re
import pathlib
import sys
import getopt

regex_word = "\#include\s+(.*)$"


def get_option_vars():
    base_dir = "."
    module_dir = "./util"
    output_folder = "output"

    options, remainder = getopt.getopt(sys.argv[1:], 'o:v', [ 'base=', 'module=', 'output=' ])

    for opt, arg in options:
        if opt == "--base":
            base_dir = arg
        if opt == "--module":
            module_dir = arg
        if opt == "--output":
            output_folder = arg

    return base_dir, module_dir, output_folder


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
        dir_to_check = os.path.join(path, fname)
        if os.path.isdir(dir_to_check):
            yield dir_to_check


def produce_output_folders(folder_list, out_folder):
    pathlib.Path(out_folder).mkdir(exist_ok=True)
    for f in folder_list:
        new_folder = out_folder + "/" + f
        pathlib.Path(new_folder).mkdir(exist_ok=True)


def produce_new_shader(output_folder, old_shader):
    with open(old_shader) as shader_file:
        new_file = open(output_folder + "/" + old_shader, "w")
        for line in shader_file:
            to_write = line
            if line.startswith("#include"):
                m = re.search(regex_word, line)
                module = m.group(1)
                to_write = modulesMap[module]
            new_file.write(to_write)
        new_file.close()
    shader_file.close()


if __name__ == "__main__":

    baseDirectory, baseModuleDirectory, outputFolder = get_option_vars()
    moduleFileList = os.listdir(baseModuleDirectory)
    modulesMap = load_modules(moduleFileList, baseModuleDirectory)

    fileList = [baseDirectory] + list(find_folders(baseDirectory))
    fileList = [f for f in fileList if not (f.endswith(baseModuleDirectory) or f.endswith(outputFolder))]

    produce_output_folders(fileList, outputFolder)

    for folder in fileList:
        fList = os.listdir(folder)
        shaderList = [os.path.normpath(folder + '/' + f) for f in fList if f.endswith(".glsl")]
        for shader in shaderList:
            produce_new_shader(outputFolder, shader)
    print("New shaders are produced successfully!")


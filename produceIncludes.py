import os


def load_modules(module_files):
    moduleMap = {}
    for file in module_files:
        name = file[:file.index(".glsl")]
        f = open("./util/" + file, "r")
        moduleMap[name] = f.read()
        f.close()

    return moduleMap


if __name__ == "__main__":
    moduleFileList = os.listdir("./util")
    moduleMap = loadModules(moduleFileList)

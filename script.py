from converter import createDatabaseDir
from converter import convert
from converter import dataFolder
import os
import glob

dataFolder = os.path.abspath('') + "/data/"


def main():
    filePaths = glob.glob(dataFolder + "*.json")
    convert(filePaths=filePaths)


if __name__ == "__main__":
    createDatabaseDir()
    main()

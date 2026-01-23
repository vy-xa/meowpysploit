import os as modOs
import sys as modSys

modSys.path.append(modOs.path.dirname(__file__))

from utils import clsInjector

if __name__ == '__main__':
    objInjector = clsInjector()
    objInjector.fnWaitForRoblox()
    if objInjector.fnInject():
        print("𐔌՞. .՞𐦯 enjoy!")

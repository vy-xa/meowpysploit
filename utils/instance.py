from globals import *
from .bytecode import clsScriptBytecode
from .memory import fnDerefPtr, fnReadRobloxString

class clsInstance:

    def __init__(self, objPm, intAddr):
        self.objPm = objPm
        self.intAddr = int(intAddr) if intAddr else 0
        self.strName = self.fnGetName()
        self.strClassName = self.fnGetClassName()
        self.intParent = self.fnGetParent()

    def fnGetNameAddr(self):
        return fnDerefPtr(self.objPm, self.intAddr + intInstanceNameOffset)

    def fnGetName(self):
        return fnReadRobloxString(self.objPm, self.fnGetNameAddr())

    def fnGetClassName(self):
        intMeta = fnDerefPtr(self.objPm, self.intAddr + intInstanceMetadataPtr)
        if not intMeta:
            return ''
        intExpAddr = fnDerefPtr(self.objPm, intMeta + intInstanceMetadataNamePtr)
        return fnReadRobloxString(self.objPm, intExpAddr)

    def fnGetParent(self):
        return fnDerefPtr(self.objPm, self.intAddr + intInstanceParentOffset)

    def fnListChildren(self):
        lstChildren = []
        intStart = fnDerefPtr(self.objPm, self.intAddr + intInstanceChildrenOffset)
        if intStart == 0:
            return lstChildren
        intEnd = fnDerefPtr(self.objPm, intStart + intChildListEndNextPtr)
        intCur = fnDerefPtr(self.objPm, intStart + intChildListStartNextPtr)
        if intCur == 0 or intEnd == 0:
            return lstChildren
        for _ in range(9000):
            if intCur == intEnd:
                break
            try:
                intChildAddr = self.objPm.read_longlong(intCur)
            except Exception:
                break
            if not intChildAddr:
                break
            lstChildren.append(clsInstance(self.objPm, intChildAddr))
            intCur += intChildListNodeStride
        return lstChildren

    def fnFindFirstChild(self, strChildName):
        for objInstChild in self.fnListChildren():
            if objInstChild.strName == strChildName:
                return objInstChild
        return None

    def fnFindFirstClass(self, strClassName):
        for objInstChild in self.fnListChildren():
            if objInstChild.strClassName == strClassName:
                return objInstChild
        return None

    def fnUnlock(self):
        intOfsIsCore = intModuleIsCoreOffset
        intOfsModuleFlags = intOfsIsCore - intModuleFlagsOffsetDelta
        if self.strClassName != "ModuleScript":
            raise RuntimeError(f"{self.strName} is not a modulescript")
        try:
            blnSuccessFlags = self.objPm.write_longlong(self.intAddr + intOfsModuleFlags, 0x100000000)
            blnSuccessCore = self.objPm.write_longlong(self.intAddr + intOfsIsCore, 0x1)
            if blnSuccessFlags and blnSuccessCore:
                return True
        except Exception:
            print(f"𐔌՞. .՞𐦯 failed to unlock {self.strName}")
        return True

    def fnSpoofWith(self, intInstancePtr):
        self.objPm.write_longlong(self.intAddr + 0x8, intInstancePtr)

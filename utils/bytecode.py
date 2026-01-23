from globals import *

class clsScriptBytecode:
    def __init__(self, objPm, intAddr):
        self.objPm = objPm
        self.intAddr = int(intAddr) if intAddr else 0
        self.bytOldBytes = None

    @property
    def bytBytecode(self):
        intPtr = self.objPm.read_longlong(self.intAddr + intScriptBytecodeMetaPtr)
        if not intPtr:
            return b''
        intBytecodePtr = self.objPm.read_longlong(intPtr + intScriptBytecodePtrInMeta)
        intSize = self.intSize
        if not intBytecodePtr or intSize <= 0:
            return b''
        try:
            return self.objPm.read_bytes(intBytecodePtr, intSize)
        except Exception:
            return b''

    @bytBytecode.setter
    def bytBytecode(self, bytVal):
        if not isinstance(bytVal, (bytes, bytearray)):
            raise TypeError('Value must be bytes or bytearray')
        try:
            self.bytOldBytes = self.objPm.read_bytes(self.intAddr + intScriptBytecodeMetaPtr)
        except Exception:
            self.bytOldBytes = None
        intValSize = len(bytVal)
        try:
            intAlloc = self.objPm.allocate(intValSize)
        except Exception:
            intAlloc = None
        if not intAlloc:
            raise RuntimeError('memory allocation failed')
        self.objPm.write_bytes(intAlloc, bytes(bytVal), intValSize)
        intPtr = self.objPm.read_longlong(self.intAddr + intScriptBytecodeMetaPtr)
        if not intPtr:
            raise RuntimeError('ptr not found for bytecode patch')
        self.objPm.write_longlong(intPtr + intScriptBytecodePtrInMeta, intAlloc)
        self.objPm.write_long(intPtr + intScriptBytecodeSizeInMeta, intValSize)

    @property
    def intSize(self):
        try:
            intPtr = self.objPm.read_longlong(self.intAddr + intScriptBytecodeMetaPtr)
            if not intPtr:
                return 0
            return self.objPm.read_long(intPtr + intScriptBytecodeSizeInMeta)
        except Exception:
            return 0

    def fnRestore(self):
        if self.bytOldBytes is not None:
            try:
                self.objPm.write_bytes(self.intAddr + intScriptBytecodeMetaPtr, self.bytOldBytes, len(self.bytOldBytes))
            except Exception:
                pass

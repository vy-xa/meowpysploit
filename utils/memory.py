import os as modOs
from pymem.process import module_from_name as fnModuleFromName
from globals import *

def fnGetDataModel(objPm):
    try:
        intBaseAddr = objPm.base_address
    except Exception:
        try:
            objMod = fnModuleFromName(objPm.process_handle, "RobloxPlayerBeta.exe")
            intBaseAddr = getattr(objMod, 'lpBaseOfDll', None)
        except Exception:
            intBaseAddr = None
    if not intBaseAddr:
        raise RuntimeError('base address not found')

    intFakeDm = objPm.read_longlong(intBaseAddr + intDatamodelFakePtrOffset)
    if not intFakeDm:
        return 0
    return objPm.read_longlong(intFakeDm + intDatamodelPtrInFake)

def fnReadRobloxString(objPm, intAddr):
    if not intAddr:
        return ''
    try:
        intLen = objPm.read_int(intAddr + intRobloxStringLengthOffset)
    except Exception:
        return ''
    if intLen > 15:
        try:
            intPtr = fnDerefPtr(objPm, intAddr)
            return objPm.read_string(intPtr, intLen)
        except Exception:
            return ''
    try:
        return objPm.read_string(intAddr, intLen)
    except Exception:
        return ''

def fnDerefPtr(objPm, intAddr, blnIs64=True):
    if not intAddr:
        return 0
    try:
        if blnIs64:
            bytPtr = objPm.read_bytes(intAddr, 8)
            return int.from_bytes(bytPtr, 'little')
        bytPtr = objPm.read_bytes(intAddr, 4)
        return int.from_bytes(bytPtr, 'little')
    except Exception:
        return 0

def fnClearDetection():
    # this makes completely ud!!
    try:
        strUserName = modOs.getlogin()
    except Exception:
        strUserName = modOs.environ.get('USERNAME', '')
    strLogPath = f'C:/Users/{strUserName}/AppData/Local/Roblox/logs'
    try:
        for strFileName in modOs.listdir(strLogPath):
            try:
                modOs.remove(modOs.path.join(strLogPath, strFileName))
            except Exception:
                pass
    except Exception:
        pass

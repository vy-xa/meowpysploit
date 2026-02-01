import ctypes as modCtypes
import time as modTime
import os as modOs
import psutil as modPsutil
import struct as modStruct
import traceback as modTraceback
import keyboard as modKeyboard
from pymem.process import module_from_name as fnModuleFromName
from utils.CyLuau import CyLuauBytecode as clsCyLuauBytecode
from tkinter import messagebox as fnMessageBox, Tk as clsTk

from globals import *
from .memory import fnGetDataModel, fnReadRobloxString, fnDerefPtr, fnClearDetection
from .bytecode import clsScriptBytecode
from .instance import clsInstance
from .signing import fnSignBytecode

class clsInjector:
    def __init__(self):
        import pymem as modPymem
        self.objPm = modPymem.Pymem()
        self.objByteHelper = clsCyLuauBytecode()
        self.fnSetupConsole()

    def fnSetupConsole(self):
        objCtWindll = modCtypes.windll
        modOs.system('cls' if modOs.name == 'nt' else 'clear')
        try:
            objCtWindll.kernel32.SetConsoleTitleW('𐔌՞. .՞𐦯')
        except Exception:
            pass

    def fnWaitForRoblox(self):
        print('𐔌՞. .՞𐦯 waiting for roblox...')
        while True:
            if self.fnWaitForProgram("RobloxPlayerBeta.exe", True, 60):
                break
        print('𐔌՞. .՞𐦯 roblox found!')

    def fnWaitForProgram(self, strProcName, blnAutoOpen=False, intLimit=60):
        intCount = 0
        while intCount <= intLimit:
            for objProc in modPsutil.process_iter():
                try:
                    if objProc.name() == strProcName:
                        if blnAutoOpen:
                            try:
                                self.objPm.open_process_from_id(objProc.pid)
                            except Exception:
                                pass
                        return True
                except Exception:
                    continue
            modTime.sleep(1)
            intCount += 1
        print('𐔌՞. .՞𐦯 error: program timed out')
        return False

    def fnKillCrashHandler(self):
        for objProc in modPsutil.process_iter():
            try:
                if objProc.name() == 'RobloxCrashHandler.exe':
                    objProc.kill()
            except Exception:
                pass

    def fnInject(self):
        try:
            self.fnKillCrashHandler()
            intGameAddr = fnGetDataModel(self.objPm)
            if not intGameAddr:
                raise RuntimeError('datamodel not found')
            objInstGame = clsInstance(self.objPm, intGameAddr)

            objInstCoreGui = objInstGame.fnFindFirstChild('CoreGui')
            if not objInstCoreGui:
                raise RuntimeError('coregui not found')

            objInstRobloxGui = objInstCoreGui.fnFindFirstChild('RobloxGui')
            if not objInstRobloxGui:
                raise RuntimeError('robloxgui not found')

            objInstModules = objInstRobloxGui.fnFindFirstChild('Modules')
            if not objInstModules:
                raise RuntimeError('modules not found')

            objInstPlayerList = objInstModules.fnFindFirstChild('PlayerList')
            if not objInstPlayerList:
                raise RuntimeError('playerlist not found')

            objInstPlayerListMgr = objInstPlayerList.fnFindFirstChild('PlayerListManager')
            if not objInstPlayerListMgr:
                raise RuntimeError('playerlistmanager not found')

            objInstCommon = objInstModules.fnFindFirstChild('Common')
            objInstCarrier = None
            if objInstCommon:
                 objInstCarrier = objInstCommon.fnFindFirstChild('HumanoidReadyUtil')
                 if not objInstCarrier:
                     objInstCarrier = objInstCommon.fnFindFirstChild('PolicyService')

            if not objInstCarrier:
                objInstStarterPlayer = objInstGame.fnFindFirstChild('StarterPlayer')
                if not objInstStarterPlayer:
                    raise RuntimeError('starterplayer not found')
                objInstStarterPlayerScripts = objInstStarterPlayer.fnFindFirstChild('StarterPlayerScripts')
                if not objInstStarterPlayerScripts:
                    raise RuntimeError('starterplayerscripts not found')
                objInstPlayerModule = objInstStarterPlayerScripts.fnFindFirstChild('PlayerModule')
                if not objInstPlayerModule:
                    raise RuntimeError('player module not found')
                objInstControlModule = objInstPlayerModule.fnFindFirstChild('ControlModule')
                if not objInstControlModule:
                    raise RuntimeError('control module not found')
                objInstCarrier = objInstControlModule.fnFindFirstChild('VRNavigation')
                if not objInstCarrier:
                    raise RuntimeError('carrier module not found')

            objInstCarrier.fnUnlock()
            objInstPlayerListMgr.fnUnlock()
            
            strBasePath = modOs.path.join(modOs.path.dirname(__file__), 'scripts')
            strScriptPath = modOs.path.join(strBasePath, 'script.lua')
            
            strFinalScript = ""
            with open(strScriptPath, 'r') as objFileScript:
                strFinalScript += objFileScript.read()

            fnCompileAttr = getattr(self.objByteHelper, 'compile', None)
            strScriptCode = "script.Parent=nil;task.spawn(function()" + strFinalScript + "\nend);while true do task.wait(9e9) end"
            bytCompiled = fnCompileAttr(strScriptCode)
            bytSignedCompressed = fnSignBytecode(bytCompiled)
            objScriptBC = clsScriptBytecode(self.objPm, objInstCarrier.intAddr)
            objScriptBC.bytBytecode = bytSignedCompressed

            objInstPlayerListMgr.fnSpoofWith(objInstCarrier.intAddr)
            try:
                hwnd = modCtypes.windll.user32.FindWindowW(None, "Roblox")
                if hwnd:
                    modCtypes.windll.user32.SetForegroundWindow(hwnd)
                    modTime.sleep(0.1)
                    modKeyboard.press_and_release('esc')
            except Exception:
                pass
            modTime.sleep(1)
            objInstPlayerListMgr.fnSpoofWith(objInstPlayerListMgr.intAddr)
            modTime.sleep(0.5)
            try:
                if 'objScriptBC' in locals() and objScriptBC is not None:
                    objScriptBC.fnRestore()
            except Exception:
                pass

            fnClearDetection()
            try:
                objRootTk = clsTk()
                objRootTk.withdraw()
                objRootTk.destroy()
            except Exception:
                pass
            return True
        except Exception as objE:
            try:
                print("𐔌՞. .՞𐦯 error:", str(objE))
                modTraceback.print_exc()
                objRootTk = clsTk()
                objRootTk.withdraw()
                objRootTk.destroy()
            except Exception:
                pass
            return False

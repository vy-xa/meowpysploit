import json
import urllib.request

intScriptBytecodeSizeInMeta = 0x20

intDatamodelFakePtrOffset = 0x0
intDatamodelPtrInFake = 0x0
intScriptBytecodeMetaPtr = 0x0
intScriptBytecodePtrInMeta = 0x0
intRobloxStringLengthOffset = 0x0
intInstanceNameOffset = 0x0
intInstanceChildrenOffset = 0x0
intInstanceParentOffset = 0x0
intInstanceMetadataPtr = 0x0
intInstanceMetadataNamePtr = 0x0
intChildListEndNextPtr = 0x0

intModuleIsCoreOffset = 0x188
intModuleFlagsOffsetDelta = 0x4

intChildListStartNextPtr = 0x0
intChildListNodeStride = 0x10

def fetch():
    global intDatamodelFakePtrOffset, intDatamodelPtrInFake, intScriptBytecodeMetaPtr, intScriptBytecodePtrInMeta
    global intRobloxStringLengthOffset, intInstanceNameOffset, intInstanceChildrenOffset
    global intInstanceParentOffset, intInstanceMetadataPtr, intInstanceMetadataNamePtr
    global intChildListEndNextPtr

    url = "https://offsets.ntgetwritewatch.workers.dev/offsets.json"
    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    )
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())

                def get_offset(key, default):
                    val = data.get(key)
                    if val is not None:
                        return int(val, 16)
                    return default

                intDatamodelFakePtrOffset = get_offset("FakeDataModelPointer", intDatamodelFakePtrOffset)
                intDatamodelPtrInFake = get_offset("FakeDataModelToDataModel", intDatamodelPtrInFake)
                intScriptBytecodeMetaPtr = get_offset("ModuleScriptByteCode", intScriptBytecodeMetaPtr)
                intScriptBytecodePtrInMeta = get_offset("ModuleScriptBytecodePointer", intScriptBytecodePtrInMeta)
                
                intRobloxStringLengthOffset = get_offset("StringLength", intRobloxStringLengthOffset)
                
                intInstanceNameOffset = get_offset("Name", intInstanceNameOffset)
                intInstanceChildrenOffset = get_offset("Children", intInstanceChildrenOffset)
                intInstanceParentOffset = get_offset("Parent", intInstanceParentOffset)
                
                intInstanceMetadataPtr = get_offset("ClassDescriptor", intInstanceMetadataPtr)
                intInstanceMetadataNamePtr = get_offset("ClassDescriptorToClassName", intInstanceMetadataNamePtr)
                
                intChildListEndNextPtr = get_offset("ChildrenEnd", intChildListEndNextPtr)
                
                print("fetched offsets :3")
            else:
                print(f"failed to fetch offsets, code: {response.status}")
    except Exception as e:
        print(f"error: {e}")

fetch()

__all__ = [
    'intDatamodelFakePtrOffset', 'intDatamodelPtrInFake',
    'intScriptBytecodeMetaPtr', 'intScriptBytecodePtrInMeta', 'intScriptBytecodeSizeInMeta',
    'intRobloxStringLengthOffset',
    'intInstanceNameOffset', 'intInstanceChildrenOffset', 'intInstanceParentOffset',
    'intInstanceMetadataPtr', 'intInstanceMetadataNamePtr',
    'intModuleIsCoreOffset', 'intModuleFlagsOffsetDelta',
    'intChildListStartNextPtr', 'intChildListEndNextPtr', 'intChildListNodeStride'
]

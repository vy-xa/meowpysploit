import json
import urllib.request

# these are hardcoded bcuz the offsets api no has :c
intScriptBytecodeSizeInMeta = 0x20

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
    try:
        with urllib.request.urlopen(url) as response:
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
                print(f"failed to fetch offsets code: {response.status}")
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

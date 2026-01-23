import struct as modStruct
import zstandard as modZstd
import xxhash as modXxhash
import blake3 as modBlake3

BYT_BYTECODE_SIGNATURE = b'RSB1'
INT_BYTECODE_HASH_MULTIPLIER = 41
INT_BYTECODE_HASH_SEED = 42
INT_MAGIC_A = 0x4C464F52
INT_MAGIC_B = 0x946AC432
TUP_KEY_BYTES = (0x52, 0x4F, 0x46, 0x4C)

def fnRotl8(intValue, intShift):
    intShift &= 7
    return ((intValue << intShift) & 0xFF) | ((intValue & 0xFF) >> (8 - intShift))

def fnCompressBytecode(bytBytecode):
    if not isinstance(bytBytecode, (bytes, bytearray)):
        bytBytecode = bytBytecode.encode('utf-8')
    objCompressor = modZstd.ZstdCompressor(level=modZstd.MAX_COMPRESSION_LEVEL)
    bytCompressed = objCompressor.compress(bytBytecode)
    bytSizeLe = modStruct.pack('<I', len(bytBytecode))
    bytBuffer = bytearray()
    bytBuffer += BYT_BYTECODE_SIGNATURE
    bytBuffer += bytSizeLe
    bytBuffer += bytCompressed
    intHashKey = modXxhash.xxh32(bytBuffer, seed=INT_BYTECODE_HASH_SEED).intdigest()
    bytBytesHash = modStruct.pack('<I', intHashKey)
    for i in range(len(bytBuffer)):
        bytBuffer[i] ^= (bytBytesHash[i % 4] + i * INT_BYTECODE_HASH_MULTIPLIER) & 0xFF
    return bytes(bytBuffer)

def fnSignBytecode(bytBytecode):
    if not bytBytecode:
        return b''
    if not isinstance(bytBytecode, (bytes, bytearray)):
        bytBytecode = bytBytecode.encode('utf-8')
    objHasher = modBlake3.blake3()
    objHasher.update(bytBytecode)
    bytBlake3Hash = objHasher.digest()
    bytTransformed = bytearray(32)
    for i in range(32):
        intByte = TUP_KEY_BYTES[i & 3]
        intHashByte = bytBlake3Hash[i]
        intCombined = (intByte + i) & 0xFF
        intMode = i & 3
        if intMode == 0:
            intShift = ((intCombined & 3) + 1)
            intResult = fnRotl8((intHashByte ^ (~intByte & 0xFF)) & 0xFF, intShift)
        elif intMode == 1:
            intShift = ((intCombined & 3) + 2)
            intResult = fnRotl8((intByte ^ (~intHashByte & 0xFF)) & 0xFF, intShift)
        elif intMode == 2:
            intShift = ((intCombined & 3) + 3)
            intResult = fnRotl8((intHashByte ^ (~intByte & 0xFF)) & 0xFF, intShift)
        else:
            intShift = ((intCombined & 3) + 4)
            intResult = fnRotl8((intByte ^ (~intHashByte & 0xFF)) & 0xFF, intShift)
        bytTransformed[i] = intResult
    bytFooter = bytearray(40)
    intFirstHashDword = modStruct.unpack_from('<I', bytes(bytTransformed), 0)[0]
    intFooterPrefix = intFirstHashDword ^ INT_MAGIC_B
    intXorEd = intFirstHashDword ^ INT_MAGIC_A
    modStruct.pack_into('<I', bytFooter, 0, intFooterPrefix)
    modStruct.pack_into('<I', bytFooter, 4, intXorEd)
    bytFooter[8:8+32] = bytTransformed
    bytSigned = bytearray(bytBytecode) + bytFooter
    return fnCompressBytecode(bytes(bytSigned))

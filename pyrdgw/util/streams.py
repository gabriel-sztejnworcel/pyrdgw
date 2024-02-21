import struct


class ReadableStream:
    
    def __init__(self, buf: bytes):
        self.buf = buf

    def read_uint8(self) -> int:
        assert len(self.buf) >= 1
        result = struct.unpack('<B', self.buf[0:1])[0]
        self.buf = self.buf[1:]
        return result

    def read_uint16(self) -> int:
        assert len(self.buf) >= 2
        result = struct.unpack('<H', self.buf[0:2])[0]
        self.buf = self.buf[2:]
        return result


    def peek_uint16(self) -> int:
        assert len(self.buf) >= 2
        result = struct.unpack('<H', self.buf[0:2])[0]
        return result

    def read_uint32(self) -> int:
        assert len(self.buf) >= 4
        result = struct.unpack('<I', self.buf[0:4])[0]
        self.buf = self.buf[4:]
        return result

    def read_uint64(self) -> int:
        assert len(self.buf) >= 8
        result = struct.unpack('<Q', self.buf[0:8])[0]
        self.buf = self.buf[8:]
        return result

    def read_utf16str(self, length: int) -> str:
        assert len(self.buf) >= length

        if self.buf[length - 1] == 0 and self.buf[length - 2] == 0:
            length = length - 2

        result = self.buf[0:length].decode('utf-16')
        self.buf = self.buf[length:]
        return result

    def read_bytes(self, length: int) -> bytes:
        result = self.buf[0:length]
        return result


class WritableStream:
    
    def __init__(self):
        self.buf = bytes()

    def write_uint8(self, i: int):
        self.buf = self.buf + struct.pack('<B', i)

    def write_uint16(self, i: int):
        self.buf = self.buf + struct.pack('<H', i)

    def write_uint32(self, i: int):
        self.buf = self.buf + struct.pack('<I', i)

    def write_uint64(self, i: int):
        self.buf = self.buf + struct.pack('<Q', i)

    def write_bytes(self, buf_to_write: bytes):
        self.buf = self.buf + buf_to_write
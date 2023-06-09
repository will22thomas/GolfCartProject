"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class camera_image_t(object):
    __slots__ = ["timestamp", "camera_name", "framecount", "width", "height", "size", "data"]

    __typenames__ = ["string", "string", "int64_t", "int32_t", "int32_t", "int32_t", "byte"]

    __dimensions__ = [None, None, None, None, None, None, ["size"]]

    def __init__(self):
        self.timestamp = ""
        self.camera_name = ""
        self.framecount = 0
        self.width = 0
        self.height = 0
        self.size = 0
        self.data = b""

    def encode(self):
        buf = BytesIO()
        buf.write(camera_image_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        __timestamp_encoded = self.timestamp.encode('utf-8')
        buf.write(struct.pack('>I', len(__timestamp_encoded)+1))
        buf.write(__timestamp_encoded)
        buf.write(b"\0")
        __camera_name_encoded = self.camera_name.encode('utf-8')
        buf.write(struct.pack('>I', len(__camera_name_encoded)+1))
        buf.write(__camera_name_encoded)
        buf.write(b"\0")
        buf.write(struct.pack(">qiii", self.framecount, self.width, self.height, self.size))
        buf.write(bytearray(self.data[:self.size]))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != camera_image_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return camera_image_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = camera_image_t()
        __timestamp_len = struct.unpack('>I', buf.read(4))[0]
        self.timestamp = buf.read(__timestamp_len)[:-1].decode('utf-8', 'replace')
        __camera_name_len = struct.unpack('>I', buf.read(4))[0]
        self.camera_name = buf.read(__camera_name_len)[:-1].decode('utf-8', 'replace')
        self.framecount, self.width, self.height, self.size = struct.unpack(">qiii", buf.read(20))
        self.data = buf.read(self.size)
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if camera_image_t in parents: return 0
        tmphash = (0x69657fa5762b1b6) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if camera_image_t._packed_fingerprint is None:
            camera_image_t._packed_fingerprint = struct.pack(">Q", camera_image_t._get_hash_recursive([]))
        return camera_image_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", camera_image_t._get_packed_fingerprint())[0]


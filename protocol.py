import struct

class ProtocolError(Exception):
    pass

def encode_fire(x: int, y:int) -> bytes:
    if not (0 <= x <= 255 and 0 <= y <= 255):
        raise ProtocolError(f"Coordinates out of range: {x}, {y}")
    return struct.pack(">BBBB", 1, 1, x, y)

def decode_fire(data: bytes) -> tuple[int, int]:
    if len(data) != 4:
        raise ProtocolError(f"expected 4 bytes, got {len(data)}")
    version, msg_type, x, y = struct.unpack(">BBBB", data)
    if version != 1:
        raise ProtocolError(f"bad version: {version}")
    if msg_type != 1:
        raise ProtocolError(f"bad type: {msg_type}")
    return (x, y)


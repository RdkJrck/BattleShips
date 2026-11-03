from protocol import decode_fire

class PacketBuffer:
    def __init__(self):
        self.pending = bytearray()

    def feed(self, chunk: bytes) -> list[tuple[int, int]]:
        self.pending.extend(chunk)
        shots = []
        while len(self.pending) >= 4:
            packet = bytes(self.pending[:4])
            del self.pending[:4]
            shots.append(decode_fire(packet))
        return shots


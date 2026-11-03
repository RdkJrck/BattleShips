import argparse
import socket

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description = "BattleShips TCP server")
    parser.add_argument("--host", default = "127.0.0.1")
    parser.add_argument("--port", type=int, default=9000)
    return parser.parse_args()



def main() -> None:
    args = parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"socket OK")
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((args.host, args.port))
    sock.listen(1)
    print(f"listening on {args.host}:{args.port}")
    conn, addr = sock.accept()
    print(f"Connected {addr}")
    
    buf = bytearray()
    while True:
        b = conn.recv(1)
        if b == b"": break
        buf.extend(b)
        while b"\n" in buf:
            i = buf.index(b"\n") + 1
            msg = bytes(buf[:i])
            del buf[:1]
            print("FRAME:", msg)

    conn.close()
    sock.close()

if __name__ == "__main__":
    main()

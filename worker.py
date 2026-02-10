import socket
import json

HOST = "0.0.0.0"
PORT = 5000

def heavy_task(start, end):
    result = 0
    for i in range(start, end):
        result += i * i
    return result

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("🟢 Worker gestart, wacht op taken...")

    while True:
        conn, addr = s.accept()
        with conn:
            task = json.loads(conn.recv(4096).decode())
            start = task["start"]
            end = task["end"]

            print(f"⚙️ Rekent {start} → {end}")

            result = heavy_task(start, end)

            conn.sendall(json.dumps({
                "result": result
            }).encode())

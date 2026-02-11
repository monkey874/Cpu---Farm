import socket
import json
import threading
import time

WORKERS = [
    "",
]

PORT = ""
TOTAL_WORK = 50_000_000
CHUNK = TOTAL_WORK // len(WORKERS)

results = []

def send_task(worker_ip, start, end):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((worker_ip, PORT))
        s.sendall(json.dumps({
            "start": start,
            "end": end
        }).encode())

        data = s.recv(4096)
        result = json.loads(data.decode())["result"]
        results.append(result)

threads = []
start_time = time.time()

for i, ip in enumerate(WORKERS):
    s = i * CHUNK
    e = TOTAL_WORK if i == len(WORKERS) - 1 else s + CHUNK

    t = threading.Thread(target=send_task, args=(ip, s, e))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

total = sum(results)
end_time = time.time()

print("✅ Totaal resultaat:", total)
print("⏱️ Totale tijd:", round(end_time - start_time, 2), "seconden")

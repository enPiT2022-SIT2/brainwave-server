import numpy as np
import socket
import sys
import threading
import redis

# socket生成
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# クライアントのIPを問わず33400番ポートで通信する
# ソケット登録
server.bind(("0.0.0.0", 33400))
# ソケット接続準備
server.listen()

# Redis に接続します
r = redis.Redis(host='localhost', port=6379, db=0)

def loop_handler(client):
    while True:
        try:
            # 1024バイトずつデータを受け取る
            data = client.recv(1024)
            if not data:
                break
            brainwave = np.frombuffer(data, dtype=np.float64)
            print(brainwave)
            if brainwave[3] == 1 :
                r.set(int(brainwave[0]), 'unhealthy')
            if brainwave[3] == 0 :
                r.set(int(brainwave[0]), 'healthy')
        except KeyboardInterrupt:
            break
    client.close()

while True:
    try:
				# ソケット接続待機
        client, _ = server.accept()
    except KeyboardInterrupt:
        sys.exit()
    # スレッド作成
    thread = threading.Thread(target=loop_handler, args=(client,), daemon=True)
    # スレッドスタート
    thread.start()

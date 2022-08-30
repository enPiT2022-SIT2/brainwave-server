import numpy as np
import socket
import sys
import threading

# socket生成
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# クライアントのIPを問わず33400番ポートで通信する
# ソケット登録
server.bind(("0.0.0.0", 33400))
# ソケット接続準備
server.listen(6)

def loop_handler(connection, address):
    while True:
				# 1024バイトずつデータを受け取る
        data = client.recv(1024)
				# すべて受信したらループを抜ける
        if not data:
            break
        brainwave = np.frombuffer(data, dtype=np.float64)
        if brainwave[3] == 1 :
            print(brainwave[0] ,"は寝ています")
    # 接続を切る
    client.close()

while True:
    try:
				# ソケット接続待機
        client, addr = server.accept()
    except InterruptedError:
        sys.exit()
    # スレッド作成
    thread = threading.Thread(target=loop_handler, args=(client, addr), daemon=True)
    # スレッドスタート
    thread.start()

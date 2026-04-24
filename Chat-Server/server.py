import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# ===== CONFIGURAZIONE =====
SERVER_HOST = '10.4.54.14'
SERVER_PORT = 5000

buffer_server = b""

def invia(sock, testo):
    sock.sendall((testo + "\n").encode('utf-8'))

def ricevi(sock):
    global buffer_server
    while b"\n" not in buffer_server:
        chunk = sock.recv(1024)
        if not chunk:
            return None
        buffer_server += chunk
    linea, buffer_server = buffer_server.split(b"\n", 1)
    return linea.decode('utf-8').strip()

# ===== GUI =====
root = tk.Tk()
root.title("TCP Chat Server")

chat = scrolledtext.ScrolledText(root, state=tk.DISABLED, width=50, height=20)
chat.pack(padx=10, pady=10)

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

def log(testo):
    chat.config(state=tk.NORMAL)
    chat.insert(tk.END, testo + "\n")
    chat.config(state=tk.DISABLED)
    chat.see(tk.END)

client_socket = None

def invia_messaggio():
    msg = entry.get().strip()
    if not msg or client_socket is None:
        return
    invia(client_socket, msg)
    log(f"Tu: {msg}")
    entry.delete(0, tk.END)
    if msg.upper() == "FINE":
        client_socket.close()

btn = tk.Button(root, text="Invia", command=invia_messaggio)
btn.pack(side=tk.LEFT, padx=10, pady=(0, 10))
entry.bind("<Return>", lambda e: invia_messaggio())

def ricevi_messaggi():
    while True:
        msg = ricevi(client_socket)
        if msg is None or msg.upper() == "FINE":
            log("[!] Client disconnesso.")
            break
        log(f"Client: {msg}")

def avvia_server():
    global client_socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", SERVER_PORT))
    server.listen(1)
    log(f"In attesa di connessione su porta {SERVER_PORT}...")
    client_socket, addr = server.accept()
    log(f"Client connesso: {addr[0]}:{addr[1]}")
    threading.Thread(target=ricevi_messaggi, daemon=True).start()

threading.Thread(target=avvia_server, daemon=True).start()
root.mainloop()


 

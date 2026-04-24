import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

HOST = '192.168.54.15'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# --- GUI setup ---
root = tk.Tk()
root.title('Client Chat')
root.configure(bg='white')
root.geometry('500x450')

chat_area = scrolledtext.ScrolledText(root, state='disabled', bg='white', fg='black',
                                      font=('Courier', 10), bd=1, relief='solid')
chat_area.pack(padx=10, pady=10, fill='both', expand=True)

frame_input = tk.Frame(root, bg='white')
frame_input.pack(padx=10, pady=(0, 10), fill='x')

entry_msg = tk.Entry(frame_input, font=('Courier', 10), bd=1, relief='solid')
entry_msg.pack(side='left', fill='x', expand=True, padx=(0, 5))

btn_invia = tk.Button(frame_input, text='Invia', bg='white', fg='black',
                      font=('Courier', 10), bd=1, relief='solid')
btn_invia.pack(side='right')


def mostra_messaggio(testo):
    def _mostra():
        chat_area.config(state='normal')
        chat_area.insert('end', testo + '\n')
        chat_area.see('end')
        chat_area.config(state='disabled')
    root.after(0, _mostra)


# --- Logica client (invariata) ---

def ricevi_messaggi():
    global client_socket
    buffer = ''

    try:
        while True:
            dati = client_socket.recv(1024)

            if not dati:
                break

            buffer += dati.decode()

            while '\n' in buffer:
                riga, buffer = buffer.split('\n', 1)
                riga = riga.strip()

                if riga:
                    mostra_messaggio(riga)

    except:
        pass

    mostra_messaggio('[SERVER] Connessione chiusa')


def invia_messaggio(event=None):
    messaggio = entry_msg.get().strip()
    if not messaggio:
        return

    entry_msg.delete(0, 'end')

    if messaggio.lower() == 'exit':
        client_socket.sendall('EXIT\n'.encode())
        root.quit()
        return

    client_socket.sendall(f'MSG:{messaggio}\n'.encode())
    mostra_messaggio(f'Tu: {messaggio}')


btn_invia.config(command=invia_messaggio)
entry_msg.bind('<Return>', invia_messaggio)


def connetti():
    nome = entry_nome.get().strip()
    if not nome:
        return

    frame_login.pack_forget()
    chat_area.pack(padx=10, pady=10, fill='both', expand=True)
    frame_input.pack(padx=10, pady=(0, 10), fill='x')

    try:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(f'NOME:{nome}\n'.encode())

        mostra_messaggio(f'Connesso al server {HOST}:{PORT}')
        mostra_messaggio("Scrivi un messaggio e premi Invio. Scrivi 'exit' per uscire.")

        thread_ricezione = threading.Thread(target=ricevi_messaggi, daemon=True)
        thread_ricezione.start()

    except Exception as errore:
        mostra_messaggio(f'Errore: {errore}')


# --- Schermata login ---
chat_area.pack_forget()
frame_input.pack_forget()

frame_login = tk.Frame(root, bg='white')
frame_login.pack(expand=True)

tk.Label(frame_login, text='Il tuo nome:', bg='white', font=('Courier', 11)).pack(pady=(0, 5))

entry_nome = tk.Entry(frame_login, font=('Courier', 11), bd=1, relief='solid', width=25)
entry_nome.pack(pady=(0, 10))
entry_nome.focus()

btn_connetti = tk.Button(frame_login, text='Connetti', bg='white', fg='black',
                         font=('Courier', 11), bd=1, relief='solid', command=connetti)
btn_connetti.pack()
entry_nome.bind('<Return>', lambda e: connetti())

root.mainloop()

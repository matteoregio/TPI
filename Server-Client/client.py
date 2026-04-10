import socket

# ===== CONFIGURAZIONE =====
ADDRESS_FAMILY = socket.AF_INET
SOCKET_TYPE = socket.SOCK_STREAM
SERVER_HOST = '10.4.54.15'
SERVER_PORT = 5000

print("\n=== CLIENT TCP QUIZ - Avvio ===")

# FASE 1: Crea socket
client = socket.socket(ADDRESS_FAMILY, SOCKET_TYPE)
print(f"[1] Socket creato")

# FASE 2: Connessione al server
client.connect((SERVER_HOST, SERVER_PORT))
print(f"[2] Connesso a {SERVER_HOST}:{SERVER_PORT}")
print("Benvenuto al Quiz! Rispondi alle domande che seguono.\n")

try:
    while True:
        # FASE 3: Ricevi domanda (o messaggio finale) dal server
        data = client.recv(1024)
        if not data:
            break  # Connessione chiusa dal server

        messaggio = data.decode('utf-8')

        # Controlla se è il messaggio di fine quiz
        if messaggio.startswith("FINE"):
            print(f"\n{messaggio}\n")
            break

        # Mostra la domanda all'utente
        print(f"\n{messaggio}")

        # FASE 4: Acquisisci risposta da tastiera
        risposta = input("   La tua risposta: ").strip()

        # FASE 5: Invia la risposta al server
        client.sendall(risposta.encode('utf-8'))

        # FASE 6: Ricevi il feedback dal server
        feedback = client.recv(1024).decode('utf-8')
        print(f"   {feedback}")

finally:
    # FASE 7: Chiudi connessione
    client.close()
    print("[7] Connessione chiusa. Ciao!\n")
 

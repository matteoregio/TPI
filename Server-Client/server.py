import socket

# ===== CONFIGURAZIONE =====
ADDRESS_FAMILY = socket.AF_INET
SOCKET_TYPE = socket.SOCK_STREAM
SERVER_HOST = 'localhost'
SERVER_PORT = 5000

# ===== DATABASE DOMANDE =====
domande = [
    {"domanda": "Quanti mondiali ha vinto Schumacher?", "risposta": "7"},
    {"domanda": "In quale anno è stata fondata la Formula 1?", "risposta": "1950"},
    {"domanda": "Quale squadra ha vinto più titoli costruttori?", "risposta": "ferrari"},
    {"domanda": "Qual'è il pilota con più vittorie in carriera", "risposta": "lewis hamilton"},
    {"domanda": "Quale pilota ha battuto Hamilton nel 2021?", "risposta": "max verstappen"},
    {"domanda": "Come si chiama il sistema di recupero di energia nelle monoposto?", "risposta": "ERS"},
    {"domanda": "Quale circuito è il più veloce nel calendario?", "risposta": "circuito di monza"},
    {"domanda": "Qual'è il colore della gomma più morbida?", "risposta": "rossa"},
]

print("\n=== SERVER TCP QUIZ - Avvio ===")

# FASE 1: Crea socket
server = socket.socket(ADDRESS_FAMILY, SOCKET_TYPE)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print(f"[1] Socket creato")

# FASE 2: Bind
server.bind(("0.0.0.0", SERVER_PORT))
print(f"[2] Bind su {SERVER_HOST}:{SERVER_PORT}")

# FASE 3: Listen
server.listen(1)
print(f"[3] Server in ascolto su porta {SERVER_PORT}...")

try:
    while True:
        # FASE 4: Accept
        client_socket, client_address = server.accept()
        print(f"\n[4] Connessione accettata da {client_address}")

        punteggio = 0
        totale = len(domande)

        # FASE 5: Ciclo domande
        for i, item in enumerate(domande):
            # Invia la domanda con il numero progressivo
            testo_domanda = f"[{i+1}/{totale}] {item['domanda']}"
            client_socket.sendall(testo_domanda.encode('utf-8'))
            print(f"[>] Domanda inviata: {testo_domanda}")

            # Ricevi la risposta del client
            data = client_socket.recv(1024)
            risposta_client = data.decode('utf-8').strip().lower()
            print(f"[<] Risposta ricevuta: '{risposta_client}'")

            # Valuta la risposta
            if risposta_client == item['risposta']:
                punteggio += 1
                feedback = "Corretto!"
            else:
                feedback = f"Sbagliato! La risposta corretta era: {item['risposta'].capitalize()}"

            # Invia il feedback
            client_socket.sendall(feedback.encode('utf-8'))
            print(f"[>] Feedback inviato: {feedback}")

        # FASE 6: Invia risultato finale
        risultato = f"FINE!! Quiz terminato! Hai totalizzato {punteggio}/{totale} risposte corrette."
        client_socket.sendall(risultato.encode('utf-8'))
        print(f"\n[FINE] Risultato inviato: {risultato}")

        # FASE 7: Chiudi connessione client
        client_socket.close()
        print(f"[7] Connessione con {client_address} chiusa\n")
        print("--- In attesa di un nuovo client ---\n")

except KeyboardInterrupt:
    print("\n\n[!] Server interrotto (Ctrl+C)")
finally:
    server.close()
    print("[8] Socket server chiusa\n")

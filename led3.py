import serial
import time

ser = serial.Serial("COM7", 9600)

file_dati = open("eventi_led.csv", "w")
file_dati.write("timestamp,valore\n")

while True:
    data = ser.readline().decode("utf-8").strip()
    valore = data

    timestamp = time.strftime("%H:%M:%S")

    
    file_dati.write(f"{timestamp}\n")
    file_dati.flush()

    print(f"Bottone premuto!!")

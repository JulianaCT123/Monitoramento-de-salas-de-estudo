import serial
import time
from estado_global import status_salas 

def iniciar_leitura_arduino():
    try:
        arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)
    except Exception as e:
        print(f"Erro serial: {e}")
        return

    while True:
        if arduino.in_waiting > 0:
            linha = arduino.readline().decode('utf-8').rstrip()
            dados = linha.split(',')
            
            # Agora esperamos 3 informações: ID, Presença e Luz
            if len(dados) == 3:
                id_sala = dados[0]
                presenca = int(dados[1])
                luz = int(dados[2])
                
                # Atualiza apenas a sala correspondente, se ela existir no sistema
                if id_sala in status_salas:
                    status_salas[id_sala]["ocupada"] = (presenca == 1)
                    status_salas[id_sala]["luminosidade"] = luz
                    status_salas[id_sala]["ultima_atualizacao"] = time.strftime("%H:%M:%S")
        
        time.sleep(0.1)
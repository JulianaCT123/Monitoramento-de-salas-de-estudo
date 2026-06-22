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
        try:
            if arduino.in_waiting > 0:
                linha = arduino.readline().decode('utf-8').strip()
                
                print(f"[DEBUG] Recebido do Arduino: {linha}")
                
                dados = linha.split(',')

                if len(dados) == 3:
                    id_sala = dados[0]
                    presenca = int(dados[1])
                    luz = int(dados[2])

                    if id_sala in status_salas:
                        status_salas[id_sala]["ocupada"] = (presenca == 1)
                        status_salas[id_sala]["luz"] = (luz == 1)
                        status_salas[id_sala]["ultima_atualizacao"] = time.strftime("%H:%M:%S")

                        # controle de tempo vazia
                        if presenca == 1:
                            status_salas[id_sala]["tempo_vazia"] = None
                        else:
                            # presenca == 0. Só conta o tempo se a luz estiver acesa!
                            if luz == 1:
                                if status_salas[id_sala]["tempo_vazia"] is None:
                                    status_salas[id_sala]["tempo_vazia"] = time.time()
                                    
                                # Se for -1, significa que o comando já foi enviado, então não faz nada
                                elif status_salas[id_sala]["tempo_vazia"] != -1:
                                    tempo_passado = time.time() - status_salas[id_sala]["tempo_vazia"]

                                    if tempo_passado >= 2.0:
                                        comando = f"D{id_sala}\n"
                                        arduino.write(comando.encode('utf-8'))
                                        
                                        # Substitui o Infinito por -1 para não dar erro de JSON no site
                                        status_salas[id_sala]["tempo_vazia"] = -1
                            else:
                                # Sala vazia e luz já apagada. Zera o cronômetro.
                                status_salas[id_sala]["tempo_vazia"] = None

        except Exception as e:
            print("Erro leitura serial:", e)
            # Dá um respiro para a CPU caso o cabo desconecte rapidamente
            time.sleep(1)

        time.sleep(0.1)
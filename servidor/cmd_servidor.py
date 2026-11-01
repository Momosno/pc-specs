import socket
import os
import platform


class Cmd:
    def __init__(self):
        super().__init__()

    def _Cmd_(self, host, port, clientsocket):
        self.fin_envio = "FIN"
        self.fin_conexion = "salir"
        self.clientsocket = clientsocket

        while True:
            try:
                ### RECIBO COMANDO ###
                self.comando_recibido = self.clientsocket.recv(1024).decode(
                    "utf-8"
                )  # chequeo opcion
                print("Comando a Ejecutar: " + str(self.comando_recibido))

                if self.comando_recibido == self.fin_conexion:
                    print("Conexion Finalizada")
                    self.clientsocket.send(self.fin_conexion.encode("utf-8"))
                    # self.clientsocket.close()
                    print("#" * 5 + "\nEsperando nueva conexion...")
                    break  # espera nueva opcion

                else:
                    self.respuesta_cmd = os.popen(
                        self.comando_recibido
                    )  # comando para cmd

                    print("*" * 20 + "\n")
                    for linea in self.respuesta_cmd.readlines():
                        self.clientsocket.send(linea.encode("utf-8"))
                        print(linea)
                    print("*" * 20)

                    self.clientsocket.send(self.fin_envio.encode("utf-8"))
                    print("\nEsperando comandos...")
                    continue

            except:
                print("Cierre cliente\n" + "#" * 5 + "\n")
                self.clientsocket.close()
                return

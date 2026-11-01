import socket
import time


class Cmd:
    def __init__(self):
        super().__init__()

    def _Cmd_(self, host):

        host = host  # IP PC local de la cual necesito datos
        port = 55555
        self.opcion = "cmd"
        self.fin_conexion = "salir"
        self.fin_comando = "FIN"

        self.clientsocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # CLIENTE TCP
        self.clientsocket.connect((host, port))
        self.clientsocket.send(self.opcion.encode("utf-8"))

        while True:  # QUEDA CONECTADO
            try:
                self.comando_envio = input(
                    "-" * 10 + '\nIngrese comando para CMD ("salir" para finalizar)\n'
                )
                self.clientsocket.send(self.comando_envio.encode("utf-8"))
                while True:
                    try:
                        self.respuesta_cmd = self.clientsocket.recv(1024).decode(
                            "utf-8"
                        )
                        print(self.respuesta_cmd)

                        if self.respuesta_cmd == self.fin_conexion:
                            print("Conexion Finalizada\n" + "#" * 10 + "\n")
                            self.clientsocket.close()
                            return  # vuelvo

                        elif self.respuesta_cmd == self.fin_comando:
                            print("**Comando ejecutado**")
                            break

                        else:
                            continue

                    except:
                        print("Conexion finalizada por el Servidor\n" + "#" * 10 + "\n")
                        self.clientsocket.close()
                        return
            except:
                print("Error servidor")
                self.clientsocket.close()
                return

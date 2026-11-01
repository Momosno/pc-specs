import socket
from tkinter import messagebox
import bandwidth, cmd_servidor
import sys


"""
socket_servidor.py:
Modulo encargado de general las conexiones para el acceso remoto.
"""


class Socket:
    def __init__(self):
        super().__init__()
        global host, port, mensajes_rcv

        host = socket.gethostname()  # IP PC local de la cual necesito datos
        port = 55555

    def Inicio_conexion(self, lista_datos_pc):
        global host, port
        self.serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # CLIENTE TCP
        """
        # AF_INET => dominio conector, IPV4
        # SOCK_STREAM => Tipo de conector (TCP en este caso)
        """
        self.fin_envio = "OK"
        self.inicio_envio = "Lista"
        try:
            self.serversocket.bind((host, port))
            self.serversocket.listen(3)
            print("Escuchando")
        except OSError as err:
            messagebox.showerror(
                message="Ya existe un programa ejecutandose. Por favor finalice el otro porceso y vuelva a ejecutar.",
                title="Error de Ejecucion",
            )
            sys.exit()

        while True:
            """#inicia conexion"""
            (self.clientsocket, self.address) = self.serversocket.accept()
            print("inicio conexion")

            """#Datos Cliente """
            print("Recibo conexion desde :" + str(self.address[0]))
            print(self.address[1])  # Numero de conexion
            # print(type(self.address)) ---> tupla de 2 valores

            self.msg = self.clientsocket.recv(1024).decode("utf-8")  # chequeo opcion
            print("Se pide: " + self.msg)

            if self.msg == "Lista":

                ############ Envio Lista Datos_PC ############# ENVIO LISTA COMO STR
                lista_datos_pc[1] = lista_datos_pc[1].replace(",", ";")
                # print(lista_datos_pc)  #'NOMBRE-PC', 'APELLIDO; Nombre'
                self.dato = str(lista_datos_pc)
                self.string = str(self.dato)
                self.codif = (self.string).encode("utf-8")
                self.clientsocket.send(self.codif)
                self.clientsocket.send(self.fin_envio.encode("utf-8"))

                print("Fin envio datos PC\n" + "-" * 10)
                self.clientsocket.close()

            elif self.msg == "bandwidth":
                while True:
                    self.datos = bandwidth.Ancho_timepo_real()
                    while True:
                        self.a = next(self.datos)
                        print(self.a)
                        self.clientsocket.send(self.a.encode("utf-8"))
                        self.response = self.clientsocket.recv(1024).decode("utf-8")
                        if self.response == "cancelar":
                            print("Fin envio ancho de Banda\n" + "-" * 10)
                            self.clientsocket.close()
                            break
                        elif self.response == "ok":
                            continue
                    break
            elif self.msg == "cmd":
                a = cmd_servidor.Cmd()._Cmd_(host, port, self.clientsocket)
                self.clientsocket.close()
                continue

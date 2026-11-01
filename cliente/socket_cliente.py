import socket
import ip_scan


"""
socket_cliente.py:
Modulo encargado de general las conexiones para el acceso remoto.
"""


class Socket:
    def __init__(self):
        super().__init__()

    def Conexion(self, opcion, ip):
        """
        Funcion encargada de crear el socket con el Servidor.
        """
        if opcion == "ancho_combinado":
            self.lista_on = ip_scan.Ingreso_datos()
            print(
                "Lista de IP de las PC encendidas y con conexion:\n"
                + str(self.lista_on)
            )
            return
        else:
            self.clientsocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )  # CLIENTE TCP
            # print(socket.gethostbyname(socket.gethostname()))

            self.host = ip  # Ip servidor / Ip de la pc a buscar (INPUT())
            self.port = 55555
            try:
                self.clientsocket.connect((self.host, self.port))
            except:
                return False

            while True:
                self.clientsocket.send(opcion.encode("utf-8"))
                #########################
                if opcion == "bandwidth":
                    while True:
                        try:
                            self.mensaje = self.clientsocket.recv(1024)
                            self.msg = self.mensaje.decode("utf-8")
                            print(self.msg)
                            self.clientsocket.send("ok".encode("utf-8"))

                        except:
                            self.clientsocket.send(("cancelar").encode("utf-8"))
                            self.clientsocket.close()
                            break
                    return
                ##########################
                elif opcion == "Lista":
                    ##### RECIBE ######
                    self.mensaje = self.clientsocket.recv(1024)
                    self.msg = self.mensaje.decode("utf-8")
                    # print(self.msg)

                    if self.msg == ("OK"):
                        print("Datos Recibidos")
                        self.clientsocket.close()
                        break
                    else:
                        ### Manejo String ###
                        self.clientsocket.close()
                        self.temp = self.msg[1:-1].replace("'", "")
                        self.lista_datos = list(self.temp.split(","))
                        self.lista_datos[1] = self.lista_datos[1].replace(";", ",")
                        return self.lista_datos

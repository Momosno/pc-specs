import socket_cliente, red, cmd_cliente


"""
view.py:
Es el modulo donde se crea la ventana e ingresan los datos.    
"""
global host
host = 0


class App:
    """
    La clase generadora de la consola.
    """

    def __init__(self):
        super().__init__()
        self.Menu_global()

    def Menu_global(self):
        global host
        """
        Funcion encargada del Menu
        """
        self.opcion1 = input("#" * 10 + "\n" + "1) Chequear PCs de la red\n2) Buscar IP\n")
        if self.opcion1 == "1":
            socket_cliente.Socket().Conexion("ancho_combinado", host)
        #################################
        elif self.opcion1 == "2":
            if host == 0:
                host = str(input("Ingrese IP a buscar: "))
                self.Menu_buscar_ip()

    def Menu_buscar_ip(self):
        global host
        self.opcion = input(
            "#" * 10
            + "\n"
            + "1) Datos PC\n2) Ancho de Banda PC Remota\n3) Ancho de banda PC Local\n"
            + "4) CMD Remoto\n5) Menu anterior\n6) Cambiar IP a buscar\n"
        )
        ######
        if self.opcion == "1":
            self.lista_datos = socket_cliente.Socket().Conexion("Lista", host)
            if self.lista_datos == False:
                print("*" * 20 + "\n" + "Ip no encontrada\n" + "*" * 20 + "\n")
                print("Ingrese IP a buscar: ")
                host = str(input())
                self.Menu_buscar_ip()
            else:
                print(
                    f"Nombre PC: {self.lista_datos[0]}\n"
                    f"Usuario: {self.lista_datos[1]}\n"
                    f"Dependencia: {self.lista_datos[2]}\n"
                    f"IP: {self.lista_datos[3]}\n"
                    f"SO: {self.lista_datos[4]}\n"
                    f"Procesador: {self.lista_datos[5]}\n"
                    f"HDD: {self.lista_datos[6]}\n"
                    f"Ram: {self.lista_datos[7]}\n"
                    f"Ups: {self.lista_datos[8]}\n"
                )
                self.Menu_buscar_ip()
        elif self.opcion == "2":
            print("Presionar 'Ctrl + C', para detener la verificacion de red.")
            socket_cliente.Socket().Conexion("bandwidth", host)
            self.Menu_buscar_ip()
        elif self.opcion == "3":
            print("Presionar 'Ctrl + C', para detener la verificacion de red.")
            red.Bandwidth().Ancho_timepo_real()
            self.Menu_buscar_ip()
        elif self.opcion == "4":
            cmd_cliente.Cmd()._Cmd_(host)
            self.Menu_buscar_ip()
        elif self.opcion == "5":
            host = 0
            self.Menu_global()
        elif self.opcion == "6":
            host = str(input("Ingrese IP a buscar: "))
            self.Menu_buscar_ip()
        else:
            print("\nOpcion no valida, vuelva a intentar\n")
            self.Menu_buscar_ip()

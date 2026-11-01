from datetime import datetime
import platform as pl
import os
import socket  # IP, cliente-servidor
import psutil
import cpuinfo
import conexion_db, socket_servidor

"""
model.py:
Modulo encargado de la logica del programa, procesa
los datos y los guarda en el block y en la base.
"""
cont = 0


class Model:
    """
    Clase generadora de la logica del programa
    """

    def __init__(self):
        super().__init__()
        global dicc_hdd, memory_types, mysql, diccionarios
        dicc_hdd = {
            "0.0": 99,  # S/D
            "70.0 GB": 8,
            "80.0 GB": 3,
            "120.0 GB": 101,
            "150.0 GB": 11,
            "160.0 GB": 6,
            "250.0 GB": 5,
            "300.0 GB": 10,
            "320.0 GB": 4,
            "500.0 GB": 2,
            "600.0 GB": 7,
            "750.0 GB": 102,
            "1.0 TB": 1,
            "2.0 TB": 9,
        }

        memory_types = {
            0: "Unknown",
            1: "Other",
            2: "DRAM",
            3: "Synchronous DRAM",
            4: "Cache DRAM",
            5: "EDO",
            6: "EDRAM",
            7: "VRAM",
            8: "SRAM",
            9: "RAM",
            10: "ROM",
            11: "Flash",
            12: "EEPROM",
            13: "FEPROM",
            14: "EPROM",
            15: "CDRAM",
            16: "3DRAM",
            17: "SDRAM",
            18: "SGRAM",
            19: "RDRAM",
            20: "DDR",
            21: "DDR2",
            22: "DDR2 FB-DIMM",
            24: "DDR3",
            25: "FBD2",
            26: "DDR4",
        }

        diccionarios = conexion_db.Actualizar_db_local()

    def Actualizar_db_local(self):
        global diccionarios
        return diccionarios

    def Conversion_ip(self):
        """
        Convierte la ip a un formato que necesitaba para la base de datos
        """
        self.s = str(socket.gethostbyname(socket.gethostname())).split(sep=".")

        self.suma = (
            (int(self.s[0]) * (256 ** 3))
            + (int(self.s[1]) * (256 ** 2))
            + (int(self.s[2]) * 256)
            + int(self.s[3])
        )
        return self.suma

    def Valor_real(self, bytes, tipo_memoria):

        """
        Funcion encargada de darle un valor real a los bytes
        de la memoria RAM, y del HDD
        """
        if tipo_memoria == "disco":
            if bytes < 2.0:
                return 2.0
            elif bytes < 70.0:
                return 70.0
            elif bytes < 80.0:
                return 80.0
            elif bytes < 120.0:
                return 120.0
            elif bytes < 150.0:
                return 150.0
            elif bytes < 160.0:
                return 160.0
            elif bytes < 250.0:
                return 250.0
            elif bytes < 300.0:
                return 300.0
            elif bytes < 320.0:
                return 320.0
            elif bytes < 500.0:
                return 500.0
            elif bytes < 600.0:
                return 600.0
            elif bytes < 750.0:
                return 750.0
            elif bytes < 1010.0:
                return 1.0

        elif tipo_memoria == "ram":
            if bytes < 3.0:
                return 2
            elif bytes < 5.0:
                return 4
            elif bytes < 7.0:
                return 6
            elif bytes < 9.0:
                return 8
            elif bytes < 13.0:
                return 12
            elif bytes < 17.0:
                return 16

    def get_size(self, bytes, tipo_memoria, suffix="B"):
        """
        Funcion encargada de convertir unidades de memoria
        """
        self.factor = 1024
        # print(type(bytes)) INT
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < self.factor:
                a = str(self.Valor_real(bytes, tipo_memoria))
                if a == "1.0":
                    unit = "T"
                    b = str(f"{a} {unit}{suffix}")
                    return b
                else:
                    b = str(f"{a} {unit}{suffix}")
                    return b
            else:
                bytes /= self.factor

    def Block_notas(self, datos_pc):
        """
        Funcion encargada de crear un block de notas de ser
        la primera vez que se ejecuta el programa.
        """
        try:
            archivo = open("Lista PC Specs.txt", "r")
            contenido = archivo.readline()

        except:
            archivo = open("Lista PC Specs.txt", "a")
            archivo.write(f"Nombre PC;Usuario;Dependencia;IP;SO;Procesador;HDD;RAM;UPS")
            archivo.write("\n")
        finally:
            archivo = open("Lista PC Specs.txt", "a")
            for key in datos_pc:
                archivo.write(f"{datos_reales_pc[key]};")
            archivo.write("\n")
            archivo.close()

    def Ram(self):
        global memory_types
        self.lista_var = ["memorytype", "capacity"]
        self.lista_memorytype = []
        self.lista_capacity = []
        self.suma_capacity = 0

        for i in self.lista_var:
            self.respuesta_cmd = os.popen(f"wmic memorychip get {i}")
            for linea in self.respuesta_cmd.readlines():
                if linea == "\n":
                    continue
                else:
                    self.temp = linea[:-2].strip()
                    if i == "memorytype":
                        self.lista_memorytype.append(self.temp)
                    elif i == "capacity":
                        self.lista_capacity.append(self.temp)

        self.lista_capacity.remove("Capacity")
        for i in self.lista_capacity:
            self.suma_capacity += int(i)

        self.memory_type = memory_types.get(int(self.lista_memorytype[1]))
        return [self.suma_capacity, self.memory_type]

    ########### Info basica ############
    def general_info(
        self, usuario, dependencia, checkbox_value, usuario_real, dependencia_real
    ):
        """
        Funcion encargada de tomar los datos de la PC y los almacena
        """
        global datos_pc, lista_datos_pc, datos_reales_pc
        lista_datos_pc = []
        self.suma_hdd = 0
        self.tamaño_part = 0
        self.uname = pl.uname()

        ########################################## Usuario / Dependencia
        self.usuario = usuario
        self.dependencia = dependencia

        ########################################## SO
        self.os = (pl.platform())[0:10]
        self.name = self.os.replace("-", " ")
        if self.name.find("10") > -1:
            self.so = "1"
        elif self.name.find("8") > -1:
            self.so = "5"
        else:
            self.so = self.os

        ########################################### UPS
        if checkbox_value == True:
            self.ups = 1
            self.ups_real = "Si"
        elif checkbox_value == False:
            self.ups = 0
            self.ups_real = "No"

        ########################################### Memoria RAM
        self.memoria = self.Ram()
        self.capacity = self.get_size(self.memoria[0], "ram")
        # print(self.capacity)

        ########################################### Tamaño HDD
        self.particiones = psutil.disk_partitions(all=False)
        # print(self.partitions) Todos los datos de las particiones existentes
        for particion in self.particiones:
            if particion.fstype == "NTFS":
                self.tamaño_part = psutil.disk_usage(particion.device).total
                self.suma_hdd += self.tamaño_part

            else:
                pass

        datos_pc = {
            "nombre_pc": self.uname.node,  # listo
            "usuario": self.usuario,
            "dependencia": self.dependencia,
            "ip": self.Conversion_ip(),
            "so": self.so,
            "procesador": str(cpuinfo.get_cpu_info()["brand_raw"]).replace(
                ",", ""
            ),  # listo
            "hdd": dicc_hdd.get(str(self.get_size(self.suma_hdd, "disco"))),
            "ram": f"{self.capacity} {self.memoria[1]}",
            "ups": self.ups,
        }

        datos_reales_pc = {
            "nombre_pc": self.uname.node,  # listo
            "usuario": usuario_real,  # listo
            "dependencia": dependencia_real,  # listo
            "ip": socket.gethostbyname(socket.gethostname()),
            "so": self.os,
            "procesador": str(cpuinfo.get_cpu_info()["brand_raw"]).replace(
                ",", ""
            ),  # listo
            "hdd": str(self.get_size(self.suma_hdd, "disco")),
            "ram": f"{self.capacity} {self.memoria[1]}",
            "ups": self.ups_real,
        }

        ################################## PARA ENVIO POR TCP
        for dato in datos_reales_pc:
            lista_datos_pc.append(str(datos_reales_pc.get(dato)))

        conexion_db.Add_procesador_ram(datos_pc)  # HACE ESTO LA PRIMERA VEZ NADA MAS

        self.block = self.Block_notas(
            datos_reales_pc
        )  # HACE ESTO LA PRIMERA VEZ NADA MAS
        return

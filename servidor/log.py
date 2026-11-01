from datetime import datetime


class Log:
    def __init__(self):
        super().__init__()
        global hora
        hora = str(datetime.now().strftime("%H:%M:%S %d-%m-%Y"))
        return

    def Block(self):
        global hora
        try:
            self.archivo = open("log_PC_Specs.txt", "r")
            self.contenido = self.archivo.readline()

        except:
            self.archivo = open("log_PC_Specs.txt", "a")
            self.archivo.write(f"Servicio Iniciado por Primera Vez -- {hora} ")
            self.archivo.write("\n")

        else:
            self.archivo = open("log_PC_Specs.txt", "a")
            self.archivo.write(f"Servicio Iniciado -- {hora} ")
            self.archivo.write("\n")

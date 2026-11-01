import psutil
import time

"""
red.py:
Se encarga de mostrar el ancho de banda utilizado en la 
PC del cliente.
"""


class Bandwidth:
    def __init__(self):
        super().__init__()

    def Ancho_timepo_real(self):
        self.ultimo_recibido = psutil.net_io_counters().bytes_recv
        self.ultimo_enviado = psutil.net_io_counters().bytes_sent
        self.ultimo_total = self.ultimo_recibido + self.ultimo_enviado

        while True:
            try:
                self.bytes_recibido = psutil.net_io_counters().bytes_recv
                self.bytes_enviado = psutil.net_io_counters().bytes_sent
                self.bytes_total = self.bytes_recibido + self.bytes_enviado

                self.new_recibido = self.bytes_recibido - self.ultimo_recibido
                self.new_enviado = self.bytes_enviado - self.ultimo_enviado
                self.new_total = self.bytes_total - self.ultimo_total

                self.mb_new_recibido = self.new_recibido / 1024
                self.mb_new_enviado = self.new_enviado / 1024
                self.mb_new_total = self.new_total / 1024

                print(
                    f"{self.mb_new_recibido:.1f} KB recibidos, {self.mb_new_enviado:.1f} KB enviados, {self.mb_new_total:.1f} KB totales"
                )

                self.ultimo_recibido = self.bytes_recibido
                self.ultimo_enviado = self.bytes_enviado
                self.ultimo_total = self.bytes_total

                time.sleep(1)

            except:
                break

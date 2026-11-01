import psutil
import time


def Ancho_timepo_real():

    """Ref values"""
    ultimo_recibido = psutil.net_io_counters().bytes_recv
    ultimo_enviado = psutil.net_io_counters().bytes_sent
    ultimo_total = ultimo_recibido + ultimo_enviado

    while True:
        """Actual Values"""
        bytes_recibido = psutil.net_io_counters().bytes_recv
        bytes_enviado = psutil.net_io_counters().bytes_sent
        bytes_total = bytes_recibido + bytes_enviado

        """ Difference Actual - Reference """
        new_recibido = bytes_recibido - ultimo_recibido
        new_enviado = bytes_enviado - ultimo_enviado
        new_total = bytes_total - ultimo_total

        """ Unit """
        mb_new_recibido = new_recibido / 1024
        mb_new_enviado = new_enviado / 1024
        mb_new_total = new_total / 1024
        string = (
            f"{mb_new_recibido:.2f} KB recibidos, {mb_new_enviado:.2f} "
            f"KB enviados, {mb_new_total:.2f} KB totales"
        )

        """New ref"""
        ultimo_recibido = bytes_recibido
        ultimo_enviado = bytes_enviado
        ultimo_total = bytes_total

        time.sleep(1)

        yield string  # changed to yield instead of return

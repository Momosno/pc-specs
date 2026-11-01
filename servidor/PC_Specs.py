# import model
import view
from multiprocessing import freeze_support
import tkinter as tk

"""
-Proyecto - "PC SPECS"- Servidor

    Se trata de sript que basicamente toma los datos de los componentes 
fisicos de una pc (usuario,ip,hdd,ram,etc); y los guarda tanto en un
block de notas con formato compatible con csv (para un mejor manejo 
posterior), y tambien en un servidor de mysql. 

    Este script tambien cuenta con una conexion remota para un cliente,
el cual puede acceder a los 
datos de la pc "Servidor".

    Finalmente cuenta tambien con la 
funcionalidad de testear el ancho de banda de la pc del cliente, como
de la del servidor.

    Los datos se toman solo una vez y se almacenan en el block de notas,
la idea es al encenderse la pc, que se cree un servicio en windows 
capaz de recibir conexiones del cliente y poder enviarle los datos.

    El fomrato que se les da a los datos para almacenarlos, es con la 
finalidad de facilitar el guardado de estos en una base de datos existente.

Este el el programa que funciona como servidor, el cual se ejecutaria al
iniciar la PC, y al cual se accederia de forma remota.
"""

"""
Este es el modulo desde el cual se ejecuta el programa.
"""

if __name__ == "__main__":
    freeze_support()
    master = tk.Tk()
    app = view.App(master=master)
    app.master.mainloop()

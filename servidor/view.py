from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
import sys, time

import model, socket_servidor, log

"""
view.py:
Es el modulo donde se crea la ventana e ingresan los datos.    
"""


class App:
    def __init__(self, master=None):
        """
        La clase generadora de la ventana.
        """
        super().__init__()
        global masterchief
        masterchief = master
        self.master = master
        self.model = model.Model()
        self.log = log.Log().Block()
        self.Pc_nueva(master)  # Chequea si ya se obtuvieron los datos de la pc
        self.Window(master)

    def Arerglo_lista_pc(self, lista):
        self.lista_datos_pc = lista
        self.lista_datos_pc = list(self.lista_datos_pc.split(";"))
        self.lista_datos_pc.pop(-1)
        return self.lista_datos_pc

    def Pc_nueva(self, master):
        """
        Se chequea si es una pc nueva donde se corre el programa,
        o si ya se corrio previamente.
        """
        try:
            f = open("Lista PC Specs.txt", "r")
        except:
            print("Es una Pc nueva")
            return  # es una pc nueva
        else:  #    # no es una pc nueva
            self.datos_pc = (f.readlines())[1]  # Datos reales pc
            f.close()

            print("No es una Pc nueva")
            self.lista_datos_pc = self.Arerglo_lista_pc(self.datos_pc)
            self.socket_servidor = socket_servidor.Socket()
            self.socket_serv = self.socket_servidor.Inicio_conexion(self.lista_datos_pc)

    def Window(self, master):
        """
        Ventana principal
        """
        global main_window
        main_window = master
        self.master.title("System Specs")
        self.master.config(bd=10, bg="black")
        self.master.geometry("700x200")
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.Frame(master)

    def Frame(self, root):
        """
        Frame principal.
        """
        self.frame = tk.Frame(root, pady=1)
        self.frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=2)
        self.frame.config(bg="darkgreen", bd=10)
        self.Label(self.frame)
        self.Combobox(self.frame)
        self.Check_ups(self.frame)
        self.Buttons(self.frame)
        self.Bind(root)
        combo_personal.focus()

    def Label(self, root):
        """
        Nombres de los campos para ingreso de datos
        """
        global font_1
        font_1 = ("Calibri", 12, "bold")
        self.l_1 = tk.Label(
            root,
            text="Usuario",
            bg="Black",
            fg="white",
            font=font_1,
        )
        self.l_1.grid(row=0, column=0, sticky=tk.EW)
        self.l_2 = tk.Label(
            root,
            text="Dependencia",
            bg="Black",
            fg="white",
            font=font_1,
        )
        self.l_2.grid(row=2, column=0, sticky=tk.EW)
        self.l_2 = tk.Label(root, bg="darkgreen")
        self.l_2.grid(row=1, column=0, sticky=tk.EW)
        self.l_3 = tk.Label(root, bg="darkgreen")
        self.l_3.grid(row=3, column=0, sticky=tk.EW)

    def Buttons(self, root):
        """
        Declaracion de botones
        """
        self.button = tk.Button(
            root,
            text="Aceptar",
            padx=8,
            activebackground="red",
            activeforeground="white",
            background="black",
            foreground="red",
            font=font_1,
            state=tk.NORMAL,
            command=lambda: self.Check_campos(root),
        )
        self.button.grid(row=5, column=1, sticky=tk.NSEW, pady=10, padx=200)

    def Combobox(self, root):
        """
        Se crea un combobox, ya que para las necesidades que
        requeria, era mucho mas simple manejarse de este modo,
        mostrando datos que tenia en una base de datos, los
        cuales estaban almacenados en diccionarios.
        """
        global combo_dependencias, dicc_dependencias, lista_dep, diccionarios
        global combo_personal, dicc_personal, lista_personal
        diccionarios = model.diccionarios
        dicc_dependencias = diccionarios[0]
        dicc_personal = diccionarios[1]

        lista_personal = list(dicc_personal.keys())
        combo_personal = tk.ttk.Combobox(root, state=tk.NORMAL, values=lista_personal)
        combo_personal.grid(row=0, column=1, sticky=tk.NSEW, padx=10)

        lista_dep = list(dicc_dependencias.keys())
        combo_dependencias = tk.ttk.Combobox(root, state=tk.NORMAL, values=lista_dep)
        combo_dependencias.grid(row=2, column=1, sticky=tk.NSEW, padx=10)

    def Check_ups(self, root):
        """
        Un campo de check
        """
        global checkbox_value
        checkbox_value = tk.BooleanVar()
        checkbox_value.set(False)
        self.checkbox = tk.ttk.Checkbutton(root, text="UPS", variable=checkbox_value)
        self.checkbox.grid(row=4, column=1, sticky=tk.NSEW, padx=10)

    def Close_Window(self):
        """
        Funcion encargada de cerrar la ventana, pero sin
        finalizar la ejecucion del programa
        """
        global main_window
        main_window.destroy()

    ###########################################
    def search(self, root):
        """
        Funcion utilizada para crear un Combobox predictivo
        """
        widget = root.focus_get()
        if str(widget) == ".!frame.!combobox2":
            valor = combo_dependencias.get()
            if valor == "":
                combo_dependencias["value"] = lista_dep

            else:
                self.data = []

                for item in lista_dep:
                    if valor.upper() in item.upper():
                        self.data.append(item)
                combo_dependencias["value"] = self.data

        elif str(widget) == ".!frame.!combobox":
            valor = combo_personal.get()
            if valor == "":
                combo_personal["value"] = lista_personal

            else:
                self.data = []

                for item in lista_personal:
                    if valor.upper() in item.upper():
                        self.data.append(item)
                combo_personal["value"] = self.data

    def guardar_data(self):
        """
        Funcion encaragada de  chequear los datos ingresados, y luego
        pasar a guardarlos en el block de notas y el servidor.
        """
        self.key_usuario = self.usuario_real = combo_personal.get()
        self.key_dependecia = self.dependencia_real = combo_dependencias.get()

        if self.key_usuario in dicc_personal:  #  OK
            if self.key_dependecia in dicc_dependencias:  # OK
                a = self.data = self.model.general_info(
                    dicc_personal.get(self.key_usuario),
                    dicc_dependencias.get(self.key_dependecia),
                    checkbox_value.get(),
                    self.usuario_real,
                    self.dependencia_real,
                )
                return True
            else:
                messagebox.showerror(
                    message="Error nombre de dependencia", title="Datos Incorrectos"
                )
            return False
        else:
            messagebox.showerror(
                message="Error en nombre de usuario", title="Datos Incorrectos"
            )
            return False

    def Bind(self, root):
        """
        Funcion encargada de activar teclas de funcion
        """
        root.bind("<Return>", lambda event: self.Check_campos(root))
        combo_dependencias.bind("<KeyRelease>", lambda event: self.search(root))
        combo_personal.bind("<KeyRelease>", lambda event: self.search(root))

    def Check_campos(self, main_window):
        global masterchief

        """
        Funcion encargada de chequear que los campos no esten
        en blanco, y cumplan con la longitud minima.
        """
        if len(combo_personal.get()) == 0 or len(combo_dependencias.get()) == 0:
            messagebox.showerror(message="Completar campos.", title="Datos Incompletos")
            return
        else:
            a = self.guardar_data()
            if a == False:
                return
            elif a == True:
                messagebox.showinfo(
                    message="El proceso ha iniciado con exito.", title="Inicio Proceso"
                )

                self.Close_Window()
                #############
                self.Pc_nueva(masterchief)
                # self.socket_servidor = socket_servidor.Socket().Inicio_conexion(self.lista_datos_pc)

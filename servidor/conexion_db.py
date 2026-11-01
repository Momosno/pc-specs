from peewee import *
from peewee import MySQLDatabase, Model, PeeweeException, OperationalError
import pymysql
from playhouse.reflection import generate_models, print_model, print_table_sql
from tkinter import messagebox
from datetime import datetime
import os

"""
conexion_db.py:
Modulo encargado de la conexion con la base de datos MySQL.
Se usa la libreria peewee, por si se presenta la necesidad
de cambiar el tipo de base de datos, sea mucho mas agil 
y rapido el cambio.
"""


def Update_tabla_computadoras(lista):
    # print(lista[3])

    query = computadora.get_or_none(computadora.ip == lista[3])
    if query == None:

        computadora.create(
            nombre=lista[0],
            id_persona=lista[1],
            id_dependencia=lista[2],
            ip=lista[3],
            id_sistema_operativo=lista[4],
            id_procesador=lista[5],
            id_hd=lista[6],
            id_memoria=lista[7],
            tiene_ups=lista[8],
            red=0,
            fisica=0,
            observaciones=0,
            agregado_por=8,
            fecha_agregado=datetime.now().strftime("%Y-%m-%d"),
            editado_por=0,
        )
        print("creado")
    else:

        qry = computadora.update({computadora.nombre: lista[0]}).where(
            computadora.ip == lista[3]
        )
        qry.execute()
        qry = computadora.update({computadora.id_persona: lista[1]}).where(
            computadora.ip == lista[3]
        )
        qry.execute()
        qry = computadora.update({computadora.id_dependencia: lista[2]}).where(
            computadora.ip == lista[3]
        )
        qry.execute()
        qry = computadora.update({computadora.id_sistema_operativo: lista[4]}).where(
            computadora.ip == lista[3]
        )
        qry.execute()
        qry = computadora.update({computadora.id_procesador: lista[5]}).where(
            computadora.ip == lista[3]
        )
        qry.execute()
        qry = computadora.update({computadora.id_hd: lista[6]}).where(
            computadora.ip == lista[3]
        )
        qry.execute()
        qry = computadora.update({computadora.id_memoria: lista[7]}).where(
            computadora.ip == lista[3]
        )
        qry.execute()
        qry = computadora.update({computadora.tiene_ups: lista[8]}).where(
            computadora.ip == lista[3]
        )
        qry.execute()
        print("update")


def Add_procesador_ram(diccionario):
    """
    Convierto los datos reales de proc y ram al
    numero de id de las respectivas tablas.
    """

    #### PROCESADOR ####
    query = procesador.get_or_none(procesador.nombre == diccionario.get("procesador"))
    if query == None:
        procesador.create(nombre=diccionario.get("procesador"))

    query = procesador.select(procesador.id_procesador).where(
        procesador.nombre == diccionario.get("procesador")
    )
    for i in query:
        diccionario["procesador"] = str(i)

    ### RAM ###
    query = memoria.get_or_none(memoria.nombre == diccionario.get("ram"))

    if query == None:
        memoria.create(nombre=diccionario.get("ram"))

    query = memoria.select(memoria.id_memoria).where(
        memoria.nombre == diccionario.get("ram")
    )
    for i in query:
        diccionario["ram"] = str(i)
    # print(diccionario)

    Update_db(diccionario)


def Update_db(diccionario):
    """
    Trata de updatear pc_specs, sino crea un nuevo registro
    """

    lista = []
    for campo in diccionario:
        lista.append(diccionario.get(campo))
    print(lista)
    try:
        qry = Lista_Pc_Specs.get(Lista_Pc_Specs.ip == lista[3])

        qry = Lista_Pc_Specs.update({Lista_Pc_Specs.nombre_pc: lista[0]}).where(
            Lista_Pc_Specs.ip == lista[3]
        )
        qry.execute()
        qry = Lista_Pc_Specs.update({Lista_Pc_Specs.usuario: lista[1]}).where(
            Lista_Pc_Specs.ip == lista[3]
        )
        qry.execute()
        qry = Lista_Pc_Specs.update({Lista_Pc_Specs.dependencia: lista[2]}).where(
            Lista_Pc_Specs.ip == lista[3]
        )
        qry.execute()
        qry = Lista_Pc_Specs.update({Lista_Pc_Specs.so: lista[4]}).where(
            Lista_Pc_Specs.ip == lista[3]
        )
        qry.execute()
        qry = Lista_Pc_Specs.update({Lista_Pc_Specs.procesador: lista[5]}).where(
            Lista_Pc_Specs.ip == lista[3]
        )
        qry.execute()
        qry = Lista_Pc_Specs.update({Lista_Pc_Specs.hdd: lista[6]}).where(
            Lista_Pc_Specs.ip == lista[3]
        )
        qry.execute()
        qry = Lista_Pc_Specs.update({Lista_Pc_Specs.ram: lista[7]}).where(
            Lista_Pc_Specs.ip == lista[3]
        )
        qry.execute()
        qry = Lista_Pc_Specs.update({Lista_Pc_Specs.ups: lista[8]}).where(
            Lista_Pc_Specs.ip == lista[3]
        )
        qry.execute()
        Update_tabla_computadoras(lista)  # update tabla comutadoras

        """                                      SE PUEDE HACER MEJOR
                                                for i in campos:
                                                    Lista_Pc_Specs.update({Lista_Pc_Specs.i: lista[cont]}).where(
                                                        Lista_Pc_Specs.ip == lista[3]
                                                    )
                                                    cont += 1
                            """
    except:
        Alta_reg(lista)


def Alta_reg(lista):
    """
    Funcion encargada del alta de los datos en la base
    """

    # print(type(pc))
    Lista_Pc_Specs.create(
        nombre_pc=lista[0],
        usuario=lista[1],
        dependencia=lista[2],
        ip=lista[3],
        so=lista[4],
        procesador=lista[5],
        hdd=lista[6],
        ram=lista[7],
        ups=lista[8],
    )

    print("Caracteristicas obtenidas en la base de datos")
    Update_tabla_computadoras(lista)


def Actualizar_db_local():
    global dicc_personal, dicc_dependencia
    modelo = generate_models(conexion)
    globals().update(modelo)  # creo el "modelo" personal y dependencia
    # print_model(dependencia)  # (personal)
    lista_key = []
    lista_value = []

    for i in personal.select():
        # "APELLIDO, Nombre": 1,
        nombre = f"{i.apellido}, {i.nombre}"
        lista_key.append(nombre)
        lista_value.append(i.id_personal)

    dicc_personal = dict(zip(lista_key, lista_value))
    # print(dicc_personal)  # DICCIONARIO CON PERSONAL ACTUALIZADO

    lista_key = []
    lista_value = []
    for i in dependencia.select():
        # "Nombre de la dependencia": 1,
        lista_key.append(i.nombre)
        lista_value.append(i.id_dependencia)
    dicc_dependencia = dict(zip(lista_key, lista_value))
    # print(dicc_dependencia)  # DICCIONARIO CON DEPENDENCIAS ACTUALIZADO
    return dicc_dependencia, dicc_personal


"""
El resto del codigo no esta en una funcion, ya que 
a nuestras finalidades no era necesario, por lo que
el codigo era un distinto
"""


try:
    # Credenciales leidas de variables de entorno (ver README).
    conexion = MySQLDatabase(
        database=os.environ.get("PCSPECS_DB_NAME", "pc_specs"),
        user=os.environ.get("PCSPECS_DB_USER", "pc_specs_user"),
        password=os.environ.get("PCSPECS_DB_PASSWORD", ""),
        host=os.environ.get("PCSPECS_DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("PCSPECS_DB_PORT", "3306")),
    )

    class MySQLModel(Model):
        class Meta:
            database = conexion

    class Lista_Pc_Specs(MySQLModel):
        nombre_pc = CharField()
        usuario = TextField()
        dependencia = TextField()
        ip = TextField()
        so = TextField()
        procesador = TextField()
        hdd = IntegerField()
        ram = TextField()
        ups = BooleanField(default=False)

    conexion.connect()
    conexion.create_tables([Lista_Pc_Specs])
    print("Conexion Exitosa")

except OperationalError:
    messagebox.showinfo(
        message="No se ha podido conectar con la base de datos.\nRevise la conexion de red.",
        title="Problema de Conexion",
    )
    quit()

import os
import platform
import threading
import time


global cont, cont_inacc, lista_pc_on, cont_off
lista_pc_on = []
cont = cont_inacc = cont_off = 0

### Comienza a buscar en el rango ###|
def Worker(ip):
    global cont, cont_inacc, ip_base, lista_pc_on, cont_off

    ### Apertura "CMD" ###
    oper = platform.system()  # "Windows"
    cmd_ping = "ping -n 1 "  # comando para cmd

    ip_address = ip_base + str(ip)  # Junto ip base con el numero a buscar
    envio_cmd = cmd_ping + ip_address  # variable con comando del cmd + la ip a buscar

    response = os.popen(envio_cmd)  # respuesta del cmd

    ### LEE RTA DEL CMD ###
    for linea in response.readlines():
        if linea.count("TTL"):
            print(ip_address + "--> ON")
            cont += 1
            lista_pc_on.append(ip_address)
        elif linea.count("inaccesible"):
            print(ip_address + "--> Inaccesible")
            cont_inacc += 1
        elif linea.count("Tiempo de espera agotado"):
            print(ip_address + "--> OFF")
            cont_off += 1


def Hilos():
    global lista_pc_on
    threads = []
    for ip in range(start1, end1):
        t = threading.Thread(target=Worker, args=(ip,))
        threads.append(t)
        t.start()

    time.sleep(5)
    print("#" * 3 + " ON " + str(cont) + " ###")
    print("#" * 3 + " OFF " + str(cont_off) + " ###")
    print("#" * 3 + " Inaccesibles " + str(cont_inacc) + " ###")
    # print(lista_pc_on)
    return lista_pc_on


def Ingreso_datos():
    global start1, end1, ip_base
    # es de referencia para los primeros 3 octetos
    while True:
        net = input("Ingresar direccion de red: (192.168.0._) ")
        ip_temp = net.split(".")
        punto = "."
        try:
            ip_base = ip_temp[0] + punto + ip_temp[1] + punto + ip_temp[2] + punto
            break
        except (IndexError):
            print("Ip no valida")
            continue

    ### Rango a buscar ###
    start1 = int(input("Ingresar primer valor del rango: "))  # 1
    end1 = int(input("Ingresar ultimo valor del rango: "))  # 254
    end1 = end1 + 1

    return Hilos()

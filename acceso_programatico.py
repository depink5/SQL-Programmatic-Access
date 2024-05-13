#!/usr/bin/env python
# =============================================================================
# BASES DE DATOS - 2022/2023
# Denisa Alexandru 
# Dayana Cifuentes Zaruma
# Jimena Martin Reina
# =============================================================================


# In[1]
    
# IMPORTACIÓN DE MÓDULOS
#Primero importamos todos los módulos que vamos a necesitar para conectarnos a sql, el formato, ...
import mysql.connector
from mysql.connector import errorcode
from colorama import Fore, Back
import time
from sys import exit
from tabulate import tabulate


# In[2]

# CONEXIÓN CON LA BASE DE DATOS
#Primero definimos todos los parámetros necesarios para conectarnos con la base de datos de sql, el nombre, el puerto, la contraseña, ...
config = { 
    'host':'localhost',
    'port':'3306',
    'user':'disnet_user',
    'password':'disnet_pwd',
    'database':'disnet_drugslayer',
    }  
#Definimos el cursor de la base de datos
try: 
    db = mysql.connector.connect(**config)
    db.autocommit = True
    cursor = db.cursor(buffered=True)

## Errores de conexión
#Definimos los errores que pueden ocurrer al conectarse con la base de datos
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(Back.RED + "\nERROR: Nombre de usuario y/o contraseña incorrectos.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(Back.RED + "\nERROR: La base de datos '%s' no existe." % config.get('database'))
    elif err.errno == errorcode.CR_CONN_HOST_ERROR:
        print(Back.RED + "\nERROR: No se puede establecer conexión con el servidor en '%s':'%s'." % (config.get('host'), config.get('port')))
    elif err.errno == errorcode.CR_UNKNOWN_HOST:
        print(Back.RED + "\nERROR: El servidor '%s' es desconocido." % config.get('host'))
    else:
        print(Back.RED)
        print(err)
    exit()
   
        
# In[3]   

# MENÚ PRINCIPAL
#Aquí creamos el aspecto del menú principal con todos sus apartados 
#Definimos qué función se tiene que ejecutar según lo que escriba el usuario
#Si el usuario selecciona una opción que no está entre las posibles, imprime que es un error y que escoja otra
def menu_principal():
    ans=True
    while ans: #Se imprimen las opciones del menú
        print("\n")
        print(Back.CYAN + "===========================================================================")
        print(" "*(30) + "MENÚ PRINCIPAL" + " "*(31))
        print("===========================================================================" + Back.RESET)
        print("\n")
        print("[1]\t Información general de la base de datos")
        print("[2]\t Información de los fármacos")
        print("[3]\t Información de las enfermedades")
        print("[4]\t Información de los efectos fenotípicos")
        print("[5]\t Información de los targets")
        print("[6]\t Borrar asociación entre un fármaco y una enfermedad con score muy bajo")
        print("[7]\t Inserción de nuevas codificaciones de fármacos")
        print("[8]\t Modificación de los scores de asociación entre fármacos y efectos secundarios\n")
        print("[9]\t Salir")
        print("[+]\t Ayuda")  
   
        ans = (input(Back.CYAN + "\nEscoja una opción:" + Back.RESET + " \n"))
        if ans == "1": #Se llama al submenú 1
            menu1()
        elif ans == "2": #Se llama al submenú 2
            menu2()
        elif ans == "3": #Se llama al submenú 3
            menu3()
        elif ans == "4": #Se llama al submenú 4
            menu4()
        elif ans == "5": #Se llama al submenú 5
            menu5()
        elif ans == "6": #Se llama a la función de borrados
            borrados()
        elif ans == "7": #Se llama a la función de inserciones
            inserciones()
        elif ans == "8": #Se llama a la función de modificaciones
            modificaciones()
        elif ans == "9": #Se llama a la función salir(), que interrumpe el código
            salir()    
        elif ans == "+": #Se llama a la función ayuda(), que proporciona información sobre el código
            ayuda()
        else:
            print(Back.RED + "\nElección no válida. Escoja otra opción." + Back.RESET)
            time.sleep(1.5)
            
#Esta es la función subtitulo, que se usa para imprimir los títulos del menú en que nos encontramos en azul
def subtitulo(subtitulo):
    long = 75
    long_sub = len(subtitulo)
    espacio = (long-long_sub)/2
    print("\n")
    print(Fore.CYAN + '.'*long)
    print(" "*int(espacio) + subtitulo + " "*int(espacio))
    print('.'*long + Fore.RESET)

#Esta es la primera función para imprimir los ouput de las consultas, para consultas que sólo dan una cifra como resultado 
def output_a(query, tipo):
    cursor.execute(query)
    data = cursor.fetchall()
    print("\n\nEl número total de " + tipo + " es: ")
    for row in data:
        print(row[0])
 
#Esta es la segunda función para imprimir los ouput de las consultas, para cuando el resultado es una tabla de distintos valores
def output_b(query, titulo, cabecera):
    cursor.execute(query)
    data = cursor.fetchall()
    cab = cabecera.split('\t')
    if not data:
        print("\n\nNo se han obtenido resultados.") 
        #imprimimos este mensaje cuando no hay información, para que el usuario sepa que no hay información 
        #de la consulta que ha realizado, y no es que haya ningún error en el programa
    else:
        print("\n" + titulo + "\n")
        print(tabulate(data, headers=cab, tablefmt='psql'))
   

# In[4]  
#Esta es la función que crea el menú para realizar las consultas del ejercicio 1
# MENÚ 1 - Información general  
def menu1():
    ans1=True
    while ans1:
        #Primero imprimimos el submenú 1 con el enunciado de todos los apartados posibles
        subtitulo("[1]\t Información general de la base de datos")
        print('[1.1]\t Número total de fármacos' )
        print('[1.2]\t Número total de enfermedades' )
        print('[1.3]\t Número total de efectos fenotípicos' )
        print('[1.4]\t Número total de targets' )
        print('[1.5]\t Primeras 10 entradas de fármacos' )
        print('[1.6]\t Primeras 10 entradas de enfermedades' )
        print('[1.7]\t Primeras 10 entradas de efectos fenotípicos' )
        print('[1.8]\t Primeras 10 entradas de targets\n' )
        print('[x]\t Volver al menú principal')
        print('[y]\t Salir del programa')
        ans1 = (input(Fore.CYAN + "\nEscoja una opción:" + Fore.RESET + " \n"))
        if ans1 == "1.1":
            #Si el usuario introduce 1.1 hacemos la consulta correspondiente
            try:
                a1="SELECT COUNT(DISTINCT drug_id) as NumDrugs FROM drug;"
                output_a(a1, "fármacos")
            #Aquí imprimimos la información si ocurre algún error
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        elif ans1 == "1.2":
            #Si el usuario introduce 1.2 hacemos la consulta correspondiente
            try:
                a2="SELECT COUNT(DISTINCT disease_id) as NumDiseases FROM disease;"
                output_a(a2, "enfermedades")
            #Aquí imprimimos la información si ocurre algún error
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        elif ans1 == "1.3":
            #Si el usuario introduce 1.3 hacemos la consulta correspondiente
            try:
                a3="SELECT COUNT(DISTINCT phenotype_id) as NumPhenoEff FROM phenotype_effect;"
                output_a(a3, "efectos fenotípicos")
            #Aquí imprimimos la información si ocurre algún error
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "Se ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        elif ans1 == "1.4":
            #Si el usuario introduce 1.4 hacemos la consulta correspondiente
            try:
                a4="SELECT COUNT(DISTINCT target_id) as NumTargets FROM target;"
                output_a(a4, "targets")
            #Aquí imprimimos la información si ocurre algún error
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        elif ans1 == "1.5":
            #Si el usuario introduce 1.5 hacemos la consulta correspondiente
            try:
                b1="SELECT drug_id, drug_name, molecular_type, chemical_structure, inchi_key FROM drug WHERE drug_name IS NOT NULL AND  molecular_type is not null and chemical_structure is not null and inchi_key is not null LIMIT 10;"
                output_b(b1, "Las primeras 10 entradas de fármacos son: ", "ID\tNombre\tTipo molecular\tEstructura química\tInChI key")
            #Aquí imprimimos la información si ocurre algún error
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        elif ans1 == "1.6":
            #Si el usuario introduce 1.6 hacemos la consulta correspondiente
            try:
                b2="SELECT disease_id, disease_name FROM disease WHERE disease_name IS NOT NULL LIMIT 10;"
                output_b(b2, "Las primeras 10 entradas de enfermedades son: ", "ID\tNombre")
           #Aquí imprimimos la información si ocurre algún error
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        elif ans1 == "1.7":
            #Si el usuario introduce 1.7 hacemos la consulta correspondiente
            try:
                b3="SELECT phenotype_id, phenotype_name FROM phenotype_effect WHERE phenotype_name IS NOT NULL LIMIT 10;"
                output_b(b3, "Las primeras 10 entradas de efectos fenotípicos son: ", "ID\tNombre")
            #Aquí imprimimos la información si ocurre algún error
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        elif ans1 == "1.8":
            #Si el usuario introduce 1.8 hacemos la consulta correspondiente
            try:
                b4="SELECT target_id, target_name_pref, target_type, taxonomy_name FROM target t, organism o WHERE t.organism_id=o.taxonomy_id and target_name_pref IS NOT NULL AND  target_type is not null and taxonomy_name is not null LIMIT 10;"
                output_b(b4, "Las primeras 10 entradas de targets son: ", "ID\tNombre\tTipo\tOrganismo") 
            #Aquí imprimimos la información si ocurre algún error
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        
        #Si el usuario quiere volver al menú principal rompemos el ciclo while
        elif ans1 == "x" or ans1 == "X":
            break
        #Si el usuario quiere salir del programa empleamos la función salir que se explicará después
        elif ans1 == "y" or ans1 == "Y":
            salir()
        #Error por si el usuario selecciona una opción no válida
        else:
            print(Back.RED + "\nElección no válida. Escoja otra opción." + Back.RESET)
            time.sleep(1.5)
        time.sleep(3) #Dejamos que el resultado se quede unos segundos en pantalla para que le dé tiempo a leerlo al usuario


# In[5]
#Esta es la función que crea el menú para realizar las consultas del ejercicio 2
# MENÚ 2 - Información de fármacos
def menu2():
    ans2=True
    while ans2:
        #Primero imprimimos el submenú 2 con el enunciado de todos los apartados posibles
        subtitulo("[2]\t Información de los fármacos")
        print('[2.1]\t Detalles de fármaco dado su identificador ChEMBL' )
        print('[2.2]\t Posibles sínónimos de un fármaco dado su nombre' )
        print('[2.3]\t Códigos ATC de un fármaco dado su identificador ChEMBL\n' )
        print('[x]\t Volver al menú principal')
        print('[y]\t Salir del programa')
        ans2 = (input(Fore.CYAN + "\nEscoja una opción:" + Fore.RESET + " \n"))
        if ans2 == "2.1":
            #Si el usuario introduce 2.1 hacemos la consulta correspondiente
            try:
                #El usuario introduce los datos que hagan falta para realizar la consulta
                identificador=input("\nIntroduzca el identificador de ChEMBL del fármaco del que desea obtener información: ")
                a2="SELECT drug_name, molecular_type, chemical_structure, inchi_key FROM drug WHERE drug_id = '%s';" %(identificador)
                output_b(a2, "", "ID\tNombre\tTipo molecular\tEstructura química\tInChI key")
            #Aquí imprimimos la información si ocurre algún error
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        elif ans2 == "2.2":
            #Si el usuario introduce 2.2 hacemos la consulta correspondiente
            try:
                #El usuario introduce los datos que hagan falta para realizar la consulta
                nombre=input("\nIntroduzca el nombre del fármaco del que desea saber los sinónimos: ")
                b2="SELECT s.synonymous_name FROM drug d, synonymous s WHERE d.drug_name = '%s' AND d.drug_id = s.drug_id;" %(nombre)
                output_b(b2, "Los sinónimos del fármaco son: ", "Sinónimos")
           #Aquí imprimimos la información si ocurre algún error
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        elif ans2 == "2.3":
            #Si el usuario introduce 2.3 hacemos la consulta correspondiente
            try:
                #El usuario introduce los datos que hagan falta para realizar la consulta
                identificador2=input("\nIntroduzca el identificador de ChEMBL del fármaco cuyos códigos ATC desea saber: ")
                c2="SELECT atc.ATC_code_id FROM drug d, ATC_code atc WHERE d.drug_id = '%s' AND d.drug_id = atc.drug_id;" %(identificador2)
                output_b(c2, "Los códigos ATC son: ", "Códigos ATC")
            #Aquí imprimimos la información si ocurre algún error
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        #Si el usuario quiere volver al menú principal rompemos el ciclo while
        elif ans2 == "x" or ans2 == "X":
            break
        #Si el usuario quiere salir del programa empleamos la función salir que se explicará después
        elif ans2 == "y" or ans2 == "Y":
            salir()
        else:
            #Error por si el usuario selecciona una opción no válida
            print(Back.RED + "\nElección no válida. Escoja otra opción." + Back.RESET)
            time.sleep(1.5)
        time.sleep(3) #Dejamos que el resultado se quede unos segundos en pantalla para que le dé tiempo a leerlo al usuario


# In[6]
#Esta es la función que crea el menú para realizar las consultas del ejercicio 3
# MENÚ 3 - Información de enfermedades
def menu3():
    ans3=True
    while ans3:
        #Primero imprimimos el submenú 3 con el enunciado de todos los apartados posibles
        subtitulo("[3]\t Información de las enfermedades")
        print('[3.1]\t Fármacos para una enfermedad dada' )
        print('[3.2]\t Fármaco y enfermedad con mayor score de asociación\n' )
        print('[x]\t Volver al menú principal')
        print('[y]\t Salir del programa')
        ans3 = (input(Fore.CYAN + "\nEscoja una opción:" + Fore.RESET + " \n"))
        if ans3 == "3.1":
            #Si el usuario introduce 3.1 hacemos la consulta correspondiente
            try:
                #El usuario introduce los datos que hagan falta para realizar la consulta
                disease_name=input("\nIntroduzca el nombre de la enfermedad a buscar: ")
                a3="SELECT DISTINCT d.drug_id, d.drug_name FROM disease_code dc, drug d, drug_disease dd WHERE dc.code_id=dd.code_id AND dd.drug_id=d.drug_id AND dc.name = '%s';" %(disease_name)
                output_b(a3, "", "ID del fármaco\tNombre del fármaco")
           #Aquí imprimimos la información si ocurre algún error
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        elif ans3 == "3.2":
            #Si el usuario introduce 3.2 hacemos la consulta correspondiente
            try:
                b3="SELECT dc.name, d.drug_name, dd.inferred_score FROM disease_code dc, drug d, drug_disease dd WHERE dc.code_id=dd.code_id AND dd.drug_id=d.drug_id AND inferred_score IN (select max(inferred_score) FROM drug_disease);"
                output_b(b3, "Fármaco y enfermedad con mayor score de asociación: ", "Enfermedad\tFármaco\tScore")
            #Aquí imprimimos la información si ocurre algún error
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        #Si el usuario quiere volver al menú principal rompemos el ciclo while
        elif ans3 == "x" or ans3 == "X":
            break
        #Si el usuario quiere salir del programa empleamos la función salir que se explicará después
        elif ans3 == "y" or ans3 == "Y":
            salir()
        else:
            #Error por si el usuario selecciona una opción no válida
            print(Back.RED + "\nElección no válida. Escoja otra opción." + Back.RESET)
            time.sleep(1.5)
        time.sleep(3) #Dejamos que el resultado se quede unos segundos en pantalla para que le dé tiempo a leerlo al usuario


# In[7]
#Esta es la función que crea el menú para realizar las consultas del ejercicio 4
# MENÚ 4 - Información de efectos fenotípicos
def menu4():
    ans4=True
    while ans4:
        #Primero imprimimos el submenú 4 con el enunciado de todos los apartados posibles
        subtitulo("[4]\t Información de los efectos fenotípicos")
        print('[4.1]\t Indicaciones de un fármaco dado' )
        print('[4.2]\t Efectos secundarios de un fármaco dado\n' )
        print('[x]\t Volver al menú principal')
        print('[y]\t Salir del programa')
        ans4 = (input(Fore.CYAN + "\nEscoja una opción:" + Fore.RESET + " \n"))
        if ans4 == "4.1":
            #Si el usuario introduce 4.1 hacemos la consulta correspondiente
            try:
                #El usuario introduce los datos que hagan falta para realizar la consulta
                drug_id=input("\nIntroduzca el ID del fármaco a buscar: ")
                a4="SELECT pe.phenotype_id, pe.phenotype_name FROM phenotype_effect pe, drug d, drug_phenotype_effect dpe WHERE d.drug_id=dpe.drug_id AND dpe.phenotype_id=pe.phenotype_id AND d.drug_id = '%s';" %(drug_id)
                output_b(a4, "", "ID del fenotipo\tNombre del fenotipo")
            #Aquí imprimimos la información si ocurre algún error
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        elif ans4 == "4.2":
            #Si el usuario introduce 4.2 hacemos la consulta correspondiente
            try:
                #El usuario introduce los datos que hagan falta para realizar la consulta
                drug_id=input("\nIntroduzca el ID del fármaco a buscar: ")
                b4="SELECT pe.phenotype_id, pe.phenotype_name, dpe.score FROM drug_phenotype_effect dpe, phenotype_effect pe WHERE dpe.drug_id = '%s' AND dpe.phenotype_type = 'SIDE EFFECT' AND dpe.phenotype_id = pe.phenotype_id ORDER BY dpe.score DESC;" %(drug_id)
                output_b(b4, "Los efectos secundarios del fármaco dado ordenados por orden descendiente: ", "ID Fenotipo\tEfecto secundario\tScore")
            #Aquí imprimimos la información si ocurre algún error
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        #Si el usuario quiere volver al menú principal rompemos el ciclo while
        elif ans4 == "x" or ans4 == "X":
            break
        #Si el usuario quiere salir del programa empleamos la función salir que se explicará después
        elif ans4 == "y" or ans4 == "Y":
            salir()
        else:
            #Error por si el usuario selecciona una opción no válida
            print(Back.RED + "\nElección no válida. Escoja otra opción." + Back.RESET)
            time.sleep(1.5)
        time.sleep(3) #Dejamos que el resultado se quede unos segundos en pantalla para que le dé tiempo a leerlo al usuario


# In[8]
#Esta es la función que crea el menú para realizar las consultas del ejercicio 5
# MENÚ 5 - Información de targets
def menu5():
    ans5=True
    while ans5: 
        #Primero imprimimos el submenú 5 con el enunciado de todos los apartados posibles              
        subtitulo("[5]\t Información de los targets")
        print('[5.1]\t Dianas de un tipo dado' )
        print('[5.2]\t Organismo al cual se asocian un mayor número de dianas\n' )
        print('[x]\t Volver al menú principal')
        print('[y]\t Salir del programa')
        ans5 = (input(Fore.CYAN + "\nEscoja una opción:" + Fore.RESET + " \n"))
        if ans5 == "5.1":
            #Si el usuario introduce 5.1 hacemos la consulta correspondiente
            try:
                #El usuario introduce los datos que hagan falta para realizar la consulta
                diana=input("\nIntroduzca el tipo de diana de la que desea obtener las dianas: ")
                cinco_a="SELECT DISTINCT target_name_pref FROM target WHERE target_type = '%s' ORDER BY target_name_pref ASC LIMIT 20;" %(diana)
                output_b(cinco_a, "Las primeras 20 dianas del tipo dado son:", "Nombre de la diana")
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        elif ans5 == "5.2":
            #Si el usuario introduce 5.2 hacemos la consulta correspondiente
            try:
                cinco_b="SELECT o.taxonomy_name, COUNT(target_id) AS num_targets FROM target t, organism o WHERE  t.organism_id = o.taxonomy_id GROUP BY o.taxonomy_id ORDER BY num_targets DESC LIMIT 1;"
                output_b(cinco_b,"El organismo al cual se asocian el mayor número de dianas es:", "Nombre organismo\t Nº dianas asociadas")
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error: ")
                print(e)
                print(Back.RESET)
        #Si el usuario quiere volver al menú principal rompemos el ciclo while
        elif ans5 == "x" or ans5 == "X":
            break
        #Si el usuario quiere salir del programa empleamos la función salir que se explicará después
        elif ans5 == "y" or ans5 == "Y":
            salir()
        else:
            #Error por si el usuario selecciona una opción no válida
            print(Back.RED + "\nElección no válida. Escoja otra opción." + Back.RESET)
            time.sleep(1.5)
        time.sleep(3) #Dejamos que el resultado se quede unos segundos en pantalla para que le dé tiempo a leerlo al usuario


# In[9]
#Esta es la función que crea el menú para realizar las consultas del ejercicio 6
# MENÚ 6 - Borrado de asociación fármaco-enfermedad con score muy bajo
def borrados():
    #Imprimimos el título del apartado (aquí sólo hay uno)
    subtitulo("[6]\t Borrar asociación entre fármaco y enfermedad con score muy bajo")
    try:    
        #Ejecutamos la consulta de sql que muestra las 10 asociaciones fármaco-enfermedad con menor score
        seis="SELECT DISTINCT d.drug_name, dc.name, dd.inferred_score FROM disease_code dc, drug_disease dd, drug d WHERE dc.code_id = dd.code_id AND d.drug_id = dd.drug_id AND dd.inferred_score IS NOT NULL ORDER BY dd.inferred_score, d.drug_name, dc.name ASC LIMIT 10;"
        output_b(seis,"Las 10 asociaciones fármaco-enfermedad con menor score son: ","Nombre fármaco\tNombre enfermedad\tScore de asociación")
        ans6 = (input("\n¿Desea borrar alguna asociación? [S/N]:\t"))
        #Preguntamos al usuario si quiere borrar alguna asociación
        if ans6 == "N" or ans6 == "n": #Si no quiere, volvemos al menú principal
            menu_principal()
        elif ans6 == "S" or ans6 == "s": #Si quiere, ejecutamos la consulta de borrado de sql correspondiente
        #El usuario introduce los datos que hagan falta para realizar la consulta
            farmaco=input("\nIntroduzca el nombre del fármaco cuya asociación quiere borrar: ")
            enfermedad=input("\nIntroduzca el nombre de la enfermedad cuya asociación quiere borrar: ")
            print(("\nBorrando asociación '%s'-'%s'...")% (farmaco, enfermedad))
            delete="DELETE FROM drug_disease WHERE drug_id = (SELECT d.drug_id FROM drug d WHERE d.drug_name = '%s') AND code_id = (SELECT dc.code_id FROM disease_code dc WHERE dc.name = '%s');" %(farmaco, enfermedad)
            cursor.execute(delete)
            print("La asociación seleccionada se ha borrado correctamente.")
        #Imprimimos los errores
        else: 
            print(Back.RED + "\nElección no válida." + Back.RESET) #Error por si el usuario introduce una opción no válida
    except mysql.connector.Error as err:
        print(Back.RED + "\nSe ha producido el siguiente error: ")
        print(err)
        print(Back.RESET)
    except Exception as e:
        print(Back.RED + "\nSe ha producido el siguiente error: ")
        print(e)
        print(Back.RESET)
    time.sleep(3) #Dejamos que el resultado se quede unos segundos en pantalla para que le dé tiempo a leerlo al usuario


# In[10]
#Esta es la función que crea el menú para realizar las consultas del ejercicio 7
# MENÚ 7 - Inserción de nuevas codificaciones de fármacos
def inserciones():
    ans7=True
    while ans7:
        subtitulo("[7]\t Inserciones de nuevas codificaciones de fármacos")
        #Preguntamos al usuario si quiere realizar esta consulta por si se equivoca, para ahorrarle pasar por todos los pasos de introducir los datos para poder volver al menú principal
        ans7 = (input("\n¿Está seguro de continuar en este submenú? [S/N]:\t"))
        #si quiere seguir, el usuario introduce los datos que se van a insertar en la base de datos
        if ans7 == "S" or ans7=="s":
            try:
                #El usuario introduce los datos que hagan falta para realizar la consulta
                name= input("\nIntroduzca el nombre del fármaco del que desea añadir información: ")
                code_id= input("\nIntroduzca el código ID que quiere introducir: ")
                vocabulary=input("\nIntroduzca el vocabulario que desea añadir: ")
                siete="INSERT INTO drug_has_code (drug_id, code_id, vocabulary) VALUES ((SELECT drug_id FROM drug WHERE drug_name='%s'), '%s', '%s');" %name %code_id %vocabulary
                cursor.execute(siete)
                print("La inserción se ha realizado con éxito")
            #Si ocurren errores se imprimen en la pantalla
            except mysql.connector.Error as err:
                print(Back.RED + "\nSe ha producido el siguiente error:")
                print(err)
                print(Back.RESET)
            except Exception as e:
                print(Back.RED + "\nSe ha producido el siguiente error:")
                print(e)
                print(Back.RESET)
        #Si el usuario no quería hacer esta consulta, vuelve al menú principal rompiendo el bucle while
        elif ans7 == "N" or ans7 == "n":
            menu_principal()
            break
        #Error por si el usuario selecciona una opción no válida
        else:
            print(Back.RED + "\nElección no válida." + Back.RESET)
        time.sleep(3) #Dejamos que el resultado se quede unos segundos en pantalla para que le dé tiempo a leerlo al usuario


# In[11]
#Esta es la función que crea el menú para realizar las consultas del ejercicio 8
# MENÚ 8 - Modificación de score de asociación entre fármacos y efectos secundarios
def modificaciones():
    ans8=True
    while ans8:
        try:
            #Imprimimos el título del apartado
            subtitulo("[8]\t Modificaciones de los scores de asociaciones entre fármacos y efectos secundarios")
            #Preguntamos al igual que en el menú anterior si quiere volver al menú principal o si quiere hacer esta consulta
            ans8 = (input("\n¿Está seguro de continuar en este submenú? [S/N]:\t"))
            if ans8 == "N" or ans8 == "n":
                menu_principal()
                break
            elif ans8 == "S" or ans8 == "s":
                #Si el usuario quiere hacer la consulta, introduce el score de asociación umbral, todos los scores menores que ese se actualizarán con valor 0
                score=input("\nIntroduzca el score de asociación utilizado como umbral: ")
                ocho="UPDATE drug_phenotype_effect SET score=0 WHERE phenotype_type='SIDE EFFECT' AND score < '%s';" %(score)
                cursor.execute(ocho)
                print("La modificación se ha realizado con éxito.")
            #Error por si el usuario selecciona una opción no válida
            else:
                print(Back.RED + "\nElección no válida." + Back.RESET)
        #Imprimimos los errores
        except mysql.connector.Error as err:
            print(Back.RED + "\nSe ha producido el siguiente error: ")
            print(err)
            print(Back.RESET)
        except Exception as e:
            print(Back.RED + "\nSe ha producido el siguiente error: ")
            print(e)
            print(Back.RESET)
        time.sleep(3) #Dejamos que el resultado se quede unos segundos en pantalla para que le dé tiempo a leerlo al usuario
 
    
# In[12]
#Esta es la función salir, que sale del programa y es importante porque cierra la conexión 
def salir():
    subtitulo("Gracias por utilizar este programa")
    time.sleep(1.5)
    cursor.close()
    db.close()
    exit()
    
    
# In[13]
#Esta es la función ayuda, que muestra la información sobre le programa en pantalla durante unos segundos en la pantalla
def ayuda():
    subtitulo("[+]\t Ayuda")
    print("\nEste programa forma parte de la práctica de acceso programático de la asignatura"
          "\n“Bases de datos” del grado en Biotecnología, UPM."
          "\nSe trata de un script Python que permite acceder a la base de datos “disnet_drugslayer”"
          "\ne interactuar con la misma tanto para obtener información sobre dicha base como"
          "\npara hacer borrados, inserciones y/o modificaciones.")

    print(Back.CYAN + "\n\nEstructura de la base de datos" + Back.RESET)
    print(Fore.CYAN + "\t· Drug:" + Fore.RESET + " información relativa a cada fármaco. Es la tabla principal. Se complementa"
          "\n\t  con otras tablas como ‘ATC_code’, ‘drug_has_code’ y ‘synonymous’."
          + Fore.CYAN + "\n\t· Disease:" + Fore.RESET + " información relativa a las enfermedades. Se complementa con tablas como"
          "\n\t  ‘disease_has_code’, ‘disease_code’ y ‘drug_disease’."
          + Fore.CYAN + "\n\t· Phenotype_effect:" + Fore.RESET + " información relativa a los efectos fenotípicos y su relación con"
          "\n\t  los fármacos (drug_phenotype_effect)."
          + Fore.CYAN + "\n\t· Target:" + Fore.RESET + " información relativa a dianas terapéuticas de fármacos. Se complementa con"
          "\n\t  otras tablas como ‘organism’, ‘target_has_code’ y ‘drug_target’.")

    print(Back.CYAN + "\n\nUso del programa" + Back.RESET)
    print("La interacción usuario-máquina se produce introduciendo la opción deseada por teclado."
         "\nEl menú principal está formado por 10 opciones, 8 de las cuales permiten acceder a"
         "\ndistintos submenús, los cuales contienen opciones relacionadas con la base de datos"
         "\ny también de vuelta al menú principal o salida del programa.\n\n")
    time.sleep(4)
  

# In[14]
menu_principal()

# Autor: Nicolas Casanova

import os
import csv

contactos = []

ARCHIVO = 'contactos.csv'

def cargar_contactos():
    """Carga los contactos desde el archivo CSV si existe"""
    global contactos
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                contactos.append({'nombre': row['nombre'].strip(), 'correo': row['correo'].strip()})
    else:
        print("No se encontró el archivo de contactos. Se creará uno nuevo")

def guardar_contactos():
    """Guarda todos los contactos en el CSV Formato: columnas 'nombre' y 'correo'"""
    with open(ARCHIVO, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['nombre', 'correo']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for contacto in contactos:
            writer.writerow(contacto)
    print("Contactos guardados")

def registrar_contacto():
    """Registra un nuevo contacto solicitando nombre y correo"""
    nombre = input("Ingrese el nombre del contacto: ").strip()
    if not nombre:
        print("El nombre no puede estar vacío")
        return
    
    correo = input("Ingrese el correo del contacto: ").strip()
    if not correo:
        print("El correo no puede estar vacío")
        return
    
    # Verificar si ya existe un contacto con el mismo nombre o correo
    for c in contactos:
        if c['nombre'].lower() == nombre.lower() or c['correo'].lower() == correo.lower():
            print("Ya existe un contacto con ese nombre o correo.")
            return
    
    nuevo_contacto = {'nombre': nombre, 'correo': correo}
    contactos.append(nuevo_contacto)
    print(f"Contacto '{nombre}' registrado exitosamente.")
    guardar_contactos()  # Guardar inmediatamente después de agregar

def buscar_contacto():
    """ Busca un contacto por nombre o correo"""
    if not contactos:
        print("No hay contactos registrados.")
        return
    
    termino = input("Ingrese el nombre o correo a buscar: ").strip().lower()
    if not termino:
        print("El término de búsqueda no puede estar vacío.")
        return
    
    encontrado = False
    for contacto in contactos:
        if (contacto['nombre'].lower() == termino or 
            contacto['correo'].lower() == termino):
            print(f"Contacto encontrado: {contacto['nombre']} - {contacto['correo']}")
            encontrado = True
            break
    
    if not encontrado:
        print("No se encontró ningún contacto con ese nombre o correo")

def listar_contactos():
    """Lista todos los contactos registrados"""
    if not contactos:
        print("No hay contactos registrados")
        return
    
    print("\n Lista de Contactos")
    for i, contacto in enumerate(contactos, 1):
        print(f"{i}. {contacto['nombre']} - {contacto['correo']}")

def eliminar_contacto():
    """Elimina un contacto existente por nombre o correo"""
    if not contactos:
        print("No hay contactos registrados")
        return
    
    termino = input("Ingrese el nombre o correo del contacto a eliminar: ").strip().lower()
    if not termino:
        print("El término no puede estar vacío")
        return
    
    encontrado = False
    for i, contacto in enumerate(contactos):
        if (contacto['nombre'].lower() == termino or 
            contacto['correo'].lower() == termino):
            print(f"Contacto a eliminar: {contacto['nombre']} - {contacto['correo']}")
            confirmacion = input("¿Está seguro de eliminarlo? (s/n): ").strip().lower()
            if confirmacion == 's':
                del contactos[i]
                print("Contacto eliminado exitosamente.")
                guardar_contactos()  # Guardar después de eliminar
            else:
                print("Eliminación cancelada")
            encontrado = True
            break
    
    if not encontrado:
        print("No se encontró ningún contacto con ese nombre o correo")

def menu_principal():
    """Muestra el menú principal y maneja las opciones del usuario"""
    cargar_contactos()  # Cargar al inicio
    while True:
        print("\n AGENDA DE CONTACTOS ")
        print("1. Registrar nuevo contacto")
        print("2. Buscar contacto por nombre o correo")
        print("3. Listar todos los contactos")
        print("4. Eliminar contacto")
        print("5. Salir")
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        if opcion == '1':
            registrar_contacto()
        elif opcion == '2':
            buscar_contacto()
        elif opcion == '3':
            listar_contactos()
        elif opcion == '4':
            eliminar_contacto()
        elif opcion == '5':
            guardar_contactos()  # Guardar al salir
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente nuevamente")

# Ejecutar el programa
if __name__ == "__main__":
    menu_principal()
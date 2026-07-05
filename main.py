# Importamos los 5 módulos desarrollados por el equipo
import equipos
import preventivo
import correctivo
import stock
import reportes

def mostrar_encabezado():
    print("\n" + "="*50)
    print(" SISTEMA DE CONTROL DE MAQUINARIA PESADA ".center(50, "="))
    print("="*50)
    print("1. Gestión de Equipos y Catálogo")
    print("2. Mantenimiento Preventivo (Programación)")
    print("3. Mantenimiento Correctivo (Registro de Fallas)")
    print("4. Control de Stock de Repuestos")
    print("5. Indicadores y Reportes Operativos")
    print("6. Salir del Sistema")
    print("="*50)

def main():
    while True:
        mostrar_encabezado()
        try:
            opcion = int(input("Seleccione un módulo (1-6): "))
            
            if opcion == 1:
                # Se asume que el compañero 1 creó una función principal en equipos.py
                print("\n--- Entrando a Gestión de Equipos ---")
                equipos.menu_equipos() 
                
            elif opcion == 2:
                print("\n--- Entrando a Mantenimiento Preventivo ---")
                preventivo.menu_preventivo()
                
            elif opcion == 3:
                print("\n--- Entrando a Mantenimiento Correctivo ---")
                correctivo.menu_correctivo()
                
            elif opcion == 4:
                print("\n--- Entrando a Control de Stock ---")
                stock.menu_stock()
                
            elif opcion == 5:
                print("\n--- Entrando a Reportes ---")
                reportes.menu_reportes()
                
            elif opcion == 6:
                print("\nCerrando el sistema. ¡Operación finalizada con éxito!")
                break
                
            else:
                print("\n[!] Error: Por favor seleccione una opción válida entre 1 y 6.")
                
        except ValueError:
            print("\n[!] Error crítico: Entrada inválida. Ingrese únicamente números.")
        except AttributeError as e:
            print(f"\n[!] Error de integración: Falta definir la función principal en el módulo llamado. ({e})")

if __name__ == "__main__":
    main()

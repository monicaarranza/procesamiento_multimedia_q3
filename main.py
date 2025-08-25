import os
import time

try:
    import proyecto
    import sunset
    import cielo
    import marine
except ImportError as e:
    print(f"Error: No se pudo importar un módulo de escena: {e}")
    print("Asegúrate de que los archivos 'proyecto.py', 'sunset.py', 'cielo.py' y 'marine.py' están en la misma carpeta.")
    exit()

class Style:
   
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
 
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
  
    END = '\033[0m'

def clear_screen():
    
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    
    clear_screen()
    print(Style.PURPLE + Style.BOLD)
   
    print(" " * 15 + "GENERADOR DE FIGURAS CON PYTHON Y C++" + " " * 16)
    
    print(Style.END)

    print(Style.YELLOW + "\n  Elige una escena para generar:" + Style.END)

    print(f"\n  {Style.CYAN}[1]{Style.END} {Style.BOLD}Figuras de Prueba{Style.END} ")
    print(f"  {Style.CYAN}[2]{Style.END} {Style.BOLD}Atardecer{Style.END} ")
    print(f"  {Style.CYAN}[3]{Style.END} {Style.BOLD}Cielo{Style.END}")
    print(f"  {Style.CYAN}[4]{Style.END} {Style.BOLD}Escena Marina{Style.END}")

    print(f"\n  {Style.RED}[5]{Style.END} {Style.BOLD}Salir del programa{Style.END}")
    print("\n" + "-"*60)

def main():

    while True:
        display_menu()
        choice = input(Style.GREEN + Style.BOLD + "  >> Ingresa tu opción: " + Style.END)

        clear_screen()
        if choice == '1':
            proyecto.run_scene()
        elif choice == '2':
            sunset.run_scene()
        elif choice == '3':
            cielo.run_scene()
        elif choice == '4':
            marine.run_scene()
        elif choice == '5':
            print(Style.BLUE + Style.BOLD + "\nbye\n" + Style.END)
            time.sleep(1)
            break
        else:
            print(Style.RED + Style.BOLD + "\nOpción no válida. Por favor, intenta de nuevo." + Style.END)

       
        input(Style.YELLOW + "\n\nPresiona Enter para volver al menu principal..." + Style.END)

if __name__ == "__main__":
    main()
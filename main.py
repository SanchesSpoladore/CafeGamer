from controllers.nav_controller import iniciar_servidor
from controllers._db_controller import Inicio
from os import system

def main():
    system('cls')
    Inicio()  
    iniciar_servidor()

if __name__ == "__main__":
    main()
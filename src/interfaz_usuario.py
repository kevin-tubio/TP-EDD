from tweet_downloader import TweetDownloader
from excepciones import OperacionCanceladaException
from time import sleep
import buscador
import indexador

class UI:

    def accion(self):
        try:
            while True:
                self.__desplegar_menu()
                n = input("")
                self.limpiar_consola()
                opciones = {
                    "1": TweetDownloader().descargar,
                    "2": self.__buscadorMenu(),
                }
                if(n == "3"):
                    raise KeyboardInterrupt()
                try:
                    opciones.get(n, lambda: {self.desplegar_mensaje("Opcion invalida."), sleep(1)})()
                    self.limpiar_consola()
                except OperacionCanceladaException as e:
                    print(e)
                    
                

        except KeyboardInterrupt:
            self.cerrar_programa()

    def __desplegar_menu(self):
        print("|************************************************************************|")
        print("| 1) Descargar Tweets                                                    |")
        print("| 2) Buscador de Tweets                                                  |")
        print("| 3) Cerrar                                                              |")
        print("|________________________________________________________________________|")
        print()
        
    def __desplegar_menu_buscador(self):
        print("|************************************************************************|")
        print("| 1) Buscar por palabra                                                  |")
        print("| 2) Buscar por frase                                                    |")
        print("| 3) Buscar por fecha y hora                                             |")
        print("|________________________________________________________________________|")
        print()

    def desplegar_confirmacion(self, mensaje):
        print("|************************************************************************|")
        print(f"| {mensaje}",                    f"{self.__espacios_en_blanco(mensaje)} |")
        print(f"| {self.__espacios_en_blanco('¿Continuar?')}",        f"{'¿Continuar?'} |")
        print("|                                                                    s/n |")
        print("|________________________________________________________________________|")
        print()
        self.__confirmar()
        
    def __buscadorMenu(self):
        self.__desplegar_menu_buscador()
        n2 = input("")
        self.limpiar_consola()
        opciones2 = {
            "1": self.buscadorPalabra(),
            "2": print("WIP"),
            "3": print("WIP"),
            }
                    
        try:
            opciones2.get(n2, lambda: {self.desplegar_mensaje("Opcion invalida."), sleep(1)})()
            self.limpiar_consola()
        except OperacionCanceladaException as e:
            print(e)
                
    #NO FUNCIONA            
    def buscadorPalabra(self):
        #Cambiar el formato, queda feo este input
        print("|************************************************************************|")
        palabra = input("| Escriba la palabra a buscar:                                           |")
        print("|________________________________________________________________________|")
        print()
        
        b = buscador()
        i = indexador()
        palabra_lematizada = i.__lematizar(palabra)
        
        b.buscar_palabra(palabra_lematizada, a.obtener_indice_palabra_id(palabra_lematizada), 100)

    def __confirmar(self):
        while True:
            n = input("")
            if n == "s":
                break
            elif n == "n":
                self.cancelar_operacion()
            else:
                self.desplegar_mensaje("Presione 's' para aceptar o 'n' para cancelar")

    def cancelar_operacion(self):
        self.limpiar_consola()
        raise OperacionCanceladaException()

    def __espacios_en_blanco(self, mensaje):
        return " " * (69 - len(mensaje))

    def desplegar_mensaje(self, mensaje):
        print("|************************************************************************|")
        print(f"| {mensaje}",                    f"{self.__espacios_en_blanco(mensaje)} |")
        print("|________________________________________________________________________|")
        print()

    def cerrar_programa(self):
        self.desplegar_mensaje("Programa finalizado")

    def limpiar_consola(self):
        print("\033[H\033[J")
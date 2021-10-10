from tweet_downloader import TweetDownloader
from excepciones import OperacionCanceladaException
#import buscador

class UI:

    def accion(self):
        try:
            while True:
                self.__desplegar_menu__()
                n = input("")
                self.limpiar_consola()
                opciones = {
                    "1": TweetDownloader().descargar,
                    #"2": buscador.Buscador().buscar,
                }
                if(n == "3"):
                    raise KeyboardInterrupt()
                try:
                    opciones.get(n, lambda: self.desplegar_mensaje("Opcion invalida."))()
                    self.limpiar_consola()
                except OperacionCanceladaException as e:
                    print(e)

        except KeyboardInterrupt:
            self.cerrar_programa()

    def __desplegar_menu__(self):
        print("|************************************************************************|")
        print("| 1) Descargar Tweets                                                    |")
        print("| 2) Buscador de palabras                                                |")
        print("| 3) Cerrar                                                              |")
        print("|________________________________________________________________________|")
        print()

    def desplegar_confirmacion(self, mensaje):
        print("|************************************************************************|")
        print(f"| {mensaje}",                  f"{self.__espacios_en_blanco__(mensaje)} |")
        print(f"| {self.__espacios_en_blanco__('¿Continuar?')}",      f"{'¿Continuar?'} |")
        print("|                                                                    s/n |")
        print("|________________________________________________________________________|")
        print()
        self.__confirmar__()

    def __confirmar__(self):
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

    def __espacios_en_blanco__(self, mensaje):
        return " " * (69 - len(mensaje))

    def desplegar_mensaje(self, mensaje):
        print("|************************************************************************|")
        print(f"| {mensaje}",                  f"{self.__espacios_en_blanco__(mensaje)} |")
        print("|________________________________________________________________________|")
        print()

    def cerrar_programa(self):
        self.desplegar_mensaje("Programa finalizado")

    def ejecutar_accion(self, accion):
        accion()

    def limpiar_consola(self):
        print("\033[H\033[J")
from tweet_downloader import TweetDownloader
from excepciones import OperacionCanceladaException
from buscador import Buscador
from indexador import Indexador
from os import system, name, path

class UI:

    def accion(self):
        self._ejecutando = True
        while self._ejecutando:
            try:
                self.__desplegar_menu()
                n = input("")
                self.limpiar_consola()
                opciones = {
                    "1": TweetDownloader().descargar,
                    "2": self.indexar,
                    "3": self.__buscador_menu,
                    "4": self.cerrar_programa,
                }
                opciones.get(n, lambda: self.desplegar_mensaje("Opcion invalida."))()
            except OperacionCanceladaException as e:
                print(e)
            except KeyboardInterrupt:
                self.cerrar_programa()

    def __desplegar_menu(self):
        print("|************************************************************************|")
        print("| 1) Descargar Tweets                                                    |")
        print("| 2) Indexar (Necesario para buscar)                                     |")
        print("| 3) Buscador de Tweets                                                  |")
        print("| 4) Cerrar                                                              |")
        print("|________________________________________________________________________|")
        print()

    def __desplegar_menu_buscador(self):
        print("|************************************************************************|")
        print("| 1) Buscar por palabra                                                  |")
        print("| 2) Buscar por frase                                                    |")
        print("| 3) Buscar por fecha y hora                                             |")
        print("| 4) Buscar por usuario                                                  |")
        print("| 5) Regresar al menú principal                                          |")
        print("| 6) Cerrar programa                                                     |")
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

    def __buscador_menu(self):
        if self.__comprobar_indexado():
            self.__comprobar_buscador()
            self.__desplegar_menu_buscador()
            n2 = input("")
            self.limpiar_consola()
            opciones2 = {
            #    "1": self.buscador_palabra,
            #    "2": print("WIP"),
            #    "3": print("WIP"),
                "4": self.buscador_usuario, 
                "5": self.limpiar_consola,
                "6": self.cerrar_programa,
            }

            try:
                opciones2.get(n2, lambda: self.desplegar_mensaje("Opcion invalida."))()
            except OperacionCanceladaException as e:
                print(e)

    def indexar(self):
        self.i = Indexador()
        self.i.indexar()

    def __comprobar_indexado(self):
        if not path.isfile("salida\posting_palabras.json"):
            self.desplegar_mensaje("ADVERTENCIA: Se debe indexar antes de buscar.")
            self.desplegar_mensaje("Pulse enter para volver al menú principal.")
            input("")
            return False
        else:
            if  not hasattr(self, "self.i"):
                self.i = Indexador()
                return True
            else:
                return True

    def __comprobar_buscador(self) -> None:
        if not hasattr(self, "self.b"):
            self.b = Buscador()

    #NO FUNCIONA
    def buscador_preguntar(self, mensaje : str) -> str:
        #Cambiar el formato, queda feo este input
        print("|************************************************************************|")
        print(f"| {mensaje}",                    f"{self.__espacios_en_blanco(mensaje)} |")
        print("|________________________________________________________________________|")
        busqueda = input("")
        print()

        return busqueda

    def buscador_usuario(self):
        usuario = self.buscador_preguntar("Escriba el usuario a buscar")
        print(self.b.buscar_usuario(usuario))
        input("Presione enter para continuar")

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
        self._ejecutando = False
        self.desplegar_mensaje("Programa finalizado")

    def limpiar_consola(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

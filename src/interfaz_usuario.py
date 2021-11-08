from typing import List
from tweet_downloader import TweetDownloader
from excepciones import OperacionCanceladaException
from buscador import Buscador
from indexador import Indexador
from datetime import datetime
from pandas import date_range
import re
from os import system, name, path

class UI:

    def __init__(self) -> None:
        self._buscador = Buscador()
        self._indexador = Indexador()
        self._descargador = TweetDownloader()

    def accion(self) -> None:
        self._ejecutando = True
        while self._ejecutando:
            try:
                self.__desplegar_menu()
                n = input("")
                self.limpiar_consola()
                opciones = {
                    "1": self._descargador.descargar,
                    "2": self._indexador.indexar,
                    "3": self.__buscador_menu,
                    "4": self.cerrar_programa,
                }
                opciones.get(n, lambda: self.desplegar_mensaje("Opcion invalida."))()
            except OperacionCanceladaException as e:
                print(e)
            except KeyboardInterrupt:
                self.cerrar_programa()

    def __desplegar_menu(self) -> None:
        print("|************************************************************************|")
        print("| 1) Descargar Tweets                                                    |")
        print("| 2) Indexar (Necesario para buscar)                                     |")
        print("| 3) Buscador de Tweets                                                  |")
        print("| 4) Cerrar                                                              |")
        print("|________________________________________________________________________|")
        print()

    def __desplegar_menu_buscador(self) -> None:
        print("|************************************************************************|")
        print("| 1) Buscar por palabra                                                  |")
        print("| 2) Buscar por frase                                                    |")
        print("| 3) Buscar por fecha y hora                                             |")
        print("| 4) Buscar por usuario                                                  |")
        print("| 5) Regresar al menú principal                                          |")
        print("|________________________________________________________________________|")
        print()

    def desplegar_confirmacion(self, mensaje) -> None:
        print("|************************************************************************|")
        print(f"| {mensaje}",                    f"{self.__espacios_en_blanco(mensaje)} |")
        print(f"| {self.__espacios_en_blanco('¿Continuar?')}",        f"{'¿Continuar?'} |")
        print("|                                                                    s/n |")
        print("|________________________________________________________________________|")
        print()
        self.__confirmar()

    def __buscador_menu(self) -> None:
        if self.__comprobar_indexado():
            self.__desplegar_menu_buscador()
            n2 = input("")
            self.limpiar_consola()
            opciones = {
                "1": self.buscador_palabra,
                "2": self.buscador_frase,
                "3": self.buscador_fecha,
                "4": self.buscador_usuario,
                "5": self.limpiar_consola,
            }
            try:
                opciones.get(n2, lambda: self.desplegar_mensaje("Opcion invalida."))()
            except OperacionCanceladaException as e:
                print(e)

    def __comprobar_indexado(self) -> bool:
        if not path.isfile("salida\posting_palabras.json"):
            self.desplegar_mensaje("ADVERTENCIA: Se debe indexar antes de buscar.")
            self.desplegar_mensaje("Pulse enter para volver al menú principal.")
            input("")
            return False
        return True

    def buscador_preguntar(self, mensaje : str) -> str:
        self.desplegar_mensaje(mensaje)
        busqueda = input("")
        return busqueda

    def buscador_usuario(self) -> None:
        busqueda = list()
        busqueda.append(self.buscador_preguntar("Escriba el usuario a buscar"))
        self.__presentar_resultados(self._buscador.buscar_usuario(busqueda))

    def buscador_palabra(self) -> None:
        busqueda = list()
        busqueda.append(self.buscador_preguntar("Escriba la palabra a buscar"))
        self.__presentar_resultados(self._buscador.buscar_palabra(busqueda))

    def buscador_frase(self) -> None:
        frase = self.buscador_preguntar("Escriba su frase a buscar")
        self.__presentar_resultados(self._buscador.buscar_frase(frase))

    def buscador_fecha(self) -> None:
        fecha_inicial = self.solicitar_fecha("desde")
        fecha_final = self.solicitar_fecha("hasta")
        while fecha_inicial > fecha_final:
            self.desplegar_confirmacion("El rango de fechas ingresado no es valido.")
            fecha_final = self.solicitar_fecha("hasta")
        cantidad = int(self.buscador_preguntar("Ingrese la cantidad de tweets a buscar"))
        usuario = self.buscador_preguntar("Ingrese un nombre de usuario")
        lista_fechas = self.armar_lista_fechas(fecha_inicial, fecha_final)
        self.__presentar_resultados(self._buscador.buscar_fechas(lista_fechas, cantidad, usuario))

    def __presentar_resultados(self, resultados: set) -> None:
        for tweet in resultados:
            print(tweet)
        input("Presione enter para continuar")
        self.limpiar_consola()

    def armar_lista_fechas(self, fecha_inicial: datetime, fecha_final: datetime) -> List[str]:
        return list(date_range(start=fecha_inicial, end=fecha_final, freq="min").strftime("%d/%m/%Y %H:%M"))

    def solicitar_fecha(self, mensaje: str) -> datetime:
        mensaje = f"Escriba la fecha {mensaje} la cual buscar, en formato DD/MM/AAAA HH:MM"
        fecha = self.buscador_preguntar(mensaje)
        while not self.__es_fecha_valida(fecha):
            self.desplegar_confirmacion("La fecha ingresada no es valida, intente nuevamente")
            fecha = self.buscador_preguntar(mensaje)
        fecha = datetime.strptime(fecha, "%d/%m/%Y %H:%M")
        return fecha

    def __es_fecha_valida(self, fecha: str) -> bool:
        regex = re.compile(r"^(?:0[1-9]|[1-2]\d|3[0-1])/(?:0[1-9]|1[0-2])/2021 (?:[0-1]\d|2[0-4]):[0-5]\d")
        return regex.match(fecha)

    def __confirmar(self) -> None:
        while True:
            n = input("")
            if n == "s":
                break
            elif n == "n":
                self.cancelar_operacion()
            else:
                self.desplegar_mensaje("Presione 's' para aceptar o 'n' para cancelar")

    def cancelar_operacion(self) -> None:
        self.limpiar_consola()
        raise OperacionCanceladaException()

    def __espacios_en_blanco(self, mensaje: str) -> str:
        return " " * (69 - len(mensaje))

    def desplegar_mensaje(self, mensaje) -> None:
        print("|************************************************************************|")
        print(f"| {mensaje}",                    f"{self.__espacios_en_blanco(mensaje)} |")
        print("|________________________________________________________________________|")
        print()

    def cerrar_programa(self) -> None:
        self._ejecutando = False
        self.desplegar_mensaje("Programa finalizado")

    def limpiar_consola(self) -> None:
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

from datetime import datetime
import re
from excepciones import FechaInvalidaException, TerminoNoEncontradoException
import json

class Buscador:

    def __init__(self):
        self.__formato_hora = re.compile("^(?:[0-1]\d|2[0-4]):[0-5]\d$")
        self.__formato_fecha = re.compile("^(?:0[1-9]|[1-2]\d|3[0-1])/(?:0[1-9]|1[0-2])/2021$")

    def buscar_fecha_hora(self, fecha_1 : str, hora_1 : str, cantidad : int, indice : dict, fecha_2="", hora_2=""):
        self.__validar_cantidad(cantidad)
        self.__validar_fecha(fecha_1)
        self.__validar_hora(hora_1)
        dt = datetime.strptime(f"{fecha_1} {hora_1}", "%d/%m/%Y %H:%M")
        n = 0
        lista_id = []
        #opcional falta que aumente n por cada adicion pero no se como
        #lista_id = [id for date, id in indice if dt <= date and n < cantidad]
        if fecha_2 == "" or hora_2 == "":
            #problema, itera todo, si indice[fecha] entonces que pasa si no llega a n las adiciones?
            for date, id in range(indice, cantidad):
                if dt <= date and n < cantidad:
                    lista_id.append(id)
                    n += 1
                    if n == cantidad:
                        break
        else:
            self.__validar_fecha(fecha_2)
            self.__validar_hora(hora_2)
            dt2 = datetime.strptime(f"{fecha_2} {hora_2}", "%d/%m/%Y %H:%M")
            #opcional tiene el problema de iterar todos los valores a menos que le pongas un break
            #lista_id = [id for date, id in indice if dt <= date <= dt2 and n < cantidad]
            for date, id in indice:
                if dt <= date <= dt2 and n < cantidad:
                    lista_id.append(id)
                    n += 1
                    if n == cantidad:
                        break
        return set(lista_id)

    def buscar_usuario(self, usuario):
        return self.__obtener_tweet(self.__obtener_lista_tweet_id("usuarios", usuario))

    def buscar_palabra(self, palabra):
        return self.__obtener_tweet(self.__obtener_lista_tweet_id("palabras", palabra))

    def buscar_frase(self, frase):
        palabras = frase.split()
        aux = list()
        for pal in palabras:
            a = self.__obtener_lista_tweet_id("palabras", pal)
            if a:
                for ids in a:
                    aux.append(ids)
        duplicated = set([i for i in aux if aux.count(i) > 1])
        if len(duplicated) == 0:
            return f"No existe un tweet con la frase: '{frase}'"
        else:
            return self.__obtener_tweet(duplicated)

    def buscar_fecha(self, fecha):
        return self.__obtener_tweet(self.__obtener_lista_tweet_id("fechas", fecha))

    def __obtener_lista_tweet_id(self, nombre: str, termino: str) -> list:
        ruta_dict = f"./salida/diccionario_{nombre}.json"
        ruta_posting = f"./salida/posting_{nombre}.json"
        with open (ruta_dict, encoding="utf-8") as diccionario:
            data = dict(json.load(diccionario))
        try:
            term_id = int(data[termino])
            with open (ruta_posting, encoding="utf-8") as post:
                linea = ""
                for _ in range(term_id + 1):
                    linea = post.readline()
        except KeyError:
            print(f"No se encontro {termino}") 
            # No conviene levantar una nueva excepción ya que al no estar controlada finaliza la ejecución
        else:
            return eval(linea)

    def __obtener_tweet(self, tweetid : list) -> dict:
        ruta_dict = f"./salida/diccionario_tweets.json"
        ruta_posting = f"./salida/posting_tweets.json"
        with open (ruta_dict, encoding="utf-8") as diccionario:
            data = json.load(diccionario)
            try:
                pos = []
                aux = {}
                for t in tweetid:
                    for tw, posicion in data.items():
                        if int(tw) == int(t):
                            pos.append((posicion, tw))
                with open (ruta_posting, encoding = "utf-8") as post:
                    lineas = post.readlines()
                    for p, tw  in pos:
                        aux[tw] = lineas[int(p)]
            except KeyError:
                print("FATAL ERROR")
            else:
                return aux

    #tal vez no levantar excepciones pero pedir que reingrese un dato valido a menos que ya desde otro la
    #se validen las entradas y esta parte directamente hace y no pregunta
    def __validar_cantidad(self, cantidad : int):
        return cantidad > 0

    def __validar_fecha(self, fecha : str):
        if not self.__formato_fecha.match(fecha):
            raise FechaInvalidaException(f"{fecha} no es una fecha valida")

    def __validar_hora(self, hora : str):
        if not self.__formato_hora.match(hora):
            raise FechaInvalidaException(f"{hora} no es una hora valida")

from typing import List
from datetime import datetime
import json

class Buscador:

    def buscar_usuario(self, usuario: list) -> set:
        return self.__obtener_tweets(list(self.__obtener_lista_tweet_id("usuarios", usuario)))

    def buscar_palabra(self, palabra: list) -> set:
        return self.__obtener_tweets(list(self.__obtener_lista_tweet_id("palabras", palabra)))

    def buscar_frase(self, frase: str):
        conjunto = self.__obtener_lista_tweet_id("palabras", frase.split())
        if len(conjunto) == 0:
            return f"No existe un tweet con la frase: '{frase}'"
        else:
            return self.__obtener_tweets(list(conjunto))

    def buscar_fechas(self, fecha_inicial: datetime, fecha_final: datetime, cantidad: int, usuario: list) -> set:
        with open("./salida/diccionario_fechas.json", encoding="utf-8") as diccionario:
            data = dict(json.load(diccionario))
            rango_fechas = [fecha for fecha in data.keys() if self.__fecha_en_rango(fecha, fecha_inicial, fecha_final)]
            data = None
        resultados = self.__obtener_lista_tweet_id("fechas", rango_fechas)
        if len(usuario) > 0:
            resultados.intersection_update(self.__obtener_lista_tweet_id("usuarios", usuario))
        return self.__obtener_tweets(list(resultados)[0:cantidad])

    def __fecha_en_rango(self, fecha_a_evaluar: str, fecha_inical: datetime, fecha_final: datetime):
        fecha = datetime.strptime(fecha_a_evaluar, "%d/%m/%Y %H:%M")
        return fecha >= fecha_inical and fecha <= fecha_final

    def __obtener_lista_tweet_id(self, nombre: str, terminos: List[str]) -> set:
        return self.__buscar_indice(nombre, terminos)

    def __obtener_tweets(self, tweet_ids: list) -> dict:
        return self.__buscar_indice("tweets", tweet_ids)

    def __buscar_indice(self, nombre: str, terminos: List[str]) -> set:
        ruta_dict = f"./salida/diccionario_{nombre}.json"
        ruta_posting = f"./salida/posting_{nombre}.json"
        conjunto_resultados = set()
        lista_term_id = []
        with open(ruta_dict, encoding="utf-8") as diccionario, open(ruta_posting, encoding="utf-8") as post:
            data = dict(json.load(diccionario))
            for termino in terminos:
                if termino in data:
                    lista_term_id.append(int(data[termino]) + 1)
            lista_term_id.sort()
            indice = 0
            for term_id in lista_term_id:
                linea = ""
                for _ in range(indice, term_id):
                    linea = post.readline()
                conjunto_resultados = conjunto_resultados.union(eval(linea))
                indice = term_id
        return conjunto_resultados

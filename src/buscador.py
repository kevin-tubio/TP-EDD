from typing import List
import json

class Buscador:

    def buscar_usuario(self, usuario: list):
        return self.__obtener_tweets(self.__obtener_lista_tweet_id("usuarios", usuario))

    def buscar_palabra(self, palabra: list):
        return self.__obtener_tweets(self.__obtener_lista_tweet_id("palabras", palabra))

    def buscar_frase(self, frase: str):
        conjunto = self.__obtener_lista_tweet_id("palabras", frase.split())
        if len(conjunto) == 0:
            return f"No existe un tweet con la frase: '{frase}'"
        else:
            return self.__obtener_tweets(conjunto)

    def buscar_fechas(self, rango_fechas: List[str], cantidad: int, usuario: str):
        resultados = self.__obtener_lista_tweet_id("fechas", rango_fechas)
        if usuario != "":
            aux = self.__obtener_lista_tweet_id("usuarios", list(usuario))
            resultados.intersection_update(aux)
        if len(resultados) > cantidad:
            resultados[0:cantidad]
        return self.__obtener_tweets(resultados)

    def __obtener_lista_tweet_id(self, nombre: str, terminos: List[str]) -> set:
        return self.__buscar_indice(nombre, terminos)

    def __obtener_tweets(self, tweet_ids: set) -> dict:
        return self.__buscar_indice("tweets", list(tweet_ids))

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

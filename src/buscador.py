from typing import List
import json

class Buscador:

    def buscar_usuario(self, usuario: list):
        return self.__obtener_tweet(self.__obtener_lista_tweet_id("usuarios", usuario))

    def buscar_palabra(self, palabra: list):
        return self.__obtener_tweet(self.__obtener_lista_tweet_id("palabras", palabra))

    def buscar_frase(self, frase: str):
        conjunto = self.__obtener_lista_tweet_id("palabras", frase.split())
        if len(conjunto) == 0:
            return f"No existe un tweet con la frase: '{frase}'"
        else:
            return self.__obtener_tweet(conjunto)

    def buscar_fechas(self, rango_fechas: List[str], cantidad: int, usuario: str):
        resultados = self.__obtener_lista_tweet_id("fechas", rango_fechas)
        if usuario != "":
            aux = self.__obtener_lista_tweet_id("usuarios", list(usuario))
            resultados.intersection_update(aux)
        if len(resultados) > cantidad:
            resultados[0:cantidad]
        return self.__obtener_tweet(resultados)

    def __obtener_lista_tweet_id(self, nombre: str, terminos: List[str]) -> set:
        ruta_dict = f"./salida/diccionario_{nombre}.json"
        ruta_posting = f"./salida/posting_{nombre}.json"
        conjunto = set()
        with open(ruta_dict, encoding="utf-8") as diccionario, open(ruta_posting, encoding="utf-8") as post:
            data = dict(json.load(diccionario))
            for termino in terminos:
                if termino in data:
                    term_id = int(data[termino])
                    post.seek(0)
                    linea = ""
                    for _ in range(term_id + 1):
                        linea = post.readline()
                    conjunto = conjunto.union(eval(linea))
        return conjunto

    def __obtener_tweet(self, tweetid: set) -> dict:
        ruta_dict = f"./salida/diccionario_tweets.json"
        ruta_posting = f"./salida/posting_tweets.json"
        with open (ruta_dict, encoding="utf-8") as diccionario:
            data = dict(json.load(diccionario))
            try:
                pos = []
                aux = {}
                for t in tweetid:
                    for tw, posicion in data.items():
                        if int(tw) == int(t):
                            pos.append((posicion, tw))
                with open(ruta_posting, encoding ="utf-8") as post:
                    lineas = post.readlines()
                    for p, tw  in pos:
                        aux[tw] = lineas[int(p)]
            except KeyError:
                print("FATAL ERROR")
            else:
                return aux

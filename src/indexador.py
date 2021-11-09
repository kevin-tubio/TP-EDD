import csv
from typing import List
from nltk.corpus import stopwords
import os
from os import path
import re
import shutil
import json

class Indexador():

    def __init__(self, salida= "./salida", temp= "./temp", tweets_x_bloque=10000):
        self._temp = temp
        self._salida = salida
        self.__comprobar_directorio(self._salida)
        self.__comprobar_directorio(self._temp)
        self._tweets_x_bloque = tweets_x_bloque  
        self.__stop_words = frozenset(stopwords.words('spanish'))
        self.__stop_words_eng = frozenset(stopwords.words('english'))
        self._palabra_id = 0
        self._user_id = 0
        self._fecha_id = 0
        self._tweetid = 0
        self._palabra_to_palabra_id = {}
        self._user_to_user_id = {}
        self._fecha_to_fecha_id = {}
        self._tweetid_to_text = {}

    def indexar(self) -> None:
        self.__vaciar_directorios()
        nro_bloque = 0
        lista_bloques_palabras = []
        lista_bloques_usuarios = []
        lista_bloques_fechas = []
        lista_bloques_tweetid = []
        for bloque_palabra, bloque_usuario, bloque_fecha, bloque_tweetid in self.__parse_next_block():
            lista_bloques_palabras.append(self.__guardar_bloque_intermedio(self.__invertir_bloque(bloque_palabra), f"pal{nro_bloque}"))
            lista_bloques_usuarios.append(self.__guardar_bloque_intermedio(self.__invertir_bloque(bloque_usuario), f"usr{nro_bloque}"))
            lista_bloques_fechas.append(self.__guardar_bloque_intermedio(self.__invertir_bloque(bloque_fecha), f"fecha{nro_bloque}"))
            lista_bloques_tweetid.append(self.__guardar_bloque_intermedio(self.__invertir_bloque(bloque_tweetid), f"tweet{nro_bloque}"))
            nro_bloque += 1
        self.__intercalar_bloques(lista_bloques_palabras, self._palabra_to_palabra_id, "posting_palabras")
        self.__intercalar_bloques(lista_bloques_usuarios, self._user_to_user_id, "posting_usuarios")
        self.__intercalar_bloques(lista_bloques_fechas, self._fecha_to_fecha_id, "posting_fechas")
        self.__intercalar_bloques(lista_bloques_tweetid, self._tweetid_to_text, "posting_tweets")
        self.__guardar_diccionario(self._palabra_to_palabra_id, "diccionario_palabras")
        self.__guardar_diccionario(self._user_to_user_id, "diccionario_usuarios")
        self.__guardar_diccionario(self._fecha_to_fecha_id, "diccionario_fechas")
        self.__guardar_diccionario(self._tweetid_to_text, "diccionario_tweets")

    def __parse_next_block(self):
        tweets = self._tweets_x_bloque
        pares_palabra_tweet_id = []
        pares_usuario_tweet_id = []
        pares_fecha_tweet_id = []
        pares_tweetid_texto = []
        with open("fetched_tweets.csv", encoding="utf-8", newline='') as stream:
            lector = csv.DictReader(stream, delimiter=",")
            for linea in lector:
                tweets -= 1
                self.armar_lista_tweetid_texto(linea, pares_tweetid_texto)
                self.armar_lista_palabra_tweet_id(linea, pares_palabra_tweet_id)
                self.armar_lista_usuario_tweet_id(linea, pares_usuario_tweet_id)
                self.armar_lista_fecha_tweet_id(linea, pares_fecha_tweet_id)
                if tweets == 0:
                    yield [pares_palabra_tweet_id, pares_usuario_tweet_id, pares_fecha_tweet_id, pares_tweetid_texto]
                    tweets = self._tweets_x_bloque
                    pares_palabra_tweet_id = []
                    pares_usuario_tweet_id = []
                    pares_fecha_tweet_id = []
                    pares_tweetid_texto = []
        yield [pares_palabra_tweet_id, pares_usuario_tweet_id, pares_fecha_tweet_id, pares_tweetid_texto]

    def armar_lista_palabra_tweet_id(self, linea, lista_de_pares: list) -> None:
        id_tweet = linea['id']
        tweet = linea['text']
        for palabra in self.limpiar(tweet):
            palabra = palabra.lower()
            if self.validar(palabra):
                self._palabra_id = self.agregar_a_diccionario_terminos(palabra, self._palabra_id, self._palabra_to_palabra_id)
                lista_de_pares.append((self._palabra_to_palabra_id[palabra], id_tweet))

    def limpiar(self, tweet: str) -> List[str]:
        return re.split("(?:@[\w_]{5,15}|https://t.co/[\w]{10}|[^áÁéÉíÍóÓúÚñÑa-zA-Z@]+|@+)", tweet)

    def validar(self, palabra: str) -> bool:
        return len(palabra) > 1 and not (palabra in self.__stop_words or palabra in self.__stop_words_eng)

    def armar_lista_tweetid_texto(self, linea, lista_de_pares: list) -> None:
        id_tweet = linea['id']
        texto = linea['text']
        self._tweetid = self.agregar_a_diccionario_terminos(id_tweet, self._tweetid, self._tweetid_to_text)
        lista_de_pares.append((self._tweetid_to_text[id_tweet], texto))

    def armar_lista_usuario_tweet_id(self, linea, lista_de_pares: list) -> None:
        id_tweet = linea['id']
        usuario = linea['username']
        self._user_id = self.agregar_a_diccionario_terminos(usuario, self._user_id, self._user_to_user_id)
        lista_de_pares.append((self._user_to_user_id[usuario], id_tweet))

    def armar_lista_fecha_tweet_id(self, linea, lista_de_pares: list) -> None:
        id_tweet = linea['id']
        una_fecha = str(linea["fecha"]) + " " + str(linea["hora"])
        self._fecha_id = self.agregar_a_diccionario_terminos(una_fecha, self._fecha_id, self._fecha_to_fecha_id)
        lista_de_pares.append((self._fecha_to_fecha_id[una_fecha], id_tweet))

    def agregar_a_diccionario_terminos(self, termino: str, term_id: int, diccionario: dict) -> int:
        if termino not in diccionario:
            diccionario[termino] = term_id
            term_id += 1
        return term_id

    def __invertir_bloque(self, bloque: list) -> dict:
        bloque_invertido={}
        bloque_ordenado = sorted(bloque, key = lambda tupla: (tupla[0], tupla[1]))
        for par in bloque_ordenado:
            self.agregar_al_diccionario(str(par[0]), str(par[1]), bloque_invertido)
        return bloque_invertido

    def __guardar_bloque_intermedio(self, bloque: dict, nombre_bloque: str) -> str:
        archivo_salida = f"bloque_{nombre_bloque}.json"
        archivo_salida = self.__join(self._temp, archivo_salida)
        for clave in bloque:
            bloque[clave] = list(bloque[clave])
        with open(archivo_salida, mode="w", encoding="utf-8") as contenedor:
            json.dump(bloque, contenedor, ensure_ascii=False)
        return archivo_salida

    def __obtener_lista_termino_id(self, diccionario: dict):
        cantidad_total = len(diccionario)
        cantidad = 0
        bloque = 5000
        while cantidad < (cantidad_total - bloque):
            yield [str(i) for i in range(cantidad, cantidad + bloque)]
            cantidad += bloque
        yield [str(i) for i in range(cantidad, cantidad_total)]

    def __intercalar_bloques(self, temp_files: list, dic_term_to_term_id: dict, nombre: str) -> None:
        posting_file = self.__join(self._salida, f"{nombre}.json")
        open_files = [open(f, encoding="utf-8") for f in temp_files]

        with open(posting_file, mode="w", encoding="utf-8") as salida:
            for segmento in self.__obtener_lista_termino_id(dic_term_to_term_id):
                diccionario = {}
                for data in open_files:
                    data.seek(0)
                    bloque = json.load(data)
                    for term_id in segmento:
                        lista_tweets_id = bloque.get(term_id)
                        if lista_tweets_id is None:
                            continue
                        posting = diccionario.setdefault(term_id, set())
                        diccionario[term_id] = posting.union(set(lista_tweets_id))
                for valor in diccionario.values():
                    json.dump(list(valor), salida, ensure_ascii=False)
                    salida.write("\n")

    def __guardar_diccionario(self, diccionario: dict, nombre: str) -> None:
        path = self.__join(self._salida, f"{nombre}.json")
        with open(path, mode="w", encoding="utf-8") as contenedor:
            json.dump(diccionario, contenedor, ensure_ascii=False)

    def unir_csvs(self, ruta_documentos: str) -> None:
        lista_documentos = [self.__join(ruta_documentos, nombre_doc) \
                        for nombre_doc in os.listdir(ruta_documentos) \
                        if os.path.isfile(self.__join(ruta_documentos, nombre_doc))]

        primer_documento = self.__join(ruta_documentos, "unificado.csv")
        os.rename(lista_documentos.pop(), primer_documento)
        with open(primer_documento, mode="w", encoding="utf-8") as unificado:
            for documento in lista_documentos:
                with open(documento, encoding="utf-8") as doc:
                    doc.readline()
                    shutil.copyfileobj(doc, unificado)

    def agregar_al_diccionario(self, termino: str, id_tweet: str, bloque_invertido: dict) -> None:
        posting = bloque_invertido.setdefault(termino, set())
        posting.add(id_tweet)

    def __comprobar_directorio(self, directorio: str) -> None:
        if not path.isdir(directorio):
            os.mkdir(directorio)

    def __vaciar_directorios(self) -> None:
        directorio = self._temp
        for f in os.listdir(directorio):
            os.remove(self.__join(directorio, f))

        directorio = self._salida
        for f in os.listdir(directorio):
            os.remove(self.__join(directorio, f))

    def __join(self, root: str, ruta: str) -> str:
        return os.path.join(root, ruta)

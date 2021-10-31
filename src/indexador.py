import csv
from datetime import datetime
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import os
import re
import shutil
import json

class Indexador():

    def __init__(self, salida, temp="./temp", tweets_x_bloque=10000):
        self._tweets_x_bloque = tweets_x_bloque
        self._temp = temp
        self._salida = salida
        self.__stop_words = frozenset(stopwords.words('spanish'))
        self.__stop_words_eng = frozenset(stopwords.words('english'))
        self.__spanish_stemmer = SnowballStemmer('spanish', ignore_stopwords=False)
        self._palabra_to_palabra_id = {}
        self._user_to_user_id = {}

    def indexar(self):
        nro_bloque = 0
        lista_bloques_palabras = []
        lista_bloques_usuarios = []
        lista_bloques_fechas = []
        for bloque_palabra, bloque_usuario, bloque_fecha in self.__parse_next_block():
            lista_bloques_palabras.append(self.__guardar_bloque_intermedio(self.__invertir_bloque(bloque_palabra), f"pal{nro_bloque}"))
            lista_bloques_usuarios.append(self.__guardar_bloque_intermedio(self.__invertir_bloque(bloque_usuario), f"usr{nro_bloque}"))
            nro_bloque += 1
        self.__intercalar_bloques(lista_bloques_palabras, self._palabra_to_palabra_id, "posting_palabras")
        self.__intercalar_bloques(lista_bloques_usuarios, self._user_to_user_id, "posting_usuarios")
        self.__guardar_diccionario(self._palabra_to_palabra_id, "diccionario_palabras")
        self.__guardar_diccionario(self._user_to_user_id, "diccionario_usuarios")

    def __parse_next_block(self):
        tweets = self._tweets_x_bloque
        self._palabra_id = 0
        pares_palabra_tweet_id = []
        pares_usuario_tweet_id = []
        pares_fecha_tweet_id = []
        with open("fetched_tweets.csv", encoding="utf-8", newline='') as stream:
            lector = csv.DictReader(stream, delimiter=",")
            for linea in lector:
                tweets -= 1
                self.armar_lista_palabra_tweet_id(linea, pares_palabra_tweet_id)
                self.armar_lista_usuario_tweet_id(linea, pares_usuario_tweet_id)

                if tweets == 0:
                    yield [pares_palabra_tweet_id, pares_usuario_tweet_id, pares_fecha_tweet_id]
                    tweets = self._tweets_x_bloque
                    pares_palabra_tweet_id = []
                    pares_usuario_tweet_id = []
                    pares_fecha_tweet_id = []
        yield [pares_palabra_tweet_id, pares_usuario_tweet_id, pares_fecha_tweet_id]

    def armar_lista_palabra_tweet_id(self, linea, lista_de_pares : list):
        id_tweet = linea['id']
        tweet = linea['text']
        for palabra in self.limpiar(tweet):
            if self.validar(palabra):
                self.agregar_a_diccionario_terminos(palabra.lower(), self._palabra_id, self._palabra_to_palabra_id)
                self._palabra_id += 1
                lista_de_pares.append((self._palabra_to_palabra_id[palabra], id_tweet))

    def limpiar(self, tweet):
        return re.split("(?:@[\w_]{5,15}|https://t.co/[\w]{10}|[^áÁéÉíÍóÓúÚñÑa-zA-Z@]+|@+)", tweet)

    def validar(self, palabra):
        return len(palabra) > 1 and not (palabra in self.__stop_words or palabra in self.__stop_words_eng)

    def armar_lista_usuario_tweet_id(self, linea, lista_de_pares : list):
        id_tweet = linea['id']
        usuario = linea['username']
        user_id = linea['author_id']
        self.agregar_a_diccionario_terminos(usuario, int(user_id), self._user_to_user_id)
        lista_de_pares.append((self._user_to_user_id[usuario], id_tweet))

    def agregar_a_diccionario_terminos(self, termino, term_id : int, diccionario : dict):
        if termino not in diccionario:
            diccionario[termino] = term_id

    def __invertir_bloque(self, bloque):
        bloque_invertido={}
        bloque_ordenado = sorted(bloque, key = lambda tupla: (tupla[0], tupla[1]))
        for par in bloque_ordenado:
            self.agregar_al_diccionario(str(par[0]), str(par[1]), bloque_invertido)
        return bloque_invertido

    def __guardar_bloque_intermedio(self, bloque, nombre_bloque):
        archivo_salida = f"bloque_{nombre_bloque}.json"
        archivo_salida = os.path.join(self._temp, archivo_salida)
        for clave in bloque:
            bloque[clave]=list(bloque[clave])
        with open(archivo_salida, "w") as contenedor:
            json.dump(bloque, contenedor)
        return archivo_salida

    def __intercalar_bloques(self, temp_files, dic_term_to_term_id, nombre):
        lista_term_id=[str(i) for i in range(len(dic_term_to_term_id))]
        posting_file = os.path.join(self._salida, f"{nombre}.json")

        open_files = [open(f, "r") for f in temp_files]

        with open(posting_file,"w") as salida:
            for term_id in lista_term_id:
                posting=set()
                #for f in temp_files:
                    #with open(f, "r") as data:
                for data in open_files:
                    data.seek(0)
                    bloque = json.load(data)
                    try:
                        posting = posting.union(set(bloque[term_id]))
                    except Exception:
                        pass
                json.dump(list(posting), salida)

    def __guardar_diccionario(self, diccionario, nombre):
        path = os.path.join(self._salida, f"{nombre}.json")
        with open(path, "w") as contenedor:
            json.dump(diccionario, contenedor)

    def unir_csvs(self, ruta_documentos):
        lista_documentos = [os.path.join(ruta_documentos, nombre_doc) \
                        for nombre_doc in os.listdir(ruta_documentos) \
                        if os.path.isfile(os.path.join(ruta_documentos, nombre_doc))]

        primer_documento = os.path.join(ruta_documentos, "unificado.csv")
        os.rename(lista_documentos.pop(), primer_documento)
        with open(primer_documento, "a") as unificado:
            for documento in lista_documentos:
                with open(documento) as doc:
                    doc.readline()
                    shutil.copyfileobj(doc, unificado)

    def agregar_al_diccionario(self, palabra : str, id_tweet : str, bloque_invertido : dict):
        posting = bloque_invertido.setdefault(palabra, set())
        posting.add(id_tweet)


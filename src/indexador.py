import csv
import datetime
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import os
import re
import shutil

class Indexador():

    def __init__(self, tweets_x_bloque=10000):
        self._tweets_x_bloque = tweets_x_bloque
        self.__stop_words = frozenset(stopwords.words('spanish'))
        self.__stop_words_eng = frozenset(stopwords.words('english'))
        self.__spanish_stemmer = SnowballStemmer('spanish', ignore_stopwords=False)
        self.__campos = ["fecha", "hora", "id", "username", "author_id", "text"]
        self._palabra_to_palabra_id = {}
        self._user_to_user_id = {}

    def indexar(self):
        nro_bloque = 0
        lista_bloques_palabras = []
        lista_bloques_usuarios = []
        lista_bloques_fechas = []
        for bloque_palabra, bloque_usuario, bloque_fecha in self.__parse_next_block():
            pass

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

    #Estos dos métodos se generalizaron, ahora se le pasa el diccionario al cual se agregan las palabras y el que se invierte
    def agregar_al_diccionario(self, palabra : str, id_tweet : str, diccio : dict):
        posting = diccio.setdefault(palabra, set())
        posting.add(id_tweet)

    def invertir_diccionario(self, diccio : dict(), invertido : dict()):
        for palabra, ids in diccio.items():
            for id in ids:
                self.invertido.setdefault(id, set())
                self.invertido[id].add(palabra)

import csv
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re
import string

class Indexador():

    def __init__(self, archivo : csv) -> None:
        self.__stop_words = frozenset(stopwords.words('spanish'))
        self.__spanish_stemmer = SnowballStemmer('spanish', ignore_stopwords=False)
        self.__puntuaciones = self.__obtener_puntuaciones()

    def armar_indices(self, archivo):
        #falta recuperar directamente el path con sys
        with open(archivo, "r", encoding="utf-8") as lector_csv:
            lector = csv.DictReader(archivo, delimiter=",")
            self.__indice_id_tweet = {}
            self.__indice_palabra_id = {}
            self.__indice_id_usuario = {}
            self.__indice_fecha_id = {}
            self.__indice_frase_id = {}
            for linea in lector:
                #falta postin y faltan pares para evitar colisiones
                fecha, hora, id_tweet, nombre_usuario, tweet = linea["fecha"], linea["hora"], linea["id"], linea["username"], linea["text"]
                lista_frases = [self.__limpiar(frase) for frase in tweet.split(".")]
                lista_palabras = [self.__lematizar(palabra) for palabra in tweet.split() if len(palabra) > 3 and not palabra in self.__stop_words]
                for frase in lista_frases:
                    self.__indice_frase_id[frase] = id_tweet
                for palabra in lista_palabras:
                    self.__indice_palabra_id[palabra] = id_tweet
                self.__indice_id_usuario[id_tweet] = nombre_usuario
                self.__indice_id_tweet[id_tweet] = tweet
                #self.__indice_fecha_id 

    def __limpiar(self, frase : str):
        frase = self.__quitar_hashtag(frase)
        frase = self.__sacar_puntuaciones(frase)
        return frase

    def __quitar_hashtag(self, palabra : str):
        return palabra.replace("#", "")

    def __sacar_puntuaciones(self, palabra : str):
        return palabra.strip(self.__puntuaciones)

    def __lematizar(self, palabra):
        palabra = self.__quitar_hashtag(palabra)
        palabra = self.__sacar_puntuaciones(palabra)
        palabra = self.__spanish_stemmer.stem(palabra)
        return palabra

    def __obtener_puntuaciones(self):
        puntuaciones = string.punctuation
        for valor in range(128, 256):
            puntuaciones += chr(valor)
        return puntuaciones

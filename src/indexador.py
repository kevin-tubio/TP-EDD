import csv
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import os
import re
import string

class Indexador():

    def __init__(self) -> None:
        self.__stop_words = frozenset(stopwords.words('spanish'))
        self.__spanish_stemmer = SnowballStemmer('spanish', ignore_stopwords=False)
        self.__puntuaciones = self.__obtener_puntuaciones()

    def armar_indices(self):
        nombre_archivo = os.path.abspath("fetched_tweets.csv")
        print(nombre_archivo)
        with open(nombre_archivo, "r", encoding="utf-8") as lector_csv:
            lector = csv.DictReader(lector_csv, delimiter=",")
            self.__indice_id_tweet = {}
            self.__indice_palabra_id = {}
            self.__indice_id_usuario = {}
            self.__indice_fecha_id = {}
            self.__indice_frase_id = {}
            pares_id_tweet = []
            pares_palabra_id = []
            pares_id_usuario = []
            pares_frase_id = []
            pares_fecha_id = []
            for linea in lector:
                # se podria hacer split(".") si tomamos como . el separador de frase, y despues split() con esa frase para las palabras?
                #[palabra for palabras in lista_frases for palabra in palabras.split()]
                #al usar esta lista hay que ver el tema del lematizado
                #falta postin y faltan pares
                fecha, hora, id_tweet, nombre_usuario, tweet = linea["fecha"], linea["hora"], linea["id"], linea["username"], linea["text"]
                lista_frases = [self.__limpiar(frase) for frase in tweet.split(".")]
                lista_palabras = [self.__lematizar(palabra) for palabras in lista_frases for palabra in palabras.split() if len(palabra) > 3 and not palabra in self.__stop_words]
                pares_frase_id = pares_frase_id + [(frase, id_tweet) for frase in lista_frases]
                pares_palabra_id = pares_palabra_id + [(palabra, id_tweet) for palabra in lista_palabras]
                pares_id_usuario = pares_id_usuario + (id_tweet, nombre_usuario)
                pares_id_tweet = pares_id_tweet + (id_tweet, tweet)
                
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
        palabra = self.__spanish_stemmer.stem(palabra)
        return palabra

    def __obtener_puntuaciones(self):
        puntuaciones = string.punctuation
        for valor in range(128, 256):
            puntuaciones += chr(valor)
        return puntuaciones
if __name__=="__main__":
    a = Indexador()
    a.armar_indices()

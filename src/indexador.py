import csv
import datetime
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import os
import re
import string

class Indexador():

    def __init__(self) -> None:
        self.__stop_words = frozenset(stopwords.words('spanish'))
        self.__spanish_stemmer = SnowballStemmer('spanish', ignore_stopwords=False)

    def armar_indices(self):
        nombre_archivo = os.path.abspath("fetched_tweets.csv")
        with open(nombre_archivo, "r", encoding="utf-8") as lector_csv:
            lector = csv.DictReader(lector_csv, delimiter=",")
            indice_id_tweet = {}
            indice_palabra_id = {}
            indice_id_usuario = {}
            indice_fecha_id = {}
            indice_frase_id = {}
            pares_id_tweet = []
            pares_palabra_id = []
            pares_id_usuario = []
            pares_frase_id = []
            pares_fecha_id = []

            for linea in lector:
                fecha, hora, id_tweet, nombre_usuario, tweet = linea["fecha"], linea["hora"], linea["id"], linea["username"], linea["text"]
                lista_frases = self.__obtener_lista_de_frases(tweet)
                lista_palabras = [self.__lematizar(palabra) for palabra in re.split("\W", str(lista_frases)) if self.__es_palabra_valida(palabra)]

                pares_frase_id += [(frase, id_tweet) for frase in lista_frases]
                pares_palabra_id += [(palabra, id_tweet) for palabra in lista_palabras]
                pares_id_usuario += (id_tweet, nombre_usuario)
                pares_id_tweet += (id_tweet, tweet)
                pares_fecha_id += (datetime.datetime.strptime(f"{fecha} {hora}", "%d/%m/%Y %H:%M"), id_tweet)

            self.__indice_frase_id = self.__ordenar_valores(self.__ordenar_claves(self.__generar(pares_frase_id, indice_frase_id)))
            self.__indice_palabra_id = self.__ordenar_valores(self.__ordenar_claves(self.__generar(pares_palabra_id, indice_palabra_id)))
            self.__indice_id_usuario = self.__ordenar_valores(self.__ordenar_claves(self.__generar(pares_id_usuario, indice_id_usuario)))
            self.__indice_id_tweet = self.__ordenar_valores(self.__ordenar_claves(self.__generar(pares_id_tweet, indice_id_tweet)))
            self.__indice_fecha_id = self.__ordenar_valores(self.__ordenar_claves(self.__generar(pares_fecha_id, indice_fecha_id)))

    def __es_palabra_valida(self, palabra) -> bool:
        return len(palabra) > 1 and palabra not in self.__stop_words

    def __generar(self, lista_pares : list, dict_indice : dict):
        for par in lista_pares:
            #devuelve el valor de esa key, sino tiene valor, le crea
            posting = dict_indice.setdefault(par[0],set()) 
            posting.add(par[1])
        return dict_indice

    def __ordenar_valores(self, diccionario : dict):
        otro_diccionario = {}
        for clave, valor in diccionario.items():
            otro_diccionario[clave] = tuple(sorted(list(valor)))
        return otro_diccionario

    def __ordenar_claves(self, diccionario : dict):
        return dict(sorted(diccionario.items()))

    def __obtener_lista_de_frases(self, tweet):
        lista_de_frases = [self.__limpiar(frase) for frase in tweet.split(".") if re.split("\W", frase)]
        return [frase for frase in lista_de_frases if frase != ""]

    def __limpiar(self, frase):
        aux = ""
        for palabra in re.split("\W", frase):
            if palabra != "":
                aux += (palabra + " ")
        return aux[:-1]

    def __lematizar(self, palabra):
        palabra = self.__spanish_stemmer.stem(palabra)
        return palabra

    def print_indices(self):
        print(self.__indice_fecha_id)
        print(self.__indice_frase_id)
        print(self.__indice_id_tweet)
        print(self.__indice_id_usuario)
        print(self.__indice_palabra_id)

if __name__=="__main__":
    a = Indexador()
    a.armar_indices()
    a.print_indices()

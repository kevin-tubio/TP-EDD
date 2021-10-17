import csv
import datetime
import shelve
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
            n = 0
            for linea in lector:
                fecha, hora, id_tweet, nombre_usuario, tweet = linea["fecha"], linea["hora"], linea["id"], linea["username"], linea["text"]
                lista_frases = self.__obtener_lista_de_frases(tweet)
                lista_palabras = [self.__lematizar(palabra) for palabra in re.split("\W", str(lista_frases)) if self.__es_palabra_valida(palabra)]

                pares_frase_id += [(frase, id_tweet) for frase in lista_frases]
                pares_palabra_id += [(palabra, id_tweet) for palabra in lista_palabras]
                pares_id_usuario += [(id_tweet, nombre_usuario)]
                pares_id_tweet += [(id_tweet, tweet)]
                pares_fecha_id += [(datetime.datetime.strptime(f"{fecha} {hora}", "%d/%m/%Y %H:%M"), id_tweet)]

                n += 1
                if n == 100:
                    self.__indice_frase_id = self.__ordenar_valores(self.__ordenar_claves(self.__generar(pares_frase_id, indice_frase_id)))
                    self.__indice_palabra_id = self.__ordenar_valores(self.__ordenar_claves(self.__generar(pares_palabra_id, indice_palabra_id)))
                    self.__indice_id_usuario = self.__ordenar_valores(self.__ordenar_claves(self.__generar(pares_id_usuario, indice_id_usuario)))
                    self.__indice_id_tweet = self.__ordenar_valores(self.__ordenar_claves(self.__generar(pares_id_tweet, indice_id_tweet)))
                    self.__indice_fecha_id = self.__ordenar_valores(self.__ordenar_claves(self.__generar(pares_fecha_id, indice_fecha_id)))
                    self.__persistir(indice_frase_id)
                    self.__persistir(indice_palabra_id)
                    self.__persistir(indice_id_usuario)
                    self.__persistir(indice_id_tweet)
                    self.__persistir(indice_fecha_id) #este podria llamar al metodo para fragmentar y unir y ordenar k,v
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
                    n = 0
                    """
                    with open("file.csv") as file:
                        for line in file:
                            pass
                        print(line) #encuentra la ultima linea lastima que lee todo pero se puede usar para cortar el n
                    """

    def __persistir(self, indice : dict):
        archivos = set()
        for clave, valor in indice:
            archivos.add(clave[0])
            #a con a, b con b, mejorar
            with shelve.open(clave[0]) as shelve_bd:
                #que pasa si esa clave ya tiene un valor?
                posting = shelve_bd.setdefault(clave, set())
                #tenga o no set
                #si tiene actualiza el set con
                posting.union(valor) #valor puede ser 1 o n, no puedo hacer p.add
                #pisa ese valor, los sorted se pueden dejar para cuando termina el csv, si o si hay que hacer 2
                shelve_bd[clave] = sorted(posting) #deja los valores que toco ordenados
        archivos = sorted(archivos) # este creo que no hace falta
        self.__ordenar_archivos_fragmentados(archivos)
#esto se podria hacer una sola vez cuando termine el csv!!!
    def __ordenar_archivos_fragmentados(self, archivos : set):#este podria ser un global que ordene todos los archivos
        #falta ordenar las keys porque los values estan ordendos
        for archivo in archivos:#en vez de hacer para los que agrega cada vez se podria hacer una sola vez al final!!!
            with shelve.open(archivo) as lector:
                lista_clave_valor = sorted(list(lector.items())) #ordena
                lector.clear() #elimina todas las keys
                for clave, valor in lista_clave_valor: #iterar y pastear keys
                    lector[clave] = valor

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
            otro_diccionario[clave] = sorted(valor) #sorted ordena tuplas
        return otro_diccionario

    def __ordenar_claves(self, diccionario : dict):
        return dict(sorted(diccionario.items()))

    def __obtener_lista_de_frases(self, tweet):
        lista_de_frases = [self.__limpiar(frase) for frase in re.split("[.\n]", tweet)]
        return [frase for frase in lista_de_frases if len(frase) > 1]

    def __limpiar(self, frase):
        aux = ""
        for palabra in re.split("(?:[^áéíóúña-zA-Z@]+|@[áéíóúña-zA-Z_]+)", frase):
            if palabra != "":
                aux += (palabra + " ")
        return aux[:-1]

    def __lematizar(self, palabra):
        palabra = self.__spanish_stemmer.stem(palabra)
        return palabra

    def lematizar(self, palabra):
        palabra = self.__spanish_stemmer.stem(palabra)
        return palabra
    #se puede volar
    def obtener_indice(self):
        # return self.__indice_fecha_id
        # return self.__indice_frase_id
        # return self.__indice_id_tweet
        # return self.__indice_id_usuario
        #print(self.__indice_palabra_id)
        return self.__indice_palabra_id
#tambien se vuela
if __name__=="__main__":
    a = Indexador()
    a.armar_indices()

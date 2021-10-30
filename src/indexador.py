import csv
import datetime
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import os
import re
import fileinput

class Indexador():

    def __init__(self, tamanio_bloque=102400):
        self.__tamanio_bloque = tamanio_bloque
        self.__stop_words = frozenset(stopwords.words('spanish'))
        self.__stop_words_eng = frozenset(stopwords.words('english'))
        self.__spanish_stemmer = SnowballStemmer('spanish', ignore_stopwords=False)
        self.__campos = ["fecha", "hora", "id", "username", "author_id", "text"]
        self.id_tweet_palabra = {}
        self.palabra_id_tweet = {}

    #Para mi hay que cambiarlo a un fileinput.input como en el metodo parse_next_block del profe
    def armar_indices(self):
        nombre_archivo = os.path.abspath("fetched_tweets.csv")
        with open(nombre_archivo, "r", encoding="utf-8") as lector_csv:
            lector = csv.DictReader(lector_csv, delimiter=",")
            #fecha y hora, id tweet -> id tweet, tweet; viceversa?
            #palabra, id tweet -> id tweet, tweet; viceversa?
            #frase, id tweet -> id tweet, tweet; viceversa?
            #autor id, id tweet -> id tweet, tweet? opcionales
            #nombre, id tweet -> id tweet, tweet? opcionales
            #autor id, nombre -> nombre, autor id? opcionales
            tamanio_bloque = self.__tamanio_bloque
            lista_bloques = []
            id_frase = 0
            id_palabra = 0
            cantidad_de_tweets = 100
            indice_palabra_a_id_palabra = {}
            indice_frase_a_id_frase = {}
            indice_fecha_hora_a_id_fecha_hora = {}

            for linea in lector:
                tamanio_bloque -= len(linea.encode("utf-8"))
                fecha, hora, id_tweet, nombre_usuario, tweet, autor_id = linea["fecha"], linea["hora"], linea["id"],linea["username"], linea["text"], linea["author_id"]
                lista_frases = self.__obtener_lista_de_frases(tweet)
                lista_palabras = [palabra for palabra in re.split("\W", str(lista_frases)) if self.__es_palabra_valida(palabra)]
                for frase in lista_frases:
                    if not indice_frase_a_id_frase.get(frase):
                        indice_frase_a_id_frase[frase] = id_frase
                        id_frase +=1
                for palabra in lista_palabras:
                    if not indice_palabra_a_id_palabra.get(palabra):
                        indice_frase_a_id_frase[palabra] = id_palabra
                        id_palabra += 1
                indice_fecha_hora_a_id_fecha_hora[datetime.datetime.strptime(f"{fecha} {hora}", "%d/%m/%Y %H:%M")] = id
                if tamanio_bloque <=0:
                        yield lista_bloques
                        tamanio_bloque = self.__tamanio_bloque
                        lista_bloques = []
            yield lista_bloques
            #invertir_indices()
            indice_invertido_palabra_a_id_palabra = {(valor, clave) for clave, valor in indice_palabra_a_id_palabra.items()}

    def armar_diccionarios(self, linea, nombreDoc):
        #Diccio palabra_id_tweet y tweet_id_palabra
        id_tweet = linea['id']
        tweet = linea['text']
        #imagino que esto deja solo las letras, lower para que no meta dos veces lo mismo  -- Correcto
        palabras = self.limpiar(tweet).lower()
        #deja al twit limpio, supongo, entonces agarro palabra por palabra
        for palabra in palabras.split():
            if self.validar(palabra):
                self.agregar_al_diccionario(palabra, id_tweet, self.palabra_id_tweet )
        self.invertir_diccionario(self.palabra_id_tweet, self.id_tweet_palabra)
    
    
    ##Arroja keyerror pero guarda bien los tweets en el archivo. Debe ser que el stream devuelve una linea vacía al final
    def unir_csvs(self, ruta_documentos):
        lista_documentos = [os.path.join(ruta_documentos, nombre_doc) \
                        for nombre_doc in os.listdir(ruta_documentos) \
                        if os.path.isfile(os.path.join(ruta_documentos, nombre_doc))]

        aux = []
        with open("unificado.csv", "a") as uni:
            writer = csv.DictWriter(uni, fieldnames=self.__campos, delimiter=",")
            writer.writeheader()
            for documento in lista_documentos:
                with open(documento, "r") as doc:
                    stream = csv.DictReader(doc, delimiter=",")
                    for linea in sorted(stream, key=lambda x: x["id"]):
                        if linea['id'] not in aux:
                            writer.writerow(linea)
                            aux.append(linea['id'])

    def limpiar(self, tweet):
        aux = ""
        for palabra in re.split("(?:@[\w_]{5,15}|https://t.co/[\w]{10}|[^áÁéÉíÍóÓúÚñÑa-zA-Z@]+|@+)", tweet):
            if palabra != "":
                aux += (palabra + " ")
        return aux[0:-1]

    def validar(self, palabra):
        #que pasa con las palabras en otros idiomas?
        return len(palabra) > 1 and palabra not in self.__stop_words and palabra not in self.__stop_words_eng

    #Estos dos métodos se generalizaron, ahora se le pasa el diccionario al cual se agregan las palabras y el que se invierte
    def agregar_al_diccionario(self, palabra : str, id_tweet : str, diccio : dict):
        posting = diccio.setdefault(palabra, set())
        posting.add(id_tweet)

    def invertir_diccionario(self, diccio : dict(), invertido : dict()):
        for palabra, ids in diccio.items():
            for id in ids:
                self.invertido.setdefault(id, set())
                self.invertido[id].add(palabra)


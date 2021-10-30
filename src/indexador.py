import csv
import datetime
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import os
import re
import json
import fileinput
import string
import time

class Indexador():

    def __init__(self, tamaño_bloque=102400):
        self.__tamaño_bloque = tamaño_bloque
        self.__stop_words = frozenset(stopwords.words('spanish'))
        self.__stop_words_eng = frozenset(stopwords.words('english'))
        self.__spanish_stemmer = SnowballStemmer('spanish', ignore_stopwords=False)

        self.id_tweet_palabra = {}
        self.palabra_id_tweet = {}
       #self.armar_indices

    
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
            tamaño_bloque = self.__tamaño_bloque
            lista_bloques = []
            id_frase = 0
            id_palabra = 0
            cantidad_de_tweets = 100
            indice_palabra_a_id_palabra = {}
            indice_frase_a_id_frase = {}
            indice_fecha_hora_a_id_fecha_hora = {}

            for linea in lector:
                tamaño_bloque -= len(linea.encode("utf-8"))
                fecha, hora, id_tweet, nombre_usuario, tweet, autor_id = linea["fecha"], linea["hora"], linea["id"], linea["username"], linea["text"], linea["author_id"]
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
                if tamaño_bloque <=0:
                        yield lista_bloques
                        tamaño_bloque = self.__tamaño_bloque
                        lista_bloques = []
            yield lista_bloques
            #invertir_indices()
            indice_invertido_palabra_a_id_palabra = {(valor, clave) for clave, valor in indice_palabra_a_id_palabra.items()}

    def parse_next_block(self):
        n = self._blocksize #espacio libre en el bloque actual
        termID = 0 #inicializamos el diccionario de términos
        bloque = [] #lista de pares (termID, docID)
        with fileinput.input(self._lista_documentos) as stream:
            for linea in stream:
                n -= len(linea.encode('utf-8'))
                palabras = linea.split()
                doc = fileinput.filename()
                for pal in palabras:
                    if pal not in self._stop_words:
                        pal = self.__lematizar(pal)
                        if pal not in self._term_to_termID:
                            self._term_to_termID[pal] = termID
                            termID += 1
                        bloque.append((self._term_to_termID[pal], self._doc_to_docID[doc]))
                if n <=0:
                    yield bloque
                    n = self._blocksize
                    bloque = []
        yield bloque

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
        
        
    def limpiar(self, tweet):
        aux = ""
        for palabra in re.split("(?:[^áéíóúña-zA-Z@]+|@[áéíóúña-zA-Z_]+)", tweet):
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


class II_BSBI:
    def __init__(self, documentos, salida, temp="./temp", blocksize=102400, language='spanish'):
        ''' documentos: carpeta con archivos a indexar
            salida: carpeta donde se guardará el índice invertido'''
        self.documentos = documentos
        self.salida = salida
        self._blocksize = blocksize
        self._temp = temp
        self._stop_words = frozenset(stopwords.words(language))  # lista de stop words
        self._stemmer = SnowballStemmer(language, ignore_stopwords=False)
        self._term_to_termID = {}

        self.__generar_docID()
        self.__indexar()

    def __generar_docID(self):
        doc_to_docID = {}
        docID_to_doc = {}
        lista_documentos = [os.path.join(self.documentos, nombre_doc) \
                            for nombre_doc in os.listdir(self.documentos) \
                            if os.path.isfile(os.path.join(self.documentos, nombre_doc))]

        for i in range(len(lista_documentos)):
            doc_to_docID[lista_documentos[i]] = i
        self._lista_documentos = lista_documentos
        self._doc_to_docID = doc_to_docID

    def __lematizar(self, palabra):
        ''' Usa el stemmer para lematizar o recortar la palabra, previamente elimina todos
        los signos de puntuación que pueden aparecer. El stemmer utilizado también se
        encarga de eliminar acentos y pasar todo a minúscula, sino habría que hacerlo
        a mano'''

        #palabra = palabra.decode("utf-8", ignore).encode("utf-8")
        palabra = palabra.strip(string.punctuation + "»" + "\x97" + "¿" + "¡" + "\u201c" +\
                               "\u201d" + "\u2014" + "\u2014l" + "\u00bf")
        # "\x97" representa un guión

        palabra_lematizada = self._stemmer.stem(palabra)
        return palabra_lematizada

    def __indexar(self):
        n = 0
        lista_bloques = []
        for bloque in self.__parse_next_block():
            bloque_invertido = self.__invertir_bloque(bloque)
            lista_bloques.append(self.__guardar_bloque_intermedio(bloque_invertido, n))
            n += 1
        start = time.process_time()
        self.__intercalar_bloques(lista_bloques)
        end = time.process_time()
        print("Intercalar Bloques Elapsed time: ", end-start)

        self.__guardar_diccionario_terminos()
        self.__guardar_diccionario_documentos()

    def __invertir_bloque(self, bloque):
        bloque_invertido={}
        bloque_ordenado = sorted(bloque,key = lambda tupla: (tupla[0], tupla[1]))
        for par in bloque_ordenado:
            posting = bloque_invertido.setdefault(par[0],set())
            posting.add(par[1]) 
        return bloque_invertido

    def __guardar_bloque_intermedio(self, bloque, nro_bloque):
        archivo_salida = "b"+str(nro_bloque)+".json"
        archivo_salida = os.path.join(self._temp, archivo_salida)
        for clave in bloque:
            bloque[clave]=list(bloque[clave])
        with open(archivo_salida, "w") as contenedor:
            json.dump(bloque, contenedor)
        return archivo_salida

    def __intercalar_bloques(self, temp_files):
        
        lista_termID=[str(i) for i in range(len(self._term_to_termID))]
        posting_file = os.path.join(self.salida,"postings.json")

        open_files = [open(f, "r") for f in temp_files]

        with open(posting_file,"w") as salida:
            for termID in lista_termID:
                posting=set()
                #for f in temp_files:
                    #with open(f, "r") as data:
                for data in open_files:
                    data.seek(0)
                    bloque = json.load(data)
                    try:
                        posting = posting.union(set(bloque[termID]))
                    except:
                        pass
                json.dump(list(posting), salida)

    def __guardar_diccionario_terminos(self):
        path = os.path.join(self.salida, "diccionario_terminos.json")
        with open(path, "w") as contenedor:
            json.dump(self._term_to_termID, contenedor)

    def __guardar_diccionario_documentos(self):
        path = os.path.join(self.salida, "diccionario_documentos.json")
        with open(path, "w") as contenedor:
            json.dump(self._doc_to_docID, contenedor)

    def __parse_next_block(self):
        n = self._blocksize #espacio libre en el bloque actual
        termID = 0 #inicializamos el diccionario de términos
        bloque = [] #lista de pares (termID, docID)
        with fileinput.input(self._lista_documentos) as stream:
            for linea in stream:
                n -= len(linea.encode('utf-8'))
                palabras = linea.split()
                doc = fileinput.filename()
                for pal in palabras:
                    if pal not in self._stop_words:
                        pal = self.__lematizar(pal)
                        if pal not in self._term_to_termID:
                            self._term_to_termID[pal] = termID
                            termID += 1
                        bloque.append((self._term_to_termID[pal], self._doc_to_docID[doc]))
                if n <=0:
                    yield bloque
                    n = self._blocksize
                    bloque = []
        yield bloque

if __name__ == '__main__':
    ii = II_BSBI("./libros", "./salida")
    print("longitud lista de documentos: ", len(ii._lista_documentos))

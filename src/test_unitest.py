import unittest
import interfaz_usuario
import indexador
import buscador
import tweet_downloader
import subprocess #este no se si se queda
import os
from nltk.corpus import stopwords #este por ahi vuela
import datetime

class pruebas(unittest.TestCase):
    stopwords = frozenset(stopwords.words('spanish'))
    interfaz = interfaz_usuario.UI()
    lista = []
    set_vacio = set()
    dict_vacio = {}
    temp = "./temp"
    salida = "./salida"
    linea = {
        "fecha" : "25/10/2021",
        "hora" : "20:56",
        "id" : "1452740907904737286",
        "username" : "Santiago_FyG",
        "author_id" : "747527199389954048",
        "text" : "Una niña de 4 años se hizo millonaria porque su padre le regalo 1 BTC cuando nació, cuando el BTC costaba 900 usd, en serio, quisiera tener un padre tan visionario. El mejor legado, un BTC. #Bitcoin"
    }
    """
    postin tweets listas con texto
    posting fechas lista con ids
    postin usuarios lista con ids
    postin palabras lista con ids
    fechas diccionario fecha : id
    palabras dict pal : id
    tweets dict t_id : id
    usuarios dict name : id
    bloque fecha dict id : t_id
    bloque pal dict id : t_id
    bloque tweet dict id : tweet
    bloque usuario dict id : id_t
    """
    #falta comprobar archivos, posting, indices, todo lo que se crea
    # def test_indexador_antes_de_indexar(self):
    #     #hay que hacer que este se ejecute, despues indexador_creacion y los demas
    #     archivos = os.listdir(self.temp)
    #     for archivo in archivos:
    #         self.assertFalse(archivo, "no hay archivos temporales")
    #     archivos = os.listdir(self.salida)
    #     for archivo in archivos:
    #         self.assertFalse(archivo, "no hay archivos intermedios y finales")
    #indexador
    # def test_indexador_creacion(self):
    #     #este tiene problemas io.text.... tira warnings como que no se cierra
    #     self.interfaz._indexador.indexar()
    #     archivos = os.listdir(self.temp)
    #     for archivo in archivos:
    #         self.assertTrue(archivo, "archivo intermedio")
    #     archivos = os.listdir(self.salida)
    #     for archivo in archivos:
    #         self.assertTrue(archivo, "diccionarios")

    def test_indexador_armar_lista_palabra_tweet_id(self):
        pares = []
        id_tweet = self.linea['id']
        self.interfaz._indexador.armar_lista_palabra_tweet_id(self.linea, pares)
        indice = 0
        for id_pal, id in pares:
            self.assertTrue(id_pal <= indice, "id_pal menor o igual al indice (palabras repetidas)")
            self.assertTrue(id == id_tweet, "id igual")
            indice += 1

    def test_indexador_limpiar(self):
        texto = self.linea['text']
        palabras = [
            "Una", "niña", "de", "años", "se", "hizo", "millonaria", "porque",
            "su", "padre", "le", "regalo", "BTC", "cuando", "nació", "cuando",
            "el", "BTC", "costaba", "usd", "en", "serio", "quisiera", "tener",
            "un", "padre", "tan", "visionario", "El", "mejor", "legado", "un",
            "BTC", "Bitcoin"]
        palabras_limpias = self.interfaz._indexador.limpiar(texto)
        indice = 0
        for palabra in palabras_limpias:
            self.assertTrue(palabra == palabras[indice])
            indice += 1

    def test_indexador_validar(self):
        palabras_limpias = self.interfaz._indexador.limpiar(self.linea['text'])
        self.assertTrue(len(palabras_limpias) == 34, "total palabras antes")
        palabras = [palabra for palabra in palabras_limpias if self.interfaz._indexador.validar(palabra)]
        self.assertTrue(len(palabras) == 23, "total palabras antes")
        for palabra in palabras:
            self.assertTrue(len(palabra) >= 2 and palabra not in self.stopwords)

    def test_indexador_armar_lista_tweet_id_texto(self):
        texto = self.linea['text']
        termid = 0
        pares = []
        self.interfaz._indexador.armar_lista_tweetid_texto(self.linea, pares)
        tweet_id, text = pares[0]
        self.assertTrue(type(pares[0]) == tuple, "tupla termid, texto")
        self.assertTrue(len(pares[0]) == 2, "tupla contiene 2 valores por linea")
        self.assertEqual(tweet_id, termid, "termid iguales")
        self.assertEqual(text, texto, "texto iguales")

    def test_indexador_armar_lista_usuario_tweet_id(self):
        id_tweet = self.linea['id']
        usuarioid = 0
        pares = []
        self.interfaz._indexador.armar_lista_usuario_tweet_id(self.linea, pares)
        userid, id = pares[0]
        self.assertEqual(id_tweet, id, "id iguales")
        self.assertEqual(usuarioid, userid, "userid iguales")

    def test_indexador_agregar_a_diccionario_terminos(self):
        diccionario = {}
        palabras = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete",
            "ocho", "nueve", "diez", "uno", "tres", "ocho"
        ]
        termid = 0
        for palabra in palabras:
           termid = self.interfaz._indexador.agregar_a_diccionario_terminos(palabra, termid, diccionario)
        indice = 0
        valores = diccionario.values()
        for palabra in palabras:
            self.assertTrue(diccionario.get(palabra) != None, "contiene esa palabra")
            self.assertTrue(indice in valores, "hay un valor con ese indice" )
            
    def test_indexador_invertir_bloque(self):
        pass
    def test_indexador_guardar_bloque_intermedio(self):
        pass
    def test_indexador_obtener_lista_termino_id(self):
        pass
    def test_indexador_intercalar_bloques(self):
        pass
    def test_indexador_guardar_diccionario(self):
        pass
    def test_indexador_unir_csv(self):
        pass
    def test_indexador_agregar_al_diccionario(self):
        pass
    def test_indexador_comprobar_directorio(self):
        pass
    def test_indexador_vaciar_directorios(self):
        pass
    def test_indexador_join(self):
        pass

    #downloader
    def test_tweet_downloader(self):
        pass
    def test_tweet_downloader_persistir(self):
        pass
    def test_tweet_downloader_obtener_datos_descarga_previa(self):
        pass
    def test_tweet_downloader_actualizar_datos_descargados(self):
        pass
    def test_tweet_downloader_quitar_atributos_necesarios(self):
        pass
    def test_tweet_downloader_crear_csv(self):
        pass
    #faltaria testear lo de twitter

    #interfaz
    def test_interfaz_creacion(self):
        #vericacion de tipo --incoherente
        self.assertEqual(type(self.interfaz._indexador),
            type(indexador.Indexador()), "Carga un indexador")
        self.assertEqual(type(self.interfaz._buscador),
            type(buscador.Buscador()), "Carga un buscador")
        self.assertEqual(type(self.interfaz._descargador),
            type(tweet_downloader.TweetDownloader()), "Carga un descargador")

    def test_interfaz_accion(self):
        pass
    def test_interfaz_desplegar_menu(self):
        pass
    def test_interfaz_desplegar_menu_buscador(self):
        pass
    def test_interfaz_desplegar_confirmacion(self):
        pass
    def test_interfaz_limpiar_consola(self):
        pass
    def test_interfaz_comprobar_indexador(self):
        pass
    def test_interfaz_buscador_preguntar(self):
        pass
    def test_interfaz_buscador_usuario(self):
        pass
    def test_interfaz_buscador_palabra(self):
        pass
    def test_interfaz_buscador_frase(self):
        pass
    def test_interfaz_buscador_fecha(self):
        pass
    def test_interfaz_presentar_resultados(self):
        pass
    def test_interfaz_armar_lista_fechas(self):
        pass
    def test_interfaz_solicitar_fecha(self):
        pass
    def test_interfaz_es_fecha_valida(self):
        pass
    def test_interfaz_imprimir_diccio(self):
        pass
    def test_interfaz_confirmar(self):
        pass
    def test_interfaz_cancelar_operacion(self):
        pass
    def test_interfaz_espacios_en_blanco(self):
        pass
    def test_interfaz_comprobar_desplegar_mensaje(self):
        pass
    def test_interfaz_cerrar_programa(self):
        pass

    #buscador
    def test_buscador_creacion(self):
        pass

    def test_buscador_buscar_usuario(self):
        #busqueda de un usuario
        self.lista.append("moon33_blue")
        conjunto_usuario = self.interfaz._buscador.buscar_usuario(self.lista)
        self.assertTrue(conjunto_usuario != self.set_vacio, "conjunto de usuario no vacio")
        self.assertTrue(type(conjunto_usuario) == type(self.set_vacio), "conjunto de usuario")
        self.assertTrue(len(conjunto_usuario) != 0, "conjunto de usuario con mas de un elemento")
        self.lista = []
        #busqueda de varios usuarios
        self.lista.append("Santiago_FyG")
        self.lista.append("Cryptomonkey01")
        conjunto_usuario = self.interfaz._buscador.buscar_usuario(self.lista)
        self.assertTrue(conjunto_usuario != self.set_vacio, "conjunto de usuarios no vacio")
        self.assertTrue(type(conjunto_usuario) == type(self.set_vacio), "conjunto de usuarios")
        self.assertTrue(len(conjunto_usuario) != 0, "conjunto de usuarios con mas de un elemento")
        self.lista = []
        #busqueda sin usuarios
        conjunto_usuario = self.interfaz._buscador.buscar_usuario(self.lista)
        self.assertTrue(conjunto_usuario == self.set_vacio, "conjunto sin usuarios vacio")
        self.assertTrue(type(conjunto_usuario) == type(self.set_vacio), "conjunto sin usuarios")
        self.assertTrue(len(conjunto_usuario) == 0, "conjunto sin usuarios y sin elementos")
        self.lista = []

    def test_buscador_buscar_palabra(self):
        #busqueda de una palabra
        self.lista.append("holder")
        conjunto_palabra = self.interfaz._buscador.buscar_palabra(self.lista)
        self.assertTrue(conjunto_palabra != self.set_vacio, "conjunto de palabra no vacio")
        self.assertTrue(type(conjunto_palabra) == type(self.set_vacio), "conjunto de palabra")
        self.assertTrue(len(conjunto_palabra) != 0, "conjunto de palabra con mas de un elemento")
        for texto in conjunto_palabra:
            self.assertTrue("holder" in texto.lower(), "palabra aparece en texto")
        self.lista = []
        #busqueda de varias palabras
        self.lista.append("buenas")
        self.lista.append("pero")
        conjunto_palabras = self.interfaz._buscador.buscar_palabra(self.lista)
        self.assertTrue(conjunto_palabras != self.set_vacio, "conjunto de palabras no vacio")
        self.assertTrue(type(conjunto_palabras) == type(self.set_vacio), "conjunto de palabras")
        self.assertTrue(len(conjunto_palabras) != 0, "conjunto de palabras con mas de un elemento")
        for texto in conjunto_palabras:
            texto.lower()
            self.assertTrue("pero" or "buenas" in texto, "palabras aparece en texto")
        self.lista = []
        #busqueda sin palabras
        conjunto_palabras = self.interfaz._buscador.buscar_palabra(self.lista)
        self.assertTrue(conjunto_palabras == self.set_vacio, "conjunto vacio de palabra")
        self.assertTrue(type(conjunto_palabras) == type(self.set_vacio), "conjunto vacio de palabra")
        self.assertTrue(len(conjunto_palabras) == 0, "conjunto vacio de palabra sin elementos")
        self.lista = []

    def test_buscador_buscar_frase(self):
        pass
    def test_buscador_fecha(self):
        fecha_inicial = datetime.datetime.strptime("25/10/2021 20:26", "%d/%m/%Y %H:%M")
        fecha_final = datetime.datetime.strptime("26/10/2021 07:00", "%d/%m/%Y %H:%M")
        cantidad = 1
        #set_retorno = self.interfaz._buscador.buscar_fechas(fecha_inicial, fecha_final, cantidad, [])
        #print(set_retorno)
        pass
    def test_buscador_obtener_lista_tweet_id(self):
        pass
    def test_buscador_obtener_tweet(self):

        pass
if __name__=="__main__":
    unittest.main()

import unittest
import interfaz_usuario
import indexador
import buscador
import tweet_downloader
from subprocess import PIPE, Popen

class pruebas(unittest.TestCase):
    
    interfaz = interfaz_usuario.UI()
    #falta comprobar archivos, posting, indices, todo lo que se crea

    #indexador
    def test_indexador_creacion(self):
        pass
    def test_indexador_indexar(self):
        pass
    def test_indexador_parse_next_block(self):
        pass
    def test_indexador_armar_lista_palabra_tweet_id(self):
        pass
    def test_indexador_limpiar(self):
        pass
    def test_indexador_validar(self):
        pass
    def test_indexador_armar_lista_tweet_id_texto(self):
        pass
    def test_indexador_armar_lista_usuario_tweet_id(self):
        pass
    def test_indexador_agregar_a_diccionario_terminos(self):
        pass
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
        pass
    def test_buscador_buscar_frase(self):
        pass
    def test_buscador_fecha(self):
        pass
    def test_buscador_obtener_lista_tweet_id(self):
        pass
    def test_buscador_obtener_tweet(self):
        pass
if __name__=="__main__":
    unittest.main()

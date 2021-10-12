from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError, HydrateType, OAuthType
from datetime import datetime
from csv import reader, DictWriter
from os import path
from threading import Thread
from time import sleep
import sys

class TweetDownloader():

    def __init__(self) -> None:
        self._fields = ['fecha', 'hora', 'id', 'username', 'text']
        self._ruta = "prueba.csv"
        self._lista_tweets = []
        self._api = self.__obtener_twitter_api()
        self.__obtener_datos_descarga_previa()
        self._fecha_inicio = datetime.now().strftime("%d/%m/%Y - %H:%M")

    def __obtener_twitter_api(self) -> TwitterAPI:
        o = TwitterOAuth.read_file()
        return TwitterAPI(o.consumer_key, o.consumer_secret, auth_type=OAuthType.OAUTH2, api_version='2')

    def descargar(self) -> None:
        self.__crear_csv()
        try:
            print("TWEET DOWNLOADER")
            self.__quitar_reglas_del_stream()
            self.__agregar_regla_al_stream('("#bitcoin" OR "bitcoin" OR ("bitcoin" BTC)) -is:reply -is:retweet -is:quote -has:links -has:images -has:videos lang:es')
            stream = self.__iniciar_stream()

            self.__iniciar_animacion()

            for tweet in stream:
                tweet = self.__quitar_atributos_innecesarios(tweet)
                self._lista_tweets.append(tweet)
                self.__actualizar_datos_descargados(tweet)
                if(self.__es_cantidad_suficiente()):
                    self.__persistir_tweets()

        except KeyboardInterrupt:
	        print('\nDone!')

        except TwitterRequestError as e:
            print(f'\n{e.status_code}')
            for msg in iter(e):
                print(msg)

        except TwitterConnectionError as e:
            print(e)

        finally:
            self.parar()

    def __crear_csv(self):
        if not path.isfile(self._ruta):
            with open(self._ruta, mode="w", encoding="utf-8", newline = '') as documento:
                escritor = DictWriter(documento, fieldnames = self._fields, delimiter=",")
                escritor.writeheader()

    def __quitar_reglas_del_stream(self):
        """
            DELETE STREAM RULES
        """
        rule_ids = []
        respuesta = self.__obtener_reglas_del_stream()
        for item in respuesta:
            if 'id' in item:
                rule_ids.append(item['id'])
        if rule_ids:
            respuesta = self._api.request('tweets/search/stream/rules', {'delete': {'ids':rule_ids}})
            self.__verificar_respuesta(respuesta)

    def __agregar_regla_al_stream(self, query):
        """
            ADD STREAM RULES
        """
        respuesta = self._api.request('tweets/search/stream/rules', {'add': [{'value':query}]})
        self.__verificar_respuesta(respuesta)
        return respuesta

    def __verificar_respuesta(self, respuesta):
        if not (respuesta.status_code == 200 or respuesta.status_code == 201):
            raise TwitterRequestError(respuesta.status_code)

    def __obtener_reglas_del_stream(self):
        """
            GET STREAM RULES
        """
        respuesta = self._api.request('tweets/search/stream/rules', method_override='GET')
        self.__verificar_respuesta(respuesta)
        return respuesta

    def __iniciar_stream(self):
        """
            START STREAM
        """
        respuesta = self._api.request('tweets/search/stream', {
                'expansions': 'author_id',
                'tweet.fields': 'created_at,id,text',
                'user.fields': 'username'
            },
            hydrate_type=HydrateType.APPEND)
        self.__verificar_respuesta(respuesta)
        return respuesta.get_iterator()

    def __es_cantidad_suficiente(self) -> bool:
        return len(self._lista_tweets) == 1000

    def __quitar_atributos_innecesarios(self, tweet : dict) -> dict:
        aux = {}
        fecha = datetime.fromisoformat(tweet['data']['created_at'][:-1])
        aux['fecha'] = fecha.strftime("%d/%m/%Y")
        aux['hora'] = fecha.strftime("%H:%M")
        aux['id'] = tweet['data']['id']
        aux['username'] = tweet['data']['author_id_hydrate']['username']
        aux['text'] = tweet['data']['text']
        return aux

    def __persistir_tweets(self) -> None:
        with open(self._ruta, mode="a", encoding="utf-8", newline = '') as documento:
            escritor = DictWriter(documento, fieldnames = self._fields, delimiter=",")
            for tweet in self._lista_tweets:
                escritor.writerow(tweet)
        self._lista_tweets = []

    def parar(self) -> None:
        self.__persistir_tweets()
        self._animacion_activa = False

    def __iniciar_animacion(self):
        self._animacion = self.__obtener_animacion()
        self._animacion_idx = 0
        self._animacion_activa = True
        Thread(target=self.__actualizar_animacion).start()

    def __obtener_datos_descarga_previa(self):
        self._cantidad = 0
        self._espacio_usado = 0
        if path.isfile(self._ruta):
            self._espacio_usado = path.getsize(self._ruta)
            with open(self._ruta, encoding="utf-8", newline = '') as documento:
                self._cantidad = sum(1 for _ in reader(documento)) - 1

    def __actualizar_datos_descargados(self, tweet : dict) -> None:
        self._cantidad += 1
        self._espacio_usado += sys.getsizeof(tweet)

    def __actualizar_animacion(self):
        while self._animacion_activa:
            print(self._animacion[self._animacion_idx % 17],
                  f"Fecha de inicio: {self._fecha_inicio} |",
                  f"Tweets descargados: {self._cantidad} |",
                  f"Espacio usado en bytes: {self._espacio_usado}", end="\r")

            self._animacion_idx += 1
            sleep(.1)

    def __obtener_animacion(self):
        return [
            "[        ]",
            "[=       ]",
            "[===     ]",
            "[====    ]",
            "[=====   ]",
            "[======  ]",
            "[======= ]",
            "[========]",
            "[ =======]",
            "[  ======]",
            "[   =====]",
            "[    ====]",
            "[     ===]",
            "[      ==]",
            "[       =]",
            "[        ]",
            "[        ]"
        ]

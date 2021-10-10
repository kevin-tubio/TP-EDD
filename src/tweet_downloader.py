from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError, HydrateType, OAuthType
from datetime import datetime
from csv import DictWriter
from os import path

class TweetDownloader():

    def __init__(self) -> None:
        self._fields = ['fecha', 'hora', 'id', 'author_id', 'text']
        self._ruta = "prueba.csv"
        self._lista_tweets = []
        self._api = self.__obtener_twitter_api()

    def __obtener_twitter_api(self) -> TwitterAPI:
        o = TwitterOAuth.read_file()
        return TwitterAPI(o.consumer_key, o.consumer_secret, auth_type=OAuthType.OAUTH2, api_version='2')

    def descargar(self) -> None:
        self.__crear_csv()
        try:
            self.__quitar_reglas_del_stream()
            self.__agregar_regla_al_stream('("#bitcoin" OR "bitcoin" OR ("bitcoin" BTC)) -is:reply -is:retweet -is:quote -has:links -has:images -has:videos lang:es')

            for tweet in self.__iniciar_stream():
                tweet = self.__quitar_atributos_innecesarios(tweet)
                self._lista_tweets.append(tweet)
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
            print(f'[{respuesta.status_code}] RULES DELETED')

    def __agregar_regla_al_stream(self, query):
        """
            ADD STREAM RULES
        """
        respuesta = self._api.request('tweets/search/stream/rules', {'add': [{'value':query}]})
        self.__verificar_respuesta(respuesta)
        print(f'[{respuesta.status_code}] RULES ADDED')
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
                'tweet.fields': 'author_id,created_at,id,text',
            },
            hydrate_type=HydrateType.APPEND)
        self.__verificar_respuesta(respuesta)
        print(f'[{respuesta.status_code}] STREAM STARTED...')
        return respuesta

    def __es_cantidad_suficiente(self) -> bool:
        return len(self._lista_tweets) == 1000

    def __quitar_atributos_innecesarios(self, tweet : dict) -> dict:
        aux = {}
        fecha = datetime.fromisoformat(tweet['data']['created_at'][:-1])
        aux['fecha'] = fecha.strftime("%d/%m/%Y")
        aux['hora'] = fecha.strftime("%H:%M")
        aux['id'] = tweet['data']['id']
        aux['author_id'] = tweet['data']['author_id']
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


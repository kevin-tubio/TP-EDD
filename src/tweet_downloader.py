from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError, HydrateType, OAuthType
import csv
from datetime import datetime

class TweetDownloader():

    def __init__(self) -> None:
        self._fields = ['fecha', 'hora', 'id', 'text']
        self._lista_tweets = []
        self._EXPANSIONS = 'author_id,referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id,attachments.media_keys,attachments.poll_ids,geo.place_id,entities.mentions.username'
        self._TWEET_FIELDS = 'author_id,conversation_id,created_at,entities,geo,id,lang,public_metrics,source,text'
        self._USER_FIELDS = 'created_at,description,entities,location,name,profile_image_url,public_metrics,url,username'
        self._api = self.__obtener_twitter_api()

    def descargar(self, query) -> None:
        try:
            self.__quitar_reglas_del_stream()
            self.__agregar_regla_al_stream(query)
            self.__obtener_reglas_del_stream()

            for tweet in self.__iniciar_stream():
                tweet = self.__quitar_atributos_innecesarios(tweet)
                self._lista_tweets.append(tweet)
                if(self.__es_cantidad_suficiente()):
                    self.__persistir_tweets()

        except KeyboardInterrupt:
            self.parar()

        except TwitterRequestError as e:
            print(f'\n{e.status_code}')
            for msg in iter(e):
                print(msg)

        except (TwitterConnectionError, Exception) as e:
            print(e)

    def __es_cantidad_suficiente(self) -> bool:
        return len(self._lista_tweets) == 1000

    def __persistir_tweets(self) -> None:
        with open("prueba.csv", mode="a", encoding="utf-8", newline = '') as documento:
            escritor = csv.DictWriter(documento, fieldnames = self._fields, delimiter=",")
            escritor.writeheader()
            
            for tweet in lista_tweets:
                escritor.writerow(tweet)
        
            

    def parar(self) -> None:
        self.__persistir_tweets()
        print('\nDone!')

    def __obtener_twitter_api(self) -> TwitterAPI:
        o = TwitterOAuth.read_file()
        return TwitterAPI(o.consumer_key, o.consumer_secret, auth_type=OAuthType.OAUTH2, api_version='2')

    def __agregar_regla_al_stream(self, query):
        """
            ADD STREAM RULES
        """
        respuesta = self._api.request('tweets/search/stream/rules', {'add': [{'value':query}]})
        self.__verificar_respuesta(respuesta)
        print(f'[{respuesta.status_code}] RULES ADDED')
        return respuesta

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
                'expansions': self._EXPANSIONS,
                'tweet.fields': self._TWEET_FIELDS,
                'user.fields': self._USER_FIELDS,
            },
            hydrate_type=HydrateType.APPEND)
        self.__verificar_respuesta(respuesta)
        print(f'[{respuesta.status_code}] STREAM STARTED...')
        return respuesta

    def __quitar_reglas_del_stream(self):
        """
        DELETE STREAM RULES
        """
        rule_ids = []
        respuesta = self._api.request('tweets/search/stream/rules', method_override='GET')
        for item in respuesta:
            if 'id' in item:
                rule_ids.append(item['id'])
        if rule_ids:
            respuesta = self._api.request('tweets/search/stream/rules', {'delete': {'ids':rule_ids}})
            print(f'[{respuesta.status_code}] RULES DELETED')

    def __verificar_respuesta(self, respuesta):
        if not (respuesta.status_code == 200 or respuesta.status_code == 201):
            raise TwitterRequestError(respuesta.status_code)

    def __quitar_atributos_innecesarios(self, tweet : dict) -> dict:
        aux = {}
        fecha = datetime.fromisoformat(tweet['data']['created_at'][:-1])
        aux['fecha'] = fecha.strftime("%d/%m/%Y")
        aux['hora'] = fecha.strftime("%H:%M")
        aux['id'] = tweet['data']['id']
        aux['text'] = tweet['data']['text']
        return aux


if __name__ == "__main__":
    prueba = TweetDownloader()
    prueba.descargar('("#bitcoin" OR "bitcoin" OR ("bitcoin" BTC)) -is:reply -is:retweet -is:quote -has:links -has:images -has:videos lang:es')

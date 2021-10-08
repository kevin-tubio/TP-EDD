import TwitterAPI
import json

class TweetDownloader():

    def __init__(self) -> None:
        self._lista_tweets = []

    def descargar(self) -> None:
        tweet = None
        self.__quitar_atributos_innecesarios(tweet)
        self._lista_tweets.append(tweet)
        if(self.__es_cantidad_suficiente()):
            self.__persistir_tweets()
        pass

    def __es_cantidad_suficiente(self) -> bool:
        pass

    def __quitar_atributos_innecesarios(self, tweet) -> dict:
        pass

    def __persistir_tweets(self) -> None:
        pass

    def parar(self) -> None:
        self.__persistir_tweets()
        pass


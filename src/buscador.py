from datetime import datetime
import re
from excepciones import FechaInvalidaException
import json

class Buscador:

    def __init__(self):
        self.__formato_hora = re.compile("^(?:[0-1]\d|2[0-4]):[0-5]\d$")
        self.__formato_fecha = re.compile("^(?:0[1-9]|[1-2]\d|3[0-1])/(?:0[1-9]|1[0-2])/2021$")

    def buscar_fecha_hora(self, fecha_1 : str, hora_1 : str, cantidad : int, indice : dict, fecha_2="", hora_2=""):
        self.__validar_cantidad(cantidad)
        self.__validar_fecha(fecha_1)
        self.__validar_hora(hora_1)
        dt = datetime.strptime(f"{fecha_1} {hora_1}", "%d/%m/%Y %H:%M")
        n = 0
        lista_id = []
        #opcional falta que aumente n por cada adicion pero no se como
        #lista_id = [id for date, id in indice if dt <= date and n < cantidad]
        if fecha_2 == "" or hora_2 == "":
            #problema, itera todo, si indice[fecha] entonces que pasa si no llega a n las adiciones?
            for date, id in range(indice, cantidad):
                if dt <= date and n < cantidad:
                    lista_id.append(id)
                    n += 1
                    if n == cantidad:
                        break
        else:
            self.__validar_fecha(fecha_2)
            self.__validar_hora(hora_2)
            dt2 = datetime.strptime(f"{fecha_2} {hora_2}", "%d/%m/%Y %H:%M")
            #opcional tiene el problema de iterar todos los valores a menos que le pongas un break
            #lista_id = [id for date, id in indice if dt <= date <= dt2 and n < cantidad]
            for date, id in indice:
                if dt <= date <= dt2 and n < cantidad:
                    lista_id.append(id)
                    n += 1
                    if n == cantidad:
                        break
        return set(lista_id)

    def buscar_palabra(self, palabra_lematizada : str, indice : dict, cantidad):
        #devolver un set vacio, este o no la palabra
        set_id = set()
        #iterar valores, si no esta devuelve None
        valores = indice.get(self.__validar_string(palabra_lematizada))
        #si no es none
        if valores:
            # validar cantidad de twits
            if self.__validar_cantidad(cantidad):
                n = 0
                #con un while podes hacer mientras, con el for conseguis los valores
                """
                para condicion necesitas algo, con cantidad no podes, porque no sabes cuantas ocurrencias puede haber
                cant > ocu; cant == ocu; cant < ocu, deberias hacer 2 casos de while
                while cant>0: 
                    if #como haces para preguntar por el id? indice[lema][x] donde x tenes que ir actulizando
                        set.add(indice[lema][x])
                        cant-=1
                        x += 1
                        te podrias ir de rango si no esta bien articulado
                """
                for id in valores:#si n < cantidad no pasa nada, termina el for antes, igual termina al mismo tiempo, mayor lo corta
                    if n < cantidad:
                        n += 1
                        set_id.add(id)
                        if n == cantidad:#cortar la iteracion cuando agregaste la cantidad deseada
                            break
        return set_id
    #revisar
    def buscar_frase(self, frase : str, indice : dict, cantidad):
        set_frase_id = set()
        valor = indice.get(self.__validar_string(frase))
        if valor and self.__validar_cantidad(cantidad):
            n = 0
            for id in indice[frase]:
                if n < cantidad:
                    n += 1
                    set_frase_id.add(id)
                    if n == cantidad:
                        break
        return set_frase_id
    
    def buscar_usuario(self, usuario):
        diccio = "./salida/diccionario_usuarios.json"
        posting = "./salida/posting_usuarios.json"
        userID = ""
        ubicacion = ""
        tweets = ""
        try:
            with open (diccio, "r") as diccionario:
                data = json.load(diccionario)
                userID = data[usuario]
                ubicacion = list(data.values()).index(userID)

            with open (posting, "r") as post:
                linea = post.readline()
                tweets = self.limpiar_resultado(linea, ubicacion)
        except KeyError as e:
            print("No se encontró el usuario: " + str(e))
            return tweets
    
    def limpiar_resultado(self, linea, ubicacion):
        linea = linea.split("]")
        tweets = linea[ubicacion]
        molesto = re.compile("[\[\s\"]")
        tweets = list(re.sub(molesto, "", tweets).split(","))
        return tweets
       
        
            
    #tal vez no levantar excepciones pero pedir que reingrese un dato valido a menos que ya desde otro la
    #se validen las entradas y esta parte directamente hace y no pregunta
    def __validar_cantidad(self, cantidad : int):
        return cantidad > 0

    def __validar_string(self, string):
        return type(string) == str and len(string) >= 2

    def __validar_fecha(self, fecha : str):
        if not self.__formato_fecha.match(fecha):
            raise FechaInvalidaException(f"{fecha} no es una fecha valida")

    def __validar_hora(self, hora : str):
        if not self.__formato_hora.match(hora):
            raise FechaInvalidaException(f"{hora} no es una hora valida")

# if __name__=="__main__":
#     from indexador import Indexador
#     
#     a = Indexador()
#     palabraLematizada = a.__lematizar("Hola")
#     b = Buscador()
#     c = b.buscar_palabra(palabraLematizada, a.obtener_indice_palabra_id(palabraLematizada), 3)
#     print(c)

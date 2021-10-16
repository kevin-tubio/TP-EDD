import datetime
import re

class Buscador:

    def __init__(self):
        self.__formato_hora = re.compile("^((0[0-9]|1[0-9]|2[0-3]):(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]))$")
        self.__formato_fecha = re.compile("^((0[1-9]|1[0-9]|2[0-9]|3[0-1])/(0[1-9]|1[0-2])/(2021))$")

    def buscar_fecha_hora(self, fecha_1 : str, hora_1 : str, cantidad : int, indice : dict, fecha_2="", hora_2=""):
        self.__validar_cantidad(cantidad)
        dt = datetime.datetime.strptime(f"{self.__validar_fecha(fecha_1).group(1)} {self.__validar_hora(hora_1).group(1)}", "%d/%m/%Y %H:%M")
        n = 0
        lista_id = []
        #opcional falta que aumente n por cada adicion pero no se como
        #lista_id = [id for date, id in indice if dt <= date and n < cantidad]
        if fecha_2 == "" or hora_2 == "":
            for date, id in indice:
                if dt <= date and n < cantidad:
                    lista_id.append(id)
                    n += 1
                    if n == cantidad:
                        break
        else:
            dt2 = datetime.datetime.strptime(f"{self.__validar_fecha(fecha_2).group(1)} {self.__validar_hora(hora_2).group(1)}", "%d/%m/%Y %H:%M")
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
        if valores != None:
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
        lista_frase_id = []
        if self.__validar_string(frase) and self.__validar_cantidad(cantidad):
            n = 0
            for sentence, id in indice:
                if frase == sentence and n < cantidad:
                    n += 1
                    lista_frase_id.append(id)
                    if n == cantidad:
                        break
        return set(lista_frase_id)
    #tal vez no levantar excepciones pero pedir que reingrese un dato valido a menos que ya desde otro la
    #se validen las entradas y esta parte directamente hace y no pregunta
    def __validar_cantidad(self, cantidad : int):
        return cantidad > 0

    def __validar_string(self, string):
        return type(string) == str and len(string) >= 2

    def __validar_fecha(self, fecha : str):
        return self.__formato_fecha.match(fecha)

    def __validar_hora(self, hora : str):
        return self.__formato_hora.match(hora)

# if __name__=="__main__":
#     from indexador import Indexador
#     a = Indexador()
#     b = Buscador()
#     c = b.buscar_palabra(a.lematizar("hola"), a.obtener_indice(), 3)
#     print(c)

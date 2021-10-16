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
                if date <= dt and n < cantidad:
                    lista_id.append(id)
                    n += 1
                    if n == cantidad:
                        break
        else:
            dt2 = datetime.datetime.strptime(f"{self.__validar_fecha(fecha_2).group(1)} {self.__validar_hora(hora_2).group(1)}", "%d/%m/%Y %H:%M")
            #opcional 
            #lista_id = [id for date, id in indice if dt <= date <= dt2 and n < cantidad]
            for date, id in indice:
                if dt <= date <= dt2 and n < cantidad:
                    lista_id.append(id)
                    n += 1
                    if n == cantidad:
                        break
        return set(lista_id)

    def buscar_palabra(self, palabra_lematizada : str, indice : dict, cantidad):
        lista_palabra_id = []
        if self.__validar_string(palabra_lematizada) and self.__validar_cantidad(cantidad):
            n = 0
            for palabra, id in indice:
                if palabra == palabra_lematizada and n < cantidad:
                    n += 1
                    lista_palabra_id.append(id)
                    if n == cantidad:
                        break
        return set(lista_palabra_id)

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

    def __validar_cantidad(self, cantidad : int):
        return cantidad > 0

    def __validar_string(self, string):
        return type(string) == str and len(string) >= 2

    def __validar_fecha(self, fecha : str):
        return self.__formato_fecha.match(fecha)

    def __validar_hora(self, hora : str):
        return self.__formato_hora.match(hora)

if __name__=="__main__":
    pass

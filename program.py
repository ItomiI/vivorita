from clases import gusano, manzana
from threading import Thread,Timer
from os import system
from msvcrt import kbhit, getwche


puntos = 0  # los puntos que voy
letra = ""  # la letra que se toco
w, h = 20, 20  # el tamaño del array
toX = 0  # hacia donde se mueve x
toY = 0  # hacia donde se mueve y
wasX = 99999  # hacia donde se movio la anterior vez x o no se algo asi
wasY = 99999  # hacia donde se movio la anterior vez y
tDefault = 0.3  # cuanto es el reset de tiempoHastaMover
# el tiempo q tarda hasta moverse otra vez, seria en segndos pero como que no
tiempoHastaMover = tDefault
elMapa = [["|-|" for x in range(w)] for y in range(h)]  # el mapa a dibujar
# y x
# x 2x 3x
# y
# 2y
# 3y

gusanito: gusano = gusano()  # inicio un head
manzanita = manzana(w, h)  # y una manzana


def direccion(x, y):  # una funcion q dependiendo el x e y dados te dice algo
    if x == 1 and y == 0:
        return "abajo"
    elif x == -1 and y == 0:
        return "arriba"
    elif x == 0 and y == 1:
        return "derecha"
    elif x == 0 and y == -1:
        return "izquierda"
    else:
        return "nose"

def dibujar():  # dibuja elMapa o otro array 2d
    global elMapa
    global manzanita
    system('cls')  # limpia la consola
    # info
    print(
        f"puntos: {puntos} | direccion: {direccion(toX,toY)} | Posicion manzana: {manzanita.getpos()[1]+1,manzanita.getpos()[0]+1} ")
    t = len(elMapa)  # cuanto mide
    for i in range(t):  # por x
        for j in range(t):  # por y
            # dibujo la pos x y(i j) sin salto de linea
            print(elMapa[i][j], end="")
        print()  # salto de linea

def comio(g: gusano, m: manzana):  # devuelve true si la cabeza del guzano esta en la manzana si no false
    return g.getpos() == m.getpos()

def choco(gusanin: gusano):  # devuelve true si la cabeza del guzano esta en una parte del cuerpo, va recorriendo todos asta que sea None
    bodyActual = gusanin.getcola()  # la cola actual que se verifica
    a, b = gusanin.getpos()  # la poscion de la cabeza
    while bodyActual != None:  # mientras que no sea None osea que haya un cuerpo
        c, d = bodyActual.getpos()  # la pos del cuerpo actual
        if [a, b] == [c, d]:  # si las dos pos son iguales
            return True
        else:
            # como no lo son que el cuerpo actual sea la siguiente
            bodyActual = bodyActual.getcola()
    return False

def start():  # mando esto cuando empieza el programa
    global elMapa
    global gusanito, manzanita
    gusanito.posicionar(elMapa)  # posiciono el gusano
    manzanita.posicionar(elMapa)  # posiciono la manzana

def update():  # muchas cosas | se repite todo el tiempo
    global tDefault
    global letra
    global elMapa
    global puntos
    global gusanito, manzanita
    global toX, toY, tiempoHastaMover,wasX,wasY
    global w, h
    dibujar()  # primero que nada dibujo

    if kbhit():  # si toque una tecla
        letra = getwche()  # guardo que tecla
        if letra == "w":  # si es la w guado la direccion
            toX = -1
            toY = 0
            if toX == wasX*-1 and toY == wasY*-1:  # si se movio para el otro lado antes, que no y lo mismo con lo de abajo
                letra = "s"
                toX = 1
                toY = 0
        elif letra == "s":
            toX = 1
            toY = 0
            if toX == wasX*-1 and toY == wasY*-1:
                letra = "w"
                toX = -1
                toY = 0
        elif letra == "a":
            toX = 0
            toY = -1
            if toX == wasX*-1 and toY == wasY*-1:
                letra = "d"
                toX = 0
                toY = 1

        elif letra == "d":
            toX = 0
            toY = 1
            if toX == wasX*-1 and toY == wasY*-1:
                letra = "a"
                toX = 0
                toY = -1

    tiempoHastaMover -= 1/60  # resto uno sobre 1/60

    if tiempoHastaMover < 0:  # si ya es momento de mover

        gusanoPosicion = gusanito.getpos()
        tx = toX  # esto a donde se va a mover realmente
        ty = toY

        if toX != 0:  # si hacia x no es 0
            # si se va a pasar de los limites basicamente h |
            if toX == 1 and (gusanoPosicion[0] + 1) >= h:
                tx = -19# podria ser -h-1 y = h-1
            elif toX == -1 and gusanoPosicion[0] <= 0:
                tx = 19
        if toY != 0:  # si hacia x no es 0
            # si se va a pasar de los limites basicamente   | w
            if toY == 1 and (gusanoPosicion[1] + 1) >= w:
                ty = -19
            elif toY == -1 and gusanoPosicion[1] <= 0:
                ty = 19

        gusanito.mover(tx, ty, elMapa)  # se mueve
        tx = toX  # reseteo tx y ty
        ty = toY
        if comio(gusanito, manzanita):  # si come
            gusanito.agregar()  # agrego un body
            manzanita.repos(elMapa)  # reposiciono la manzana
            puntos += 1  # sumo un punto

        if choco(gusanito):  # si choco con si mismo reinicio todo
            gusanito = gusano()#spawneo un nuevo gusano
            elMapa = [["|-|" for x in range(w)] for y in range(h)]#reinicio el mapa
            manzanita = manzana(w, h)#spawneo un nuevo manzana
            puntos = 0#reinicio los puntos
            start()#hago el start para reposicionar

        wasX = toX#guardo esto para la info
        wasY = toY
        tiempoHastaMover = tDefault # reinicio el tiempo de momento de mover

    Timer(1/100, update).start()  # que se repita todo


start()
U = Thread(target=update).start()

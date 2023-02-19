from random import randrange


class vector2:
    def __init__(self, xx: int, yy: int):  # se inicia en donde diga xx, yy
        self.v = [xx, yy]
        self.x = xx
        self.y = yy

    def tp(self, xx: int, yy: int):  # se tpa a donde diga xx, yy
        self.v = [xx, yy]
        self.x = xx
        self.y = yy

    def mover(self, xx, yy):  # se mueve en x i en y lo que diga el parametro xx, yy
        self.x += xx
        self.y += yy
        self.v[1] += yy
        self.v[0] += xx

    def getpos(self):  # devuelve el vector en forma [x,y]
        return self.v

    def getx(self):  # devuelve el x del vector
        return self.x

    def gety(self):  # devuelve el y del vector
        return self.y


class gusano:  # la cabeza del guzano, funciona como una linkedlist

    # inicia en 0,0 default pero puede donde quiera
    def __init__(self, x: int = 0, y: int = 0):
        self.pos = vector2(x, y)  # la pos inicial
        # la pos anterior es la inicial porque no se movio
        self.pos2 = vector2(x, y)
        self.body = None  # la siguiente parte del cuerpo

    # lo que es cuando hago x = cola o como se llame en vez de algo raro
    def __str__(self):
        return "|G|"

    # se posiciona en una array, pone "|G|" en la posicion y devuelve la "|X|" en donde estaba
    def posicionar(self, mat: list[list]):
        mat[self.pos2.getx()][self.pos2.gety()] = "|-|"  # pone X donde estaba
        mat[self.pos.getx()][self.pos.gety()] = self  # pone G donde esta
        if self.body != None:  # si el body no es None
            self.body.posicionar(mat)  # que se posicione en el array

    # se mueve hacia una direccion (x y)
    def mover(self, x: int, y: int, mat=list[list]):
        v = self.pos.getpos()  # guardo la pos actual
        # cambio la anterior por la actual pq se va a mover
        self.pos2.tp(v[0], v[1])
        self.pos.mover(x, y)  # se mueve el vector
        if self.body != None:  # si el body no es None
            self.body.mover(self.pos2.getpos(), mat)  # se mueve
        self.posicionar(mat)  # se posiciona

    # si come agrega uno, si ya hay uno agrega uno al hijo y haci susesivamente
    def agregar(self):
        if self.body == None:  # si el body es none
            p = self.pos2.getpos()  # guardo la pos anterior
            # creo el nuevo body en la pos anterior
            self.body = cola(p[0], p[1])
            # innesesario pero devuelve el body nuevo, por si quiero guardad los nuevos bodys
            return self.body
        else:
            self.body.agregar()  # como ya tiene uno, agrega un body al body y asi susesivamente

    # retorno la pos actual en forma de [x,y]
    def getpos(self):
        return self.pos.getpos()

    # retorno el body si no es None
    def getcola(self):
        return self.body if self.body is not None else None


class cola:  # el body

    # inicia en 0,0 default pero puede donde quiera
    def __init__(self, x: int, y: int):
        self.pos = vector2(x, y)  # la pos inicial
        # la pos anterior es la inicial porque no se movio
        self.pos2 = vector2(x, y)
        self.body = None  # la siguiente parte del cuerpo

    # lo que es cuando hago x = cola o como se llame
    def __str__(self):
        return "|C|"

    # se posiciona en una array, pone "|C|" en la posicion y devuelve la "|X|" en donde estaba
    def posicionar(self, mat: list[list]):
        mat[self.pos2.getx()][self.pos2.gety()] = "|-|"  # pone X donde estaba
        mat[self.pos.getx()][self.pos.gety()] = self  # pone C donde esta
        if self.body != None:  # si el body no es None
            self.body.posicionar(mat)  # que se posicione en el array

    # se tpea a un lugar (x y)
    def mover(self, v: list[int], mat=list[list]):
        h = self.pos.getpos()  # guardo la pos actual
        # cambio la anterior por la actual pq se va a mover
        self.pos2.tp(h[0], h[1])
        self.pos.tp(v[0], v[1])  # se tpea el vector
        if self.body != None:  # si el body no es None
            self.body.mover(self.pos2.getpos(), mat)  # se mueve
        self.posicionar(mat)  # se posiciona

    # si se comio uno agrega uno, si ya hay uno agrega uno al hijo y haci susesivamente
    def agregar(self):
        if self.body == None:  # si el body es none
            p = self.pos2.getpos()  # guardo la pos anterior
            # creo el nuevo body en la pos anterior
            self.body = cola(p[0], p[1])
            # innesesario pero devuelve el body nuevo, por si quiero guardad los nuevos bodys
            return self.body
        else:
            self.body.agregar()  # como ya tiene uno, agrega un body al body y asi susesivamente

    # retorno la pos actual en forma de [x,y]
    def getpos(self):
        return self.pos.getpos()

    # retorno el body si no es None
    def getcola(self):
        return self.body if self.body is not None else None


class manzana:

    # se inicia en una pos aleatoria entre mx,my(los limites)
    def __init__(self, mx, my):
        self.mx = mx  # guardo los limites para despues
        self.my = my
        x = randrange(1, mx)  # el x donde se va a poner
        y = randrange(1, my)  # el y donde se va a poner
        self.pos = vector2(x, y)  # se crea el vector

    # que es
    def __str__(self):
        return "|M|"

    # retorn la pos actual en forma de [x,y]
    def getpos(self):
        return self.pos.getpos()

    # se posiciona
    def posicionar(self, mat: list[list]):
        # en donde salio el vector
        mat[self.pos.getx()][self.pos.gety()] = self.__str__()

    # cuando come se reposiciona, en el mat
    def repos(self, mat: list[list]):
        x = randrange(0, self.mx)  # nuevo x
        y = randrange(0, self.my)  # nuevo y
        while mat[x][y] != "|-|":  # por si la pos esta usada por un G o
            x = randrange(0, self.mx)  # nuevo x
            y = randrange(0, self.my)  # nuevo y
        self.pos.tp(x, y)  # la nueva pos
        mat[x][y] = self.__str__()  # se posiciona

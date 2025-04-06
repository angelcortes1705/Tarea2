class Conjunto:
    def __init__(self, capacidad=100):
        self.capacidad = capacidad
        self.tabla = [[] for _ in range(capacidad)]

    def _hash(self, valor):
        return hash(valor) % self.capacidad

    def insertar(self, valor):
        indice = self._hash(valor)
        if valor not in self.tabla[indice]:
            self.tabla[indice].append(valor)

    def eliminar(self, valor):
        indice = self._hash(valor)
        if valor in self.tabla[indice]:
            self.tabla[indice].remove(valor)

    def buscar(self, valor):
        indice = self._hash(valor)
        return valor in self.tabla[indice]

    def union(self, otro):
        resultado = Conjunto(self.capacidad)
        for lista in self.tabla:
            for elemento in lista:
                resultado.insertar(elemento)
        for lista in otro.tabla:
            for elemento in lista:
                resultado.insertar(elemento)
        return resultado

    def interseccion(self, otro):
        resultado = Conjunto(self.capacidad)
        for lista in self.tabla:
            for elemento in lista:
                if otro.buscar(elemento):
                    resultado.insertar(elemento)
        return resultado

    def diferencia(self, otro):
        resultado = Conjunto(self.capacidad)
        for lista in self.tabla:
            for elemento in lista:
                if not otro.buscar(elemento):
                    resultado.insertar(elemento)
        return resultado

# Implementación de un Mapa (Dictionary) usando tabla hash abierta con listas de colisiones
class Mapa:
    def __init__(self, capacidad=100):
        self.capacidad = capacidad
        self.tabla = [[] for _ in range(capacidad)]

    def _hash(self, clave):
        return hash(clave) % self.capacidad

    def insertar(self, clave, valor):
        indice = self._hash(clave)
        for i, (k, _) in enumerate(self.tabla[indice]):
            if k == clave:
                self.tabla[indice][i] = (clave, valor)
                return
        self.tabla[indice].append((clave, valor))

    def buscar(self, clave):
        indice = self._hash(clave)
        for k, v in self.tabla[indice]:
            if k == clave:
                return v
        return None

    def actualizar(self, clave, valor):
        self.insertar(clave, valor)

    def eliminar(self, clave):
        indice = self._hash(clave)
        for i, (k, _) in enumerate(self.tabla[indice]):
            if k == clave:
                del self.tabla[indice][i]
                return

if __name__ == "__main__":
    # Prueba rápida de funcionalidad
    a = Conjunto()
    b = Conjunto()
    for i in range(5):
        a.insertar(i)
    for i in range(3, 8):
        b.insertar(i)

    print("Intersección:", [x for lista in a.interseccion(b).tabla for x in lista])
    print("Unión:", [x for lista in a.union(b).tabla for x in lista])

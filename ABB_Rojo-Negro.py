RED = "RED"
BLACK = "BLACK"

# Nodo para el Árbol Rojo-Negro
class RBNode:
    def __init__(self, key, color=RED, left=None, right=None, parent=None, size=1):
        self.key = key              # Clave del nodo
        self.color = color          # Color del nodo (RED o BLACK)
        self.left = left            # Hijo izquierdo
        self.right = right          # Hijo derecho
        self.parent = parent        # Padre del nodo
        self.size = size            # Tamaño del subárbol (número de nodos)

# Árbol Rojo-Negro
class RedBlackTree:
    def __init__(self):
        # Nodo NIL (sentinela) para simplificar operaciones
        self.NIL = RBNode(key=None, color=BLACK, size=0)
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL
        self.root = self.NIL        # La raíz inicia como NIL

    # Realiza una rotación izquierda para reequilibrar el árbol
    def left_rotate(self, x):
        y = x.right                    # y es el hijo derecho de x
        x.right = y.left               # Mueve el subárbol izquierdo de y a la derecha de x
        if y.left != self.NIL:
            y.left.parent = x          # Actualiza el padre de y.left
        y.parent = x.parent            # Asigna el padre de x a y
        if x.parent == self.NIL:
            self.root = y              # y se vuelve la raíz
        elif x == x.parent.left:
            x.parent.left = y          # y se asigna como hijo izquierdo
        else:
            x.parent.right = y         # o como hijo derecho
        y.left = x                     # x pasa a ser hijo izquierdo de y
        x.parent = y                   # Actualiza el padre de x

        y.size = x.size                # Actualiza tamaños
        x.size = x.left.size + x.right.size + 1

    # Realiza una rotación derecha para reequilibrar el árbol
    def right_rotate(self, y):
        x = y.left                     # x es el hijo izquierdo de y
        y.left = x.right               # Mueve el subárbol derecho de x a la izquierda de y
        if x.right != self.NIL:
            x.right.parent = y         # Actualiza el padre de x.right
        x.parent = y.parent            # Asigna el padre de y a x
        if y.parent == self.NIL:
            self.root = x              # x se vuelve la raíz
        elif y == y.parent.right:
            y.parent.right = x         # x se asigna como hijo derecho
        else:
            y.parent.left = x          # o como hijo izquierdo
        x.right = y                    # y pasa a ser hijo derecho de x
        y.parent = x                   # Actualiza el padre de y

        x.size = y.size                # Actualiza tamaños
        y.size = y.left.size + y.right.size + 1

    # Inserta una nueva clave en el árbol
    def insert(self, key):
        z = RBNode(key)                # Crea el nuevo nodo
        z.left = self.NIL             # Inicializa hijos con NIL
        z.right = self.NIL
        z.parent = self.NIL
        z.color = RED                  # Nuevo nodo es rojo
        z.size = 1

        y = self.NIL
        x = self.root
        while x != self.NIL:
            y = x
            x.size += 1               # Incrementa tamaño mientras recorre el árbol
            if key < x.key:
                x = x.left          # Avanza a la izquierda
            else:
                x = x.right         # Avanza a la derecha

        z.parent = y
        if y == self.NIL:
            self.root = z           # Si el árbol está vacío, z es la raíz
        elif key < y.key:
            y.left = z              # Inserta z a la izquierda
        else:
            y.right = z             # Inserta z a la derecha

        self.rb_insert_fixup(z)     # Corrige propiedades rojo-negro

    # Ajusta el árbol después de la inserción para mantener sus propiedades
    def rb_insert_fixup(self, z):
        while z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.left_rotate(z.parent.parent)
        self.root.color = BLACK    # Asegura que la raíz sea negra

    # Busca y retorna el nodo con la clave dada (o NIL si no existe)
    def search_node(self, key):
        x = self.root
        while x != self.NIL and x.key != key:
            if key < x.key:
                x = x.left         # Sigue a la izquierda
            else:
                x = x.right        # Sigue a la derecha
        return x

    # Retorna el nodo si se encuentra, sino None
    def search(self, key):
        node = self.search_node(key)
        return node if node != self.NIL else None

    # Recorrido in-order auxiliar que retorna una lista de claves
    def inorder_helper(self, node):
        if node == self.NIL:
            return []
        return self.inorder_helper(node.left) + [node.key] + self.inorder_helper(node.right)

    # Recorrido in-order del árbol completo
    def inorder(self):
        return self.inorder_helper(self.root)

    # Encuentra el nodo mínimo (más a la izquierda) en el subárbol
    def minimum(self, x):
        while x.left != self.NIL:
            x = x.left
        return x

    # Reemplaza el subárbol u por v
    def rb_transplant(self, u, v):
        if u.parent == self.NIL:
            self.root = v        # Si u es la raíz, v se convierte en raíz
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent      # Actualiza el padre de v

    # Elimina el nodo con la clave dada y reequilibra el árbol
    def delete(self, key):
        z = self.search_node(key)
        if z == self.NIL:
            return             # No existe la clave, termina

        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
            y.size = y.left.size + y.right.size + 1

        # Actualiza el tamaño desde x hacia la raíz
        node = x.parent
        while node != self.NIL:
            node.size = node.left.size + node.right.size + 1
            node = node.parent

        if y_original_color == BLACK:
            self.rb_delete_fixup(x)

    # Ajusta el árbol después de la eliminación para mantener propiedades rojo-negro
    def rb_delete_fixup(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    # Auxiliar para obtener el k-ésimo elemento mayor usando tamaños
    def kth_largest_helper(self, node, k):
        if node == self.NIL:
            return None
        right_size = node.right.size
        if k == right_size + 1:
            return node.key
        elif k <= right_size:
            return self.kth_largest_helper(node.right, k)
        else:
            return self.kth_largest_helper(node.left, k - right_size - 1)

    # Retorna el k-ésimo elemento mayor del árbol
    def kth_largest(self, k):
        return self.kth_largest_helper(self.root, k)

    # Auxiliar para obtener las claves en el rango [a, b]
    def range_query_helper(self, node, a, b):
        if node == self.NIL:
            return []
        result = []
        if a < node.key:
            result.extend(self.range_query_helper(node.left, a, b))
        if a <= node.key <= b:
            result.append(node.key)
        if node.key < b:
            result.extend(self.range_query_helper(node.right, a, b))
        return result

    # Retorna una lista de claves que se encuentran en el rango [a, b]
    def range_query(self, a, b):
        return self.range_query_helper(self.root, a, b)

# Bloque principal para probar el Árbol Rojo-Negro
if __name__ == "__main__":
    tree = RedBlackTree()
    claves = [20, 4, 15, 70, 50, 100, 3, 10]
    for clave in claves:
        tree.insert(clave)  # Inserta cada clave en el árbol

    print("Inorder (orden creciente):", tree.inorder())

    clave_buscar = 15
    nodo = tree.search(clave_buscar)
    print(f"Buscando {clave_buscar}: {'Encontrado' if nodo else 'No encontrado'}")

    tree.delete(15)  # Elimina la clave 15 del árbol
    print("Inorder después de eliminar 15:", tree.inorder())

    k = 3
    kth = tree.kth_largest(k)
    print(f"El {k}-ésimo elemento mayor es:", kth)

    a, b = 10, 70
    print(f"Elementos en el rango [{a}, {b}]:", tree.range_query(a, b))

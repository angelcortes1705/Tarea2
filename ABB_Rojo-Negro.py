RED = "RED"
BLACK = "BLACK"

class RBNode:
    def __init__(self, key, color=RED, left=None, right=None, parent=None, size=1):
        self.key = key
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent
        self.size = size

class RedBlackTree:
    def __init__(self):
        self.NIL = RBNode(key=None, color=BLACK, size=0)
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL
        self.root = self.NIL

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

        y.size = x.size
        x.size = x.left.size + x.right.size + 1

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

        x.size = y.size
        y.size = y.left.size + y.right.size + 1

    def insert(self, key):
        z = RBNode(key)
        z.left = self.NIL
        z.right = self.NIL
        z.parent = self.NIL
        z.color = RED
        z.size = 1

        y = self.NIL
        x = self.root
        while x != self.NIL:
            y = x
            x.size += 1
            if key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y == self.NIL:
            self.root = z
        elif key < y.key:
            y.left = z
        else:
            y.right = z

        self.rb_insert_fixup(z)

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
        self.root.color = BLACK

    def search_node(self, key):
        x = self.root
        while x != self.NIL and x.key != key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def search(self, key):
        node = self.search_node(key)
        return node if node != self.NIL else None

    def inorder_helper(self, node):
        if node == self.NIL:
            return []
        return self.inorder_helper(node.left) + [node.key] + self.inorder_helper(node.right)

    def inorder(self):
        return self.inorder_helper(self.root)

    def minimum(self, x):
        while x.left != self.NIL:
            x = x.left
        return x

    def rb_transplant(self, u, v):
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete(self, key):
        z = self.search_node(key)
        if z == self.NIL:
            return

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

        node = x.parent
        while node != self.NIL:
            node.size = node.left.size + node.right.size + 1
            node = node.parent

        if y_original_color == BLACK:
            self.rb_delete_fixup(x)

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

    def kth_largest(self, k):
        return self.kth_largest_helper(self.root, k)

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

    def range_query(self, a, b):
        return self.range_query_helper(self.root, a, b)

if __name__ == "__main__":
    tree = RedBlackTree()
    claves = [20, 4, 15, 70, 50, 100, 3, 10]
    for clave in claves:
        tree.insert(clave)

    print("Inorder (orden creciente):", tree.inorder())

    clave_buscar = 15
    nodo = tree.search(clave_buscar)
    print(f"Buscando {clave_buscar}: {'Encontrado' if nodo else 'No encontrado'}")

    tree.delete(15)
    print("Inorder después de eliminar 15:", tree.inorder())

    k = 3
    kth = tree.kth_largest(k)
    print(f"El {k}-ésimo elemento mayor es:", kth)

    a, b = 10, 70
    print(f"Elementos en el rango [{a}, {b}]:", tree.range_query(a, b))

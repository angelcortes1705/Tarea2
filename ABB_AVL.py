# Clase para definir un nodo del árbol AVL
class AVLNode:
    def __init__(self, key):
        self.key = key            # Valor o clave del nodo
        self.left = None          # Hijo izquierdo
        self.right = None         # Hijo derecho
        self.height = 1           # Altura del nodo (inicialmente 1)
        self.size = 1             # Tamaño del subárbol (inicialmente 1)

# Función para obtener la altura de un nodo
def height(node):
    return node.height if node else 0

# Función para obtener el tamaño de un nodo
def size(node):
    return node.size if node else 0

# Actualiza la altura y tamaño del nodo según sus hijos
def update(node):
    if node:
        node.height = 1 + max(height(node.left), height(node.right))
        node.size = 1 + size(node.left) + size(node.right)

# Calcula el factor de balance del nodo
def get_balance(node):
    return height(node.left) - height(node.right) if node else 0

# Realiza una rotación derecha para reequilibrar el árbol
def right_rotate(y):
    x = y.left
    T2 = x.right

    x.right = y           # Mueve y como hijo derecho de x
    y.left = T2           # Asigna T2 como hijo izquierdo de y

    update(y)             # Actualiza alturas y tamaños
    update(x)
    return x

# Realiza una rotación izquierda para reequilibrar el árbol
def left_rotate(x):
    y = x.right
    T2 = y.left

    y.left = x            # Mueve x como hijo izquierdo de y
    x.right = T2          # Asigna T2 como hijo derecho de x

    update(x)             # Actualiza alturas y tamaños
    update(y)
    return y

# Inserta un nodo en el árbol AVL y reequilibra si es necesario
def insert(node, key):
    if node is None:
        return AVLNode(key)  # Crea y retorna un nuevo nodo si no existe

    if key < node.key:
        node.left = insert(node.left, key)  # Inserta a la izquierda
    else:
        node.right = insert(node.right, key)  # Inserta a la derecha

    update(node)             # Actualiza el nodo actual
    balance = get_balance(node)  # Calcula el balance

    # Casos de reequilibrio:
    if balance > 1 and key < node.left.key:
        return right_rotate(node)
    if balance < -1 and key > node.right.key:
        return left_rotate(node)
    if balance > 1 and key > node.left.key:
        node.left = left_rotate(node.left)
        return right_rotate(node)
    if balance < -1 and key < node.right.key:
        node.right = right_rotate(node.right)
        return left_rotate(node)

    return node

# Encuentra el nodo con el valor mínimo (más a la izquierda)
def min_value_node(node):
    current = node
    while current.left is not None:
        current = current.left
    return current

# Elimina un nodo del árbol AVL y reequilibra si es necesario
def delete(node, key):
    if node is None:
        return node

    if key < node.key:
        node.left = delete(node.left, key)  # Busca en el subárbol izquierdo
    elif key > node.key:
        node.right = delete(node.right, key)  # Busca en el subárbol derecho
    else:
        # Nodo a eliminar encontrado
        if node.left is None:
            temp = node.right
            node = None
            return temp
        elif node.right is None:
            temp = node.left
            node = None
            return temp
        temp = min_value_node(node.right)  # Encuentra el sucesor in-order
        node.key = temp.key                 # Reemplaza la clave
        node.right = delete(node.right, temp.key)  # Elimina el sucesor

    if node is None:
        return node

    update(node)                 # Actualiza el nodo
    balance = get_balance(node)  # Recalcula el balance

    # Casos de reequilibrio:
    if balance > 1 and get_balance(node.left) >= 0:
        return right_rotate(node)
    if balance > 1 and get_balance(node.left) < 0:
        node.left = left_rotate(node.left)
        return right_rotate(node)
    if balance < -1 and get_balance(node.right) <= 0:
        return left_rotate(node)
    if balance < -1 and get_balance(node.right) > 0:
        node.right = right_rotate(node.right)
        return left_rotate(node)

    return node

# Busca un nodo con una clave específica
def search(node, key):
    if node is None or node.key == key:
        return node
    if key < node.key:
        return search(node.left, key)
    else:
        return search(node.right, key)

# Realiza un recorrido in-order y retorna las claves en orden creciente
def inorder(node):
    return inorder(node.left) + [node.key] + inorder(node.right) if node else []

# Encuentra el k-ésimo elemento mayor usando tamaños de subárbol
def kth_largest(node, k):
    if node is None:
        return None
    right_size = size(node.right)
    if k == right_size + 1:
        return node.key
    elif k <= right_size:
        return kth_largest(node.right, k)
    else:
        return kth_largest(node.left, k - right_size - 1)

# Retorna una lista de claves dentro del rango [a, b]
def range_query(node, a, b):
    if node is None:
        return []
    result = []
    if a < node.key:
        result.extend(range_query(node.left, a, b))
    if a <= node.key <= b:
        result.append(node.key)
    if node.key < b:
        result.extend(range_query(node.right, a, b))
    return result

# Bloque principal para probar el árbol AVL
if __name__ == "__main__":
    root = None
    claves = [20, 4, 15, 70, 50, 100, 3, 10]
    # Inserta cada clave en el árbol AVL
    for clave in claves:
        root = insert(root, clave)

    print("Inorder (orden creciente):", inorder(root))

    # Busca el nodo con la clave 15
    clave_buscar = 15
    nodo = search(root, clave_buscar)
    print(f"Buscando {clave_buscar}: {'Encontrado' if nodo else 'No encontrado'}")

    # Elimina el nodo con la clave 15 y muestra el recorrido in-order
    root = delete(root, 15)
    print("Inorder después de eliminar 15:", inorder(root))

    # Obtiene el 3º elemento mayor del árbol
    k = 3
    kth = kth_largest(root, k)
    print(f"El {k}-ésimo elemento mayor es:", kth)

    # Realiza una consulta de rango entre 10 y 70
    a, b = 10, 70
    print(f"Elementos en el rango [{a}, {b}]:", range_query(root, a, b))

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        self.size = 1

def height(node):
    return node.height if node else 0

def size(node):
    return node.size if node else 0

def update(node):
    if node:
        node.height = 1 + max(height(node.left), height(node.right))
        node.size = 1 + size(node.left) + size(node.right)

def get_balance(node):
    return height(node.left) - height(node.right) if node else 0

def right_rotate(y):
    x = y.left
    T2 = x.right

    x.right = y
    y.left = T2

    update(y)
    update(x)
    return x

def left_rotate(x):
    y = x.right
    T2 = y.left

    y.left = x
    x.right = T2

    update(x)
    update(y)
    return y

def insert(node, key):
    if node is None:
        return AVLNode(key)
    
    if key < node.key:
        node.left = insert(node.left, key)
    else:
        node.right = insert(node.right, key)
    
    update(node)
    balance = get_balance(node)
    
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

def min_value_node(node):
    current = node
    while current.left is not None:
        current = current.left
    return current

def delete(node, key):
    if node is None:
        return node

    if key < node.key:
        node.left = delete(node.left, key)
    elif key > node.key:
        node.right = delete(node.right, key)
    else:

        if node.left is None:
            temp = node.right
            node = None
            return temp
        elif node.right is None:
            temp = node.left
            node = None
            return temp
        temp = min_value_node(node.right)
        node.key = temp.key
        node.right = delete(node.right, temp.key)

    if node is None:
        return node

    update(node)
    balance = get_balance(node)
    
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

def search(node, key):
    if node is None or node.key == key:
        return node
    if key < node.key:
        return search(node.left, key)
    else:
        return search(node.right, key)

def inorder(node):
    return inorder(node.left) + [node.key] + inorder(node.right) if node else []

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

if __name__ == "__main__":
    root = None
    claves = [20, 4, 15, 70, 50, 100, 3, 10]
    for clave in claves:
        root = insert(root, clave)

    print("Inorder (orden creciente):", inorder(root))

    clave_buscar = 15
    nodo = search(root, clave_buscar)
    print(f"Buscando {clave_buscar}: {'Encontrado' if nodo else 'No encontrado'}")

    root = delete(root, 15)
    print("Inorder después de eliminar 15:", inorder(root))

    k = 3
    kth = kth_largest(root, k)
    print(f"El {k}-ésimo elemento mayor es:", kth)

    a, b = 10, 70
    print(f"Elementos en el rango [{a}, {b}]:", range_query(root, a, b))

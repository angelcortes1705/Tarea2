import time
import random
import string

# Implementación de tabla hash con Encadenamiento (Chaining)
class ChainingHashTable:
    def __init__(self, size=10007):
        """Inicializa la tabla con listas vacías en cada índice."""
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, key):
        """Calcula el índice hash de la clave."""
        return hash(key) % self.size
    
    def insert(self, key, value):
        """Inserta un par clave-valor en la tabla usando encadenamiento."""
        index = self._hash(key)
        # Busca si la clave ya existe para actualizar el valor
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        # Si no existe, se agrega a la lista
        self.table[index].append([key, value])
    
    def search(self, key):
        """Busca una clave en la tabla y devuelve su valor, o None si no existe."""
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]  # Retorna el valor si encuentra la clave
        return None
    
    def delete(self, key):
        """Elimina una clave de la tabla, si existe."""
        index = self._hash(key)
        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                del self.table[index][i]  # Elimina la clave de la lista
                return True
        return False  # Retorna False si no se encontró

# Implementación de tabla hash con Direccionamiento Abierto (Open Addressing)
class OpenAddressingHashTable:
    def __init__(self, size=10007):
        """Inicializa la tabla con espacios vacíos (None)."""
        self.size = size
        self.table = [None] * size
    
    def _hash(self, key):
        """Calcula el índice hash de la clave."""
        return hash(key) % self.size
    
    def insert(self, key, value):
        """Inserta un par clave-valor usando sondeo lineal para manejar colisiones."""
        index = self._hash(key)
        original_index = index  # Guarda el índice original para detectar ciclos
        while self.table[index] is not None:
            if self.table[index][0] == key:  # Si la clave ya existe, se actualiza
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.size  # Sondeo lineal
            if index == original_index:
                raise Exception("Hash table is full")  # La tabla está llena
        self.table[index] = (key, value)
    
    def search(self, key):
        """Busca una clave y devuelve su valor si existe, o None si no está."""
        index = self._hash(key)
        original_index = index
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]  # Retorna el valor si lo encuentra
            index = (index + 1) % self.size  # Sondeo lineal
            if index == original_index:
                break
        return None
    
    def delete(self, key):
        """Elimina una clave si existe, marcando el espacio como vacío."""
        index = self._hash(key)
        original_index = index
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = None  # Se elimina la clave
                return True
            index = (index + 1) % self.size
            if index == original_index:
                break
        return False

# Función para generar claves aleatorias
def generate_random_key(length=8):
    """Genera una clave alfanumérica aleatoria."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Función para medir rendimiento de inserción, búsqueda y eliminación
def benchmark(hash_table_class, num_elements=10000):
    hash_table = hash_table_class()
    keys = [generate_random_key() for _ in range(num_elements)]
    values = [random.randint(1, 100000) for _ in range(num_elements)]
    
    # Medir tiempo de inserción
    start_time = time.time()
    for i in range(num_elements):
        hash_table.insert(keys[i], values[i])
    insertion_time = time.time() - start_time
    
    # Medir tiempo de búsqueda
    start_time = time.time()
    found = sum(1 for i in range(num_elements // 2) if hash_table.search(keys[i]) is not None)
    search_time = time.time() - start_time
    
    # Medir tiempo de eliminación
    start_time = time.time()
    deleted = sum(1 for i in range(num_elements // 2) if hash_table.delete(keys[i]))
    deletion_time = time.time() - start_time
    
    return insertion_time, search_time, deletion_time, found, deleted

# Ejecución de pruebas
if __name__ == "__main__":
    print("Chaining Hash Table")
    chain_times = benchmark(ChainingHashTable)
    print(f"Insertion Time: {chain_times[0]:.4f}s, Search Time: {chain_times[1]:.4f}s, Deletion Time: {chain_times[2]:.4f}s")

    print("\nOpen Addressing Hash Table")
    open_times = benchmark(OpenAddressingHashTable)
    print(f"Insertion Time: {open_times[0]:.4f}s, Search Time: {open_times[1]:.4f}s, Deletion Time: {open_times[2]:.4f}s")

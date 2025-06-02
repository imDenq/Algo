class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

def get_height(n):
    return n.height if n else 0

def update_height(n):
    n.height = 1 + max(get_height(n.left), get_height(n.right))

def get_balance(n):
    return get_height(n.left) - get_height(n.right) if n else 0

def rotate_right(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    update_height(y)
    update_height(x)
    return x

def rotate_left(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    update_height(x)
    update_height(y)
    return y

def insert(root, key):
    if not root:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    update_height(root)
    balance = get_balance(root)
    if balance > 1 and key < root.left.key:
        return rotate_right(root)
    if balance < -1 and key > root.right.key:
        return rotate_left(root)
    if balance > 1 and key > root.left.key:
        root.left = rotate_left(root.left)
        return rotate_right(root)
    if balance < -1 and key < root.right.key:
        root.right = rotate_right(root.right)
        return rotate_left(root)
    return root

def min_value_node(n):
    current = n
    while current.left:
        current = current.left
    return current

def delete(root, key):
    if not root:
        return root
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        if not root.left:
            return root.right
        elif not root.right:
            return root.left
        temp = min_value_node(root.right)
        root.key = temp.key
        root.right = delete(root.right, temp.key)
    update_height(root)
    balance = get_balance(root)
    if balance > 1 and get_balance(root.left) >= 0:
        return rotate_right(root)
    if balance > 1 and get_balance(root.left) < 0:
        root.left = rotate_left(root.left)
        return rotate_right(root)
    if balance < -1 and get_balance(root.right) <= 0:
        return rotate_left(root)
    if balance < -1 and get_balance(root.right) > 0:
        root.right = rotate_right(root.right)
        return rotate_left(root)
    return root

def inorder(root, result):
    if root:
        inorder(root.left, result)
        result.append((root.key, root.height))
        inorder(root.right, result)
    return result

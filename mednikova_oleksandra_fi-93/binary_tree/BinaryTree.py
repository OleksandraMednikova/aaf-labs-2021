class BinaryNode:
    def __init__(self, value=None, data=None):
        self.value = value
        self.data = data 
        self.left = None
        self.right = None
        self.height = 0
    
    def compute_height(self):
        height = -1
        if self.left:
            height = max(height, self.left.height)
        if self.right:
            height = max(height, self.right.height)
        
        self.height = height + 1

    def height_difference(self):
        left_target = 0
        right_target = 0
        if self.left:
            left_target = self.left.height + 1
        if self.right:
            right_target = self.right.height + 1
        return left_target - right_target
    
    def add_to_subtree(self, parent, value, data):
        if parent is None:
            return BinaryNode(value, data)
        
        parent = parent.add(value, data)
        return parent

    def rotate_right(self):
        new_root = self.left
        grandson = new_root.right
        self.left = grandson
        new_root.right = self

        self.compute_height()
        return new_root

    def rotate_left(self):
        new_root = self.right
        grandson = new_root.left
        self.right = grandson
        new_root.left = self

        self.compute_height()
        return new_root

    def rotate_right_left(self):
        child = self.right
        new_root = child.left
        grand1 = new_root.left
        grand2 = new_root.right
        child.left = grand2
        self.right = grand1

        new_root.left = self
        new_root.right = child

        child.compute_height()
        self.compute_height()
        return new_root

    def rotate_left_right(self):
        child = self.left
        new_root = child.right
        grand1 = new_root.left
        grand2 = new_root.right
        child.right = grand1
        self.left = grand2

        new_root.left = child
        new_root.right = self

        child.compute_height()
        self.compute_height()
        return new_root

    def add(self, value, data):
        new_root = self
        if value <= self.value:
            self.left = self.add_to_subtree(self.left, value, data)
            if self.height_difference() == 2:
                if value <= self.left.value:
                    new_root = self.rotate_right()
                else: 
                    new_root = self.rotate_left_right()
        else:
            self.right = self.add_to_subtree(self.right, value, data)
            if self.height_difference() == -2:
                if value >= self.right.value:
                    new_root = self.rotate_left()
                else: 
                    new_root = self.rotate_right_left()
        
        new_root.compute_height()
        return new_root

    def remove_from_parent(self, parent, value):
        if parent:
            return parent.remove(value)
        return None

    def remove(self, value):
        new_root = self
        if value == self.value:
            if self.left is None:
                return self.right

            child = self.left
            while child.right:
                child = child.right

            child_key = child.value
            self.left = self.remove_from_parent(self.left, child_key)
            self.value = child_key

            if self.height_difference() == -2:
                if self.right.height_difference() <= 0:
                    new_root = self.rotate_left()
                else:
                    new_root = self.rotate_right_left()

        elif value < self.value:
            self.left = self.remove_from_parent(self.left, value)
            if self.height_difference() == -2:
                if self.right.height_difference() <= 0:
                    new_root = self.rotate_left()
                else:
                    new_root = self.rotate_right_left()
        
        else:
            self.right = self.remove_from_parent(self.right, value)
            if self.height_difference() == 2:
                if self.left.height_difference() >= 0:
                    new_root = self.rotate_right()
                else:
                    new_root = self.rotate_left_right()
        
        new_root.compute_height()
        return new_root

    def inorder(self):
        if self.left:
            for n in self.left.inorder():
                yield n
        
        yield self.value, self.data

        if self.right:
            for n in self.right.inorder():
                yield n       

class BinaryTree:
    def __init__(self):
        self.root = None

    def __iter__(self):
        if self.root:
            return self.root.inorder()
    
    def __contains__(self, target):
        node = self.root
        while node:
            if target < node.value:
                node = node.left
            elif target > node.value:
                node = node.right
            else:
                return True
        return False 
    
    def add(self, value, data):
        if self.root is None:
            self.root = BinaryNode(value, data)
        else:
            self.root = self.root.add(value, data)

    def get(self, target):
        node = self.root
        while node:
            if target < node.value:
                node = node.left
            elif target > node.value:
                node = node.right
            elif target == node.value:
                return node
        return None

    def interval_search(self, less, more, ids, target = None):
        node = target
        while node:
            if node.value < less:
                node = node.right
            elif node.value > more:
                node = node.left
            else:
                ids.update(node.data.keys())
                self.interval_search(less, more, ids, node.left)
                self.interval_search(less, more, ids, node.right)
                node = None


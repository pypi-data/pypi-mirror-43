class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def inorderUtil(self, root):
        if root:
            self.inorderUtil(root.left)
            self.result += str(root.val)+' '
            self.inorderUtil(root.right)
    
    def inorder(self):
        self.result = ''
        self.inorderUtil(self.root)
        return self.result
    
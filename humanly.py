import os

from yaml import scan
print(os.environ)

list_ = []
while True:
    scan_result = scan(os.environ)
    list_.append(scan_result)

    print(scan_result)

# This file will be able to only be done manually because it is programmed by a real programmer
class Node:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.parent = None
        if self.left:
            self.left.parent = self
        if self.right:
            self.right.parent = self
    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return self.left is None and self.right is None     
    def has_children(self):
        return self.left is not None or self.right is not None
    def is_only_child(self):
        return self.parent and ((self.parent.left is self and self.parent.right is None) or (self.parent.right is self and self.parent.left is None))   
class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.childrenNames = []

    def __repr__(self):
        return f"Node(name='{self.name}', parent='{self.parent.name if self.parent else None}')"

    def getChild(self, name):
        for child in self.children:
            if child.name == name:
                return child
        return None

import base64

class Node:
    def __init__(self, name, parent=None, node_type='folder', content=None):
        self.name = name
        self.parent = parent
        self.type = node_type  # 'folder' или 'file'
        self.content = content  # строка base64 или None
        self.children = []
        self.childrenNames = []

    def __repr__(self):
        return f"Node(name='{self.name}', type='{self.type}', parent='{self.parent.name if self.parent else None}')"

    def getChild(self, name):
        for child in self.children:
            if child.name == name:
                return child
        return None

    def readContent(self, reverse=False):
        if self.type == 'file' and self.content:
            result = base64.b64decode(self.content).decode('utf-8')
            if not reverse:
                return result
            else:
                return "\n".join(result.split('\n')[::-1])

        return None

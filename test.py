import json
import base64


class Node:
    def __init__(self, name, parent=None, node_type='folder', content=None):
        self.name = name
        self.parent = parent
        self.type = node_type  # 'folder' или 'file'
        self.content = content  # строка base64 или None
        self.children = []

    def __repr__(self):
        return f"Node(name='{self.name}', type='{self.type}', parent='{self.parent.name if self.parent else None}')"

    def get_content_as_text(self):
        if self.type == 'file' and self.content:
            return base64.b64decode(self.content).decode('utf-8')
        return None


class VfsBuilder:
    def __init__(self, filepath):
        self.filepath = filepath
        self.root = None

    def _build_tree_from_json(self, data, parent=None):
        node_type = data.get('type', 'folder')
        content = data.get('content', None)
        node = Node(data['name'], parent, node_type, content)

        if node_type == 'folder':
            for child_data in data.get('children', []):
                child_node = self._build_tree_from_json(child_data, node)
                node.children.append(child_node)

        return node

    def _flatten_tree_to_array(self, node, result_array):
        result_array.append(node)
        for child in node.children:
            self._flatten_tree_to_array(child, result_array)

    def build(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.root = self._build_tree_from_json(data)
        nodes_array = []
        self._flatten_tree_to_array(self.root, nodes_array)
        return nodes_array


# Пример использования
if __name__ == "__main__":
    builder = VfsBuilder('filesystem.json')
    nodes = builder.build()

    for node in nodes:
        if node.type == 'file':
            print(f"File: {node.name}")
            print("Content:", node.get_content_as_text())
        else:
            print(f"Folder: {node.name}")
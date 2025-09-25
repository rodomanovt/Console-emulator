import json
from Node import *


class VFSBuilder:
    def __init__(self, filepath):
        self._filepath = filepath
        with open(self._filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self._root = self._build_tree_from_json(data)

    def _build_tree_from_json(self, data, parent=None):
        node_type = data.get('type', 'folder')
        content = data.get('content', None)
        node = Node(data['name'], parent, node_type, content)

        if node_type == 'folder':
            for child_data in data.get('children', []):
                child_node = self._build_tree_from_json(child_data, node)
                node.children.append(child_node)
                node.childrenNames.append(child_node.name)

        return node


    def getRoot(self):
        return self._root


if __name__ == "__main__":
    builder = VFSBuilder('vfs.json')

    root = builder.getRoot()
    print(root.children[0])

    # for node in nodes:
    #     print(node)
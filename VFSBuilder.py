import json
from Node import *


class VFSBuilder:
    def __init__(self, filepath):
        self._filepath = filepath
        with open(self._filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self._root = self._build_tree_from_json(data)

    def _build_tree_from_json(self, data, parent=None):
        node = Node(data['name'], parent)
        for child_data in data.get('children', []):
            child_node = self._build_tree_from_json(child_data, node)
            node.children.append(child_node)
            node.childrenNames.append(child_node.name)
        return node


    def _flatten_tree_to_array(self, node, result_array):
        result_array.append(node)
        for child in node.children:
            self._flatten_tree_to_array(child, result_array)


    def getRoot(self):
        return self._root


    def getAllNodes(self):
        nodes_array = []
        self._flatten_tree_to_array(self._root, nodes_array)
        return nodes_array


# Пример использования
if __name__ == "__main__":
    builder = VFSBuilder('vfs.json')
    nodes = builder.getAllNodes()

    root = builder.getRoot()
    print(root.children[0])

    # for node in nodes:
    #     print(node)
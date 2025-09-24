import json
from Node import *



def build_tree_from_json(data, parent=None):
    # Создаём узел
    node = Node(data['name'], parent)

    # Обрабатываем дочерние элементы
    for child_data in data.get('children', []):
        child_node = build_tree_from_json(child_data, node)
        node.children.append(child_node)

    return node


def flatten_tree_to_array(node, result_array):
    result_array.append(node)
    for child in node.children:
        flatten_tree_to_array(child, result_array)


def load_and_parse_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    root = build_tree_from_json(data)
    nodes_array = []
    flatten_tree_to_array(root, nodes_array)

    return nodes_array


# Пример использования
if __name__ == "__main__":
    # Загрузка из файла
    filepath = 'vfs.json'  # Укажите путь к вашему JSON-файлу
    nodes = load_and_parse_json_file(filepath)

    # Вывод всех узлов
    for node in nodes:
        print(node)
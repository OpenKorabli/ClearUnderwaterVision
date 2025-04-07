import os
import xml.etree.ElementTree as Et
from pathlib import Path
from typing import List


def is_number(text: str) -> bool:
    """简单判断字符串是否为数字（整数/浮点数等）。"""
    if text is None:
        return False
    text = text.strip()
    if not text:
        return False
    try:
        float(text)
        return True
    except ValueError:
        return False


def update_values(elem_a: Et.Element, elem_b: Et.Element, changes: List):
    """
    递归地比较并更新 elem_a 中的数字值，若 elem_b 的同位置值也是数字则替换。
    假设 A、B 文件在对应位置存在相同的元素结构。
    """
    # 如果两者都有文本，并且都是数字，则替换 A 的文本
    if elem_a.text and elem_b.text and is_number(elem_a.text) and is_number(elem_b.text):
        old_value = elem_a.text.strip()
        new_value = elem_b.text.strip()
        # 只有在新旧值不相同的时候才算“发生变化”
        if old_value != new_value:
            # 记录变化信息
            changes.append({
                "element_name": elem_a.tag,
                "old_value": old_value,
                "new_value": new_value
            })
            # 在文件 A 中替换掉旧值
            elem_a.text = new_value
        # elem_a.text = elem_b.text

    # 如果有子节点，递归对子节点做同样的处理
    children_a = list(elem_a)
    children_b = list(elem_b)

    # 这里假设文件 A 和 B 的子节点顺序相同
    for child_a, child_b in zip(children_a, children_b):
        update_values(child_a, child_b)


def main(file_a_path: str, file_b_path: str, output_path: str):
    # 解析文件A和文件B
    tree_a = Et.parse(file_a_path)
    root_a = tree_a.getroot()

    tree_b = Et.parse(file_b_path)
    root_b = tree_b.getroot()
    changes = []
    # 更新 A 的元素值
    update_values(root_a, root_b, changes)
    os.makedirs(Path(output_path).parent, exist_ok=True)
    # 写出修改后的文件 A
    tree_a.write(output_path, encoding='utf-8')


if __name__ == "__main__":
    for root, dirs, files in os.walk('ports$'):
        for filename in files:
            if filename != 'space.ubersettings':
                continue
            file_o_path = os.path.join(root, filename)
            file_m_path = file_o_path.replace('ports$', 'ports$_m')
            if not Path(file_m_path).is_file():
                continue
            main(file_o_path, file_m_path, file_m_path.replace('ports$_m', 'ports$_e'))


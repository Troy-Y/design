import json
import os

def json_sort(path):
    # 读取JSON文件
    with open(path, "r") as f:
        data = json.load(f)

    # 对cells进行排序
    sorted_cells = sorted(data['cells'], key=lambda x: (x['src'], x['dest']))

    # 更新data中的cells
    data["cells"] = sorted_cells

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

root_dir = '../data/depends_output_json'
num = 0
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        old = dirpath + '\old.json'
        new = dirpath + '\\new.json'
        # print(old)
        # print(new)
        json_sort(old)
        json_sort(new)

        num += 1
print(num)


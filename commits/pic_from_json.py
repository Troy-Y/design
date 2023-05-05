import json
import os

path_pic = '../data/pic_from_diff'

def pic(path):
    # 读取原始json文件
    data = {}
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except:
            pass
    if not data:
        return

    # 添加节点
    node_list = []
    for var in data['variables']:
        node_list.append(var)

    # 添加边
    edge_list = []
    for cell in data['cells']:
        src_file = data['variables'][cell['src']]
        dest_file = data['variables'][cell['dest']]
        edge_dict = {'source': src_file, 'target': dest_file, 'label': ''}
        for key, value in cell['values'].items():
            edge_dict['label'] += f"{key}: {value}, "
        edge_list.append(edge_dict)

    # 更新边的权重值
    for edge in edge_list:
        for cell in data['cells']:
            src_file = data['variables'][cell['src']]
            dest_file = data['variables'][cell['dest']]
            if edge['source'] == src_file and edge['target'] == dest_file:
                for key, value in cell['values'].items():
                    edge[key] = value

    # 将节点和边保存到新的 JSON 文件中
    output_data = {'nodes': node_list, 'edges': edge_list}

    f_pic = path_pic + '/' + os.path.basename(os.path.dirname(path))
    if not os.path.exists(f_pic):
        os.makedirs(f_pic)
    f_pic = f_pic + '/' + os.path.basename(path)
    with open(f_pic, 'w') as f:
        json.dump(output_data, f, indent=4)


root_dir = '../data/depends_output_json'

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        old = dirpath + '/old.json'
        new = dirpath + '/new.json'
        # print(old)
        # print(new)
        # print(os.path.basename(dirpath))
        # print(os.path.basename(old))
        cmt = os.path.basename(dirpath)
        pic(old)
        pic(new)
        break
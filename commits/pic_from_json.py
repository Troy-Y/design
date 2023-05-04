import json
import os
import networkx as nx

def pic(path,cmt):
    # 读取JSON文件
    data = {}
    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except:
            pass

    if not data:
        return

    # 创建一个有向图
    G = nx.DiGraph()

    # 添加节点
    for node in data['variables']:
        G.add_node(node)

    # 添加边
    for cell in data['cells']:
        src = data['variables'][cell['src']]
        dest = data['variables'][cell['dest']]
        values = cell['values']
        for key, value in values.items():
            if value > 0:
                G.add_edge(src, dest, label=key, weight=value)

    # 将图保存为JSON文件
    graph_data = nx.readwrite.json_graph.node_link_data(G)

    pic_path = '../data/pic_from_diff/' + cmt
    if not os.path.exists(pic_path):
        os.makedirs(pic_path)
    f_old = pic_path + '/' + os.path.basename(path)
    fo = open(f_old,'w')
    json.dump(graph_data, fo, indent=2)


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
        pic(old,cmt)
        pic(new,cmt)
        break

import json
import os

import networkx as nx
import matplotlib.pyplot as plt

pic_path = '../data/pic_from_diff/'
scc_path = '../data/scc/'

def scc(path):
    # 读取 JSON 数据
    with open(path, "r") as f:
        data = json.load(f)

    # 创建有向图
    G = nx.DiGraph()

    # 添加节点
    G.add_nodes_from(data['nodes'])

    # 添加边
    for edge in data['edges']:
        source = edge['source']
        target = edge['target']
        weight = edge['Extend'] if 'Extend' in edge else 1.0  # 从 JSON 数据中获取边的权重
        G.add_edge(source, target, weight=weight)



    # 计算强连通分量
    scc = nx.strongly_connected_components(G)
    i = 1

    for line in list(scc):
        if len(line) > 1:
            s = scc_path + os.path.basename(os.path.dirname(path))
            # print(s)

            if not os.path.exists(s):
                os.makedirs(s)

            s = s + '/' + os.path.basename(path)
            basename, extension = os.path.splitext(s)
            s = basename + '.txt'
            with open(s,'a') as f:  # 'a'继续输入
                print(i,file = f)
                i = i + 1
                for l in line:
                    print(l,file = f)

for item in os.listdir(pic_path):
    json_old = pic_path + item + '/old.json'
    json_new = pic_path + item + '/new.json'
    # print(json_old)
    # print(json_new)
    if os.path.isfile(json_old):
        scc(json_old)
    if os.path.isfile(json_new):
        scc(json_new)
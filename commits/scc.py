import json
import os
import networkx as nx

pic_path = '../data/pic_from_diff/'
scc_path = '../data/scc/'

# 查找强连通分量
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

# 格式化json文件
def format_scc(file_path):
    with open(file_path, 'r+') as file:
        # 逐行读取文件
        lines = file.readlines()

        # 逐行处理
        for i in range(len(lines)):
            # 如果是数字行，跳过
            if lines[i].isdigit():
                continue

            # 提取文件路径和文件名
            path, filename = os.path.split(lines[i].strip())
            fname, ext = os.path.splitext(lines[i])

            # 修改文件名
            new_filename = filename.split('.')[0] + ext
            lines[i] = os.path.join(path, new_filename) + '\n'

        # 将修改后的内容写回文件
        file.seek(0)
        file.writelines(lines)
        file.truncate()

# 去掉空行
def clean_txt(file_path):
    with open(file_path, 'r') as file:
        # 读取文件内容
        content = file.read()

    # 清除空行
    new_content = "\n".join([line for line in content.splitlines() if line.strip()])

    # 将新内容写回文件
    with open(file_path, 'w') as file:
        file.write(new_content)

# 找出所有json文件的强连通分量
for item in os.listdir(pic_path):
    json_old = pic_path + item + '/old.json'
    json_new = pic_path + item + '/new.json'
    # print(json_old)
    # print(json_new)
    if os.path.isfile(json_old):
        scc(json_old)
    if os.path.isfile(json_new):
        scc(json_new)

# 由于depends输出的所有new.json文件中所有路径的文件名都有显示bug，在此进行解决。
for item in os.listdir(scc_path):
    scc_file_path = scc_path + item + '/new.txt'
    # print(scc)
    if os.path.isfile(scc_file_path):
        with open(scc_file_path, 'r+') as file:
            format_scc(scc_file_path)

# 为后续比较方便，去掉所有空行
for item in os.listdir(scc_path):
    s_old = scc_path + item + '/old.txt'
    s_new = scc_path + item + '/new.txt'
    if os.path.isfile(s_old):
        clean_txt(s_old)
    if os.path.isfile(s_new):
        clean_txt(s_new)
import json
import os
import shutil
import networkx as nx
from pydriller import Repository
import json
from jsondiff import diff

url = r'D:\desktop\myrepo\cassandra'
json_path = r'D:\PythonProject\design_cassandra\data_copy\depends_json'
json_caused_change_path = r'D:\PythonProject\design_cassandra\data_copy\json_caused_change'

def get_scc_list(json_path):
    with open(json_path,'r') as f:
        data = json.load(f)

    # 创建有向图
    G = nx.DiGraph()

    # 添加节点
    G.add_nodes_from(data['variables'])
    # print(G.nodes)

    # 添加边
    for edge in data['cells']:
        source = edge['src']
        target = edge['dest']
        label = edge['values']
        G.add_edge(source, target, label=label)
        # print(edge)

    # 计算强连通分量
    sccs = nx.strongly_connected_components(G)

    files_latest_scc = []

    for scc in sccs:
        if len(scc) > 2:
            # print(scc)
            node_names = [list(G.nodes())[i] for i in scc]
            for name in node_names:
                files_latest_scc.append(name[name.index('src\java'):])
            break

    return files_latest_scc



cmts_list = []

for cmt in Repository(url).traverse_commits():
    cmts_list.append(cmt)

# 按时间从近到远排序
cmts_list = list(reversed(cmts_list))

cmt_may_caused_change = []

with open('../data_copy/cmt_may_caused_change.txt','r') as f:
    for line in f:
        cmt_may_caused_change.append(line.strip())

# for cmt in cmt_may_caused_change:
#     print(cmt)

files_latest_scc = get_scc_list(os.path.join(json_caused_change_path,cmts_list[0].hash + '.json'))

# for f in files_latest_scc:
#     print(f)

files_latest_scc_copy = files_latest_scc
cmt_copy = cmts_list[0].hash
# print(cmt_copy)

json_latest_path = os.path.join('../data_copy/depends_json',cmts_list[0].hash + '.json')

with open(json_latest_path,'r') as f:
    json_latest = json.load(f)
json_now = json_latest

for cmt in cmts_list:
    if cmt.hash in cmt_may_caused_change:
        # print(cmt.hash)
        scc_path = os.path.join(json_path, cmt.hash) + '.json'
        scc_list= get_scc_list(scc_path)
        if set(scc_list) != set(files_latest_scc_copy):
            if cmt.hash == cmts_list[len(cmts_list) - 1].hash:
                print('依赖关系在最初创建时就已存在。')
            else:
                print(f'{cmt.hash}引起了依赖关系的改变。')

            # 输出cmt前后文件
            # print(f'{cmt.hash}后有{len(files_latest_scc_copy)}个文件，为：')
            # for f in files_latest_scc_copy:
            #     print(f)
            #
            # print(f'{cmt.hash}前有{len(scc_list)}个文件，为：')
            # for f in scc_list:
            #     print(f)

            old_json_path =  os.path.join(json_path,cmt.hash + '.json')
            new_json_path = os.path.join(json_caused_change_path,cmt.hash + '.json')
            with open(new_json_path,'w') as f:
                shutil.copy(old_json_path, new_json_path)
            if (len(scc_list) > len(files_latest_scc_copy)):
                print('本次commit后下列文件不存在于循环依赖文件组中：')
                diff = set(scc_list) - set(files_latest_scc_copy)
                i = 1
                for f in diff:
                    print(i,end='.')
                    print(f)
                    i += 1
            elif (len(scc_list) < len(files_latest_scc_copy)):
                print('本次commit后循环依赖文件组中新增了下列文件：')
                diff = set(files_latest_scc_copy) - set(scc_list)
                i = 1
                for f in diff:
                    print(i, end='.')
                    print(f)
                    i += 1
            else:
                print('本次commit后下列文件不存在于循环依赖文件组中：')
                diff1 = set(scc_list) - set(files_latest_scc_copy)
                i = 1
                for f in diff1:
                    print(i, end='.')
                    print(f)
                    i += 1
                print('本次commit后循环依赖文件组中新增了下列文件：')
                diff2 = set(files_latest_scc_copy) - set(scc_list)
                i = 1
                for f in diff2:
                    print(i, end='.')
                    print(f)
                    i += 1

            print('')
            files_latest_scc_copy.clear()
            files_latest_scc_copy = scc_list
            # json1 = json_now
            # with open (old_json_path,'r') as f:
            #     json_now = json.load(f)
            # with open(old_json_path, 'r') as f:
            #     json2 = json.load(f)
            # rst = diff(json1,json2)
            # print(rst)

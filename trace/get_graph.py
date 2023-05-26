import json
import os.path
import networkx as nx
import matplotlib.pyplot as plt
from pydriller import Repository

url = r'D:\desktop\myrepo\cassandra'
json_change = '../data_copy/depends_json'


cmts_list = []

def get_rows_cols(a):
    min = 100
    x = 0
    y = 0
    max = 10
    while(max):
        for i in range(1, a):
            for j in range(1, a):
                if i * j == a and 0 < j - i and j - i < min:
                    x = i
                    y = j
                    min = j - i
        a += 1
        max -= 1
    return x,y

for cmt in Repository(url).traverse_commits():
    cmts_list.append(cmt)

# 找到第一个出现循环依赖的commit
first_json_cmt = cmts_list[0]

for cmt in cmts_list:
    if os.path.exists(os.path.join(json_change, cmt.hash + '.json')):
        first_json_cmt = cmt
        break

graph_before_path = os.path.join(json_change, first_json_cmt.hash + '.json')
# print(graph_before_path)

fig = plt.figure()
figManager = plt.get_current_fig_manager()
figManager.full_screen_toggle()

# 画出第一个引起循环依赖的图
with open(graph_before_path, 'r') as f:
    data_before = json.load(f)

    # 创建有向图
    graph_before = nx.DiGraph()

    # 添加边
    for edge in data_before['cells']:
        source = os.path.basename(data_before['variables'][edge['src']])
        target = os.path.basename(data_before['variables'][edge['dest']])
        label = edge['values']
        graph_before.add_edge(source, target, label=label)

graph_before_copy = graph_before

graph_num = 1
for cmt in cmts_list:
    if os.path.exists(os.path.join(json_change, cmt.hash + '.json')) and os.path.join(json_change,
                                                                                             cmt.hash + '.json') != graph_before_path:
        graph_after_path_copy = os.path.join(json_change, cmt.hash + '.json')

        with open(graph_after_path_copy, 'r') as f:
            data_after = json.load(f)

        # 画出要对比的图
        graph_after_copy = nx.DiGraph()
        for edge in data_after['cells']:
            source = os.path.basename(data_after['variables'][edge['src']])
            target = os.path.basename(data_after['variables'][edge['dest']])
            label = edge['values']
            graph_after_copy.add_edge(source, target, label=label)

        # 计算两个图的节点集和边集的差异
        nodes_added_copy = graph_after_copy.nodes() - graph_before_copy.nodes()
        nodes_removed_copy = graph_before_copy.nodes() - graph_after_copy.nodes()
        edges_added_copy = graph_after_copy.edges() - graph_before_copy.edges()
        edges_removed_copy = graph_before_copy.edges() - graph_after_copy.edges()

        if nodes_added_copy or nodes_removed_copy or edges_added_copy or edges_removed_copy:
            graph_num += 1
            graph_before_copy = graph_after_copy
print(graph_num)
i = 1

nrows, ncols =get_rows_cols(graph_num)

print(nrows , ncols)

if graph_before.nodes:
    pos = nx.circular_layout(graph_before, scale=5)
    # elif nodes_added and nodes_removed:

    # 新建一个子图
    ax = fig.add_subplot(nrows, ncols, i)
    i += 1

    commit_time = first_json_cmt.committer_date
    date = commit_time.strftime('%Y-%m-%d')

    plt.title(f'{first_json_cmt.hash[0:7]}  {date}', loc='center')

    # 绘制节点
    for node in graph_before.nodes:
        nx.draw_networkx_nodes(graph_before, pos, nodelist=[node], node_color='black', node_size=500)
    # 绘制边
    for edge in graph_before.edges:
        nx.draw_networkx_edges(graph_before, pos, edgelist=[edge], edge_color='grey', width=3)
    # 绘制结点名称
    for j, node in enumerate(graph_before.nodes(), start=1):
        x, y = pos[node][0], pos[node][1]
        plt.text(x, y, str(j), color='white', ha='center', va='center', fontsize=15)

for cmt in cmts_list:
    if os.path.exists(os.path.join(json_change, cmt.hash + '.json'))and os.path.join(json_change,
                                                                                             cmt.hash + '.json') != graph_before_path:
        graph_after_path = os.path.join(json_change, cmt.hash + '.json')

        with open(graph_after_path, 'r') as f:
            data_after = json.load(f)

        # 画出要对比的图
        graph_after = nx.DiGraph()
        for edge in data_after['cells']:
            source = os.path.basename(data_after['variables'][edge['src']])
            target = os.path.basename(data_after['variables'][edge['dest']])
            label = edge['values']
            graph_after.add_edge(source, target, label=label)

        # 计算两个图的节点集和边集的差异
        nodes_added = graph_after.nodes() - graph_before.nodes()
        nodes_removed = graph_before.nodes() - graph_after.nodes()
        edges_added = graph_after.edges() - graph_before.edges()
        edges_removed = graph_before.edges() - graph_after.edges()

        if not nodes_added and not nodes_removed and not edges_added and not edges_removed:
            continue

        if graph_after.nodes:
            pos = nx.circular_layout(graph_after, scale=5)
            # elif nodes_added and nodes_removed:

            # 新建一个子图
            ax = fig.add_subplot(nrows, ncols, i)
            i += 1

            commit_time = cmt.committer_date
            date = commit_time.strftime('%Y-%m-%d')

            plt.title(f'{cmt.hash[0:7]}  {date}', loc='center')

            # 绘制节点
            for node in graph_after.nodes:
                nx.draw_networkx_nodes(graph_after, pos, nodelist=[node], node_color='black', node_size=500)
            # 绘制边
            for edge in graph_after.edges:
                nx.draw_networkx_edges(graph_after, pos, edgelist=[edge], edge_color='grey', width=3)
            # 绘制结点名称
            for j, node in enumerate(graph_after.nodes(), start=1):
                x, y = pos[node][0], pos[node][1]
                plt.text(x, y, str(j), color='white', ha='center', va='center', fontsize=15)
            graph_before = graph_after
            print(f'{cmt.hash[0:7]}:')
            print(f'{cmt.msg}')

plt.axis('off')
plt.show()
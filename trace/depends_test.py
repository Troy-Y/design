import json
import os
import shutil
import subprocess
from pydriller import Repository
import networkx as nx
import git

url = r'D:\desktop\myrepo\cassandra'
depends_path = r'D:\depends-0.9.7'
data_path = r'D:\PythonProject\design_cassandra\data_copy'
cmdline_path = url
javasrc_path = r'D:\PythonProject\design_cassandra\data_copy\java_files'
json_path = r'D:\PythonProject\design_cassandra\data_copy\depends_json'

cmts_list = []
repo = git.Repo(url)

for cmt in Repository(url).traverse_commits():
    cmts_list.append(cmt)

# 按时间从近到远排序
cmts_list = list(reversed(cmts_list))
# for line in cmts_list:
#     print(line.hash)

def get_depends(src_path, dest_path, cmt):
    # 切换到depends的路径
    os.chdir(depends_path)

    cmd = f'java -jar depends.jar java {src_path} \output\n'


    # 启动 CMD 进程
    p = subprocess.Popen(['cmd'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.stdin.write(cmd.encode('utf-8'))
    p.stdin.flush()

    # 获取输出
    output, error = p.communicate()

    # 等待进程结束
    p.wait()

    # 将该commits的json文件移动该文件data目录下并改名
    src_file = r'D:\depends-0.9.7\output-file.json'

    with open(cmt, 'w') as f:
        new_path = os.path.join(dest_path, cmt + '.json')
        shutil.move(src_file, new_path)
    # 切换回原来的路径
    os.chdir(data_path)

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
    sccs = nx.kosaraju_strongly_connected_components(G)

    files_latest_scc = []

    for scc in sccs:
        if len(scc) > 2:
            # print(scc)
            node_names = [list(G.nodes())[i] for i in scc]
            for name in node_names:
                files_latest_scc.append(name[name.index('src\java'):])

    return files_latest_scc

def convert_path(path):
    return path.replace('\\', '/')

def get_file_from_cmt(commit, file_path):
    os.chdir(cmdline_path)
    file_path = convert_path(file_path)
    cmd = f'git show {commit}:{file_path}\n'
    # print(cmd)
    content = None
    # 执行命令获取文件内容
    # content = subprocess.run(cmd_get_content, stdout=subprocess.PIPE, shell=True,text=True).stdout
    try:
        # 执行命令获取文件内容
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                shell=True,
                                text=True)
        if result.returncode != 0:
            raise Exception(result.stderr.strip())
        content = result.stdout
    except Exception as e:
        # print(f'{file_path} is not found in {cmt.hash}')
        pass
    # 切换回原来的路径
    os.chdir(data_path)
    # print(content)
    return content

if not os.path.exists('../data_copy/output_of_latest_commit.json'):
    # 切换到depends的路径
    path = r'D:\depends-0.9.7'
    os.chdir(path)

    command = 'java -jar depends.jar java D:\depends-0.9.7\src\cassandra\src \output\n'

    # 启动 CMD 进程
    p = subprocess.Popen(['cmd'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.stdin.write(command.encode('utf-8'))
    p.stdin.flush()

    # 获取输出
    output, error = p.communicate()

    # 等待进程结束
    p.wait()

    # 将该commits前的json文件移动该文件data目录下并改名
    src_file = r'D:\depends-0.9.7\output-file.json'

    with open(src_file,'r') as f:
        output_of_latest_commit = f.read()

    dst_folder = data_path
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    json_name_old = 'output_of_latest_commit.json'
    new_path = os.path.join(dst_folder, json_name_old)
    shutil.move(src_file, new_path)

os.chdir(data_path)
with open('../data_copy/output_of_latest_commit.json','r') as f:
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
    sccs = nx.kosaraju_strongly_connected_components(G)

    files_latest_scc = []

    for scc in sccs:
        if len(scc) > 2:
            # print(scc)
            node_names = [list(G.nodes())[i] for i in scc]
            for name in node_names:
                files_latest_scc.append(name[name.index('src\java'):])
            # 只做一个，由18个文件组成的scc
            break

    for file in files_latest_scc:
        print(file)
    # print('1')

    # for line in files_latest_scc:
    #     print(line)
    # print(len(files_latest_scc))

    try:
        for cmt in cmts_list:
            for file in cmt.modified_files:
                # print(file.new_path)
                if file.new_path in files_latest_scc:
                    print(cmt.hash + ' is analyzed...')
                    # path_dir = ../data_copy/java_files/commits
                    path_dir = os.path.join('../data_copy/java_files', cmt.hash)
                    # print(path_dir)
                    if not os.path.exists(path_dir):
                        os.makedirs(path_dir)
                    for file_path in files_latest_scc:
                        # os.chdir(data_path)
                        # f_path = ../data_copy/java_files/commits/src/depends/....
                        f_path = os.path.join(path_dir, os.path.dirname(file_path))
                        # print(f_path)
                        if not os.path.exists(f_path):
                            os.makedirs(f_path)
                        f_path = os.path.join(f_path,os.path.basename(file_path))
                        # print(f_path)
                        with open(f_path,'w') as f:
                            input_path = os.path.join(data_path,'java_files',cmt.hash,file_path)
                            # file_path = Path(file_path).as_posix()

                            # 切换路径
                            os.chdir(cmdline_path)
                            # 获取文件内容
                            content = get_file_from_cmt(cmt.hash[0:7], file_path)
                            os.chdir(data_path)

                            # 将文件内容写入指定路径中的文件中
                            with open(input_path, 'w') as f_input:
                                if content != None:
                                    f_input.write(content)
                                else:
                                    print('',file=f_input)
                    src = os.path.join(javasrc_path, cmt.hash)
                    get_depends(src, json_path, cmt.hash)
                    break
    except ValueError:
        print("Maybe this commit had been deleted.")
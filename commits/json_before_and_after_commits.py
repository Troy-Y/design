import subprocess
import os
from pydriller import Repository
import shutil

url = r'D:\desktop\myrepo\depends'
cmts_list = []

for commit in Repository(url).traverse_commits():
    cmts_list.append(commit)

# 切换到depends的路径
path = r'D:\depends-0.9.7'
os.chdir(path)

i=1
for commit in cmts_list:
    print(i, end='.')
    print(commit.hash, end=' is analysing...\n')
    i += 1

    # 启动CMD进程
    p = subprocess.Popen(['cmd'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 向CMD输入命令
    command = 'java -jar depends.jar java D:\desktop\git-data\depends\\'
    command_old = command + commit.hash + '\old\src output\n'
    command_new = command + commit.hash + '\\new\src output\n'
    # print(command_old)
    # print(command_new)

    p.stdin.write(command_old.encode('utf-8'))
    p.stdin.flush()
    # 将该commits前的json文件移动该文件data目录下并改名
    src_file = r'D:\depends-0.9.7\output-file.json'
    dst_folder = r'D:\PythonProject\design\data\depends_output_json\\' + commit.hash
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    json_name_old = 'old.json'
    new_path = os.path.join(dst_folder, json_name_old)
    shutil.move(src_file, new_path)
    # 获取输出
    output, error = p.communicate()

    # 启动CMD进程
    p = subprocess.Popen(['cmd'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 将该commits前的json文件移动该文件data目录下并改名
    p.stdin.write(command_new.encode('utf-8'))
    p.stdin.flush()
    json_name_new = 'new.json'
    new_path = os.path.join(dst_folder, json_name_new)
    shutil.move(src_file, new_path)

    # 获取输出
    output, error = p.communicate()
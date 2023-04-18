import subprocess
import os
from pydriller import Repository

url = r'D:\desktop\myrepo\depends'
cmts_list = []

for commit in Repository(url).traverse_commits():
    cmts_list.append(commit)

# 切换到depends的路径
path = r'D:\depends-0.9.7'
os.chdir(path)

# 启动CMD进程
p = subprocess.Popen(['cmd'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

i=1
for commit in cmts_list:
    print(i,end='.')
    print(commit.hash,end=' is analysing...\n')
    i += 1
    # 向CMD输入命令
    command = 'java -jar depends.jar java D:\desktop\git-data\depends\\'
    command_old = command + commit.hash+ '\old\src output\n'
    command_new = command + commit.hash + '\\new\src output\n'
    p.stdin.write(command_old.encode('utf-8'))
    p.stdin.write(command_new.encode('utf-8'))


# 获取输出
output, error = p.communicate()
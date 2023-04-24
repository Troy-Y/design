import os
from pydriller import Repository
import subprocess

url = r'D:\desktop\myrepo\depends'
cmts_list = []

# i=1
# print("该项目的commits：")
for commit in Repository(url).traverse_commits():
    cmts_list.append(commit)
    # print(i,end='.')
    # print(commit.hash)
    # i+=

# f1,f2 = os.path.split(cmts_list[0].modified_files[3].new_path)
#
# print(f2)

path = r'D:\desktop\git-data\depends'

if not os.path.exists(path):
    os.mkdir(path)

for commit in cmts_list:
    # 输出每个commits前后被改变的文件
    try:
        commit_path = path + '\\' + commit.hash
        if not os.path.exists(commit_path):
            os.mkdir(commit_path)
        old_src_path = commit_path + '\\' + 'old'
        new_src_path = commit_path + '\\' + 'new'
        if not os.path.exists(old_src_path):
            os.mkdir(old_src_path)
        if not os.path.exists(new_src_path):
            os.mkdir(new_src_path)
        for file in commit.modified_files:
            # 按路径输出
            try:
                folder_name_old, file_name_old = os.path.split(file.old_path)
                folder_name_new, file_name_new = os.path.split(file.new_path)
                # print(folder_name_old)
                # print(file_name_old)
                # print(folder_name_new)
                # print(file_name_new)
                file_old_path = old_src_path + '\\' + folder_name_old
                file_new_path = new_src_path + '\\' + folder_name_new
                # print(file_old_path)
                # print(file_new_path)
                if not os.path.exists(file_old_path):
                    os.makedirs(file_old_path)
                if not os.path.exists(file_new_path):
                    os.makedirs(file_new_path)
                f_old = file_old_path + '\\' + file_name_old
                f_new = file_new_path + '\\' + file_name_new
                # print(f_old)
                # print(f_new)
                file_old = open(f_old, "w")
                file_new = open(f_new + file_name_new, "w")
                print(file.source_code,file = file_new)
                print(file.source_code_before,file = file_old)
            except TypeError:
                print('This is a NoneType file , so analysis the next one.')
    except ValueError:
        print("Maybe this commit had been deleted , analysis the next one.")
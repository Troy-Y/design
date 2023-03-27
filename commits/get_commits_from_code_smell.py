from pydriller import Repository
import pandas as pd
import numpy as np
from git import *

url = r'D:\desktop\myrepo\depends'
cmts_list = []
designCodeSmells = pd.read_csv("../data/designCodeSmells.csv")
# print(code_smell)
col1 = designCodeSmells["Type Name"]
code_smell_file = np.array(col1)
col2 = designCodeSmells["Code Smell"]
code_smell_type = np.array(col2)
code_smell = []
code_type = []
for file in code_smell_file:
    code_smell.append(file)
for t in code_smell_type:
    code_type.append(t)

for i in range(len(code_smell)):
    code_smell[i] = code_smell[i] + '.java'

i=1
# print("该项目的commits：")
for commit in Repository(url).traverse_commits():
    cmts_list.append(commit)
    # print(i,end='.')
    # print(commit.hash)
    i+=1
# print(i)

num=1
output_commits_file = open("../data/commits.txt","w")
output_diff_file = open("../data/diff.txt","w")

print("该项目中带代码气味的commits：")
for i in range(len(cmts_list)):
    try:
        for file in cmts_list[i].modified_files:
            if(file.filename in code_smell):
                print(num,end='. ')
                print(cmts_list[i].hash)
                num += 1
                print("产生代码气味的文件：",file.filename)
                print("产生的代码气味类型：",code_type[code_smell.index(file.filename)])
                print(cmts_list[i].hash,file=output_commits_file)
                print(cmts_list[i].hash,file=output_diff_file)
                print(file.diff,file=output_diff_file)
                break
    except ValueError:
        print("again")
output_commits_file.close()
output_diff_file.close()
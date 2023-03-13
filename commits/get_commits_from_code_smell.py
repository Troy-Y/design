from pydriller import Repository
import pandas as pd
import numpy as np

url = r'D:\desktop\myrepo\depends'
cmts_list = []
code_smell = pd.read_csv("../data/designCodeSmells.csv")
# print(code_smell)
col1 = code_smell["Type Name"]
code_smell_file = np.array(col1)

for i in range(len(code_smell_file)):
    code_smell_file[i] = code_smell_file[i] + '.java'
# print(f_name)
# print(f_name)
# print(code_smell_name)



i=1
# print("该项目的commits：")
for commit in Repository(url).traverse_commits():
    cmts_list.append(commit)
    # print(i,end='.')
    # print(commit.hash)
    i+=1
# print(i)

num=1
# fo = open("../data/commits.txt","w")
print("该项目中带代码气味的commits：")
for i in range(len(cmts_list)):
    for file in cmts_list[i].modified_files:
        if(file.filename in code_smell_file):
            print(num,end='.')
            num += 1
            print(cmts_list[i].hash)
            # print(cmts_list[i].hash,file=fo)
            break
# fo.close()
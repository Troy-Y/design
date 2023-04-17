import json
import os

# 读取JSON文件
with open('../data/output-file.json', 'r') as f:
    data = json.load(f)

variables = []
fnames_of_depends = open("../data/fnames_of_depends","w")

line_num_of_depends = 0

for line in data['variables']:
    if line not in variables:
        line_num_of_depends += 1
        variables.append(line)
        fname = os.path.basename(line)
        print(fname,file = fnames_of_depends)

fnames_of_depends = []

for vrabl in variables:
    fname = os.path.basename(vrabl)
    fnames_of_depends.append(fname)
    # print(fname)

line_num_of_diff = 0

with open('../data/fnames_of_diff', 'r') as f:
    fnames_of_diff = [line.strip() for line in f]
    for line in fnames_of_diff:
        line_num_of_diff += 1
# print(line_num_of_diff)

same_files_num = 0

for line in fnames_of_diff:
    if line in fnames_of_depends:
        same_files_num += 1
if same_files_num == line_num_of_depends:
    print("与depends分析行数相同")
elif same_files_num == line_num_of_diff:
    print("与diff分析行数相同")

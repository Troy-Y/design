import re

definition_key = ['abstract','assert','boolean','byte','char','class','double','final',
            'float','int','interface','long','new','private','protected','public',
            'short','static','void','String','Integer']
none_key = ['}']

# str = '+public class DependencyType {'
# s1 = str.lstrip('+')
# if any(substring in s1.split() for substring in java_key):
#     print('true')

empty = []

code_line = open('../data/code_line_analysis.txt',mode='w')

with open('../data/diff.txt') as diff_file:
    diff = diff_file.read().splitlines()
    for line in diff:
        line_splt = ''
        line_copy = line
        if '//' in line_copy :
            print(line_copy, file=code_line)
            continue
        if(len(line)>1 and line[0] == '+'):
            temp = line.lstrip('+')
            line_splt = temp.split()
            t = ''
            if line_splt != empty:
                if any(substring in line_splt for substring in definition_key):
                    t = t + line_copy + ' // this code line is the definition line'
                elif line_splt == none_key:
                    continue
                else:
                    t = t + line_copy + ' // this code line is the reference line'
            else:
                t = t + line_copy + ' // this code line is the reference line'
            print(t, file=code_line)
            # print(t)
        else:
            print(line_copy,file=code_line)
            # print(line_copy)
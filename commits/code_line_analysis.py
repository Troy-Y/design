import re

definition_key = ['abstract','assert','boolean','byte','char','class','double','final',
            'float','int','interface','long','new','private','protected','public',
            'short','static','void','String','Integer']

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
        if(len(line)>2 and line[0] == '+'):
            temp = line.lstrip('+')     # 去掉+号
            line_splt = temp.split()    # 按空格分裂
            t = ''
            if line_splt != empty:
                if any(substring in line_splt for substring in definition_key) \
                        and '{' not in line_copy:
                    t = t + line_copy + ' // this code line is the definition line,'
                    is_cls = 1
                    for key in line_splt:
                        if key in definition_key:
                            continue
                        if is_cls == 1:
                            t = t + ' Class:' + key
                            is_cls = 0
                        elif is_cls == 0 and key != '=':
                            t = t + ', Variables:' + key
                            break

                elif '{' in line_copy or '}' in line_copy or 'return' in line_copy:
                    t = t + line_copy
                else:
                    t = t + line_copy + ' // this code line is the reference line'
            else:
                t = t + line_copy + ' // this code line is the reference line'
            print(t, file=code_line)
            # print(t)
        else:
            print(line_copy,file=code_line)
            # print(line_copy)
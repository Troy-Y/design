import re

# 匹配Java类名
class_name_pattern = r'\b[A-Z]\w*\b'

# 匹配Java变量名
variable_name_pattern = r'(?:^|\s)([A-Za-z]\w*)\s*(?:=|;)'

# 匹配Java代码行
class_pattern = r'\b[A-Z][a-zA-Z0-9_]*\b'
variable_pattern = r'\b[a-z][a-zA-Z0-9_]*\b'

def get_classname_and_variable_name(line):
    # 提取类名
    class_name_match = re.findall(class_name_pattern, line)
    if class_name_match:
        class_name = class_name_match[0]
        line = line + ' Class name: ' + class_name
    # 提取变量名
    variable_name_match = re.search(variable_name_pattern, line)
    if variable_name_match:
        variable_name = variable_name_match.group(1)
        line = line + ', Variable name: ' + variable_name
    return line

code_file = open('../data/code_line_analysis.txt', mode='w')

with open('../data/diff.txt') as diff_file:
    diff = diff_file.read().splitlines()
    for line in diff:
        # 判断是否为define行
        if re.search(r'\b' + class_pattern + r'\s+' + variable_pattern + r'\s*;', line):
            line = line + ' // This is a define line.'
            line = get_classname_and_variable_name(line)
        # 判断是否为refer行
        elif re.search(r'\b' + variable_pattern + r'\s*=\s*new\s+' + class_pattern + r'\s*\(\s*\)\s*;',
                       line) or re.search(
                r'\b' + class_pattern + r'\s+' + variable_pattern + r'\s*=\s*new\s+' + class_pattern + r'\s*\(\s*\)\s*;',
                line):
            line = line + ' // This is a refer line.'
            line = get_classname_and_variable_name(line)
        print(line, file=code_file)

code_file.close()
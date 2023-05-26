import os
import subprocess

d = r'D:\desktop\cassandra\diff'
cmdline_path = r'D:\desktop\myrepo\cassandra'
data_path = r'D:\PythonProject\design_cassandra\data_copy'
def get_file_diff(commit1, commit2, file_path):
    os.chdir(cmdline_path)
    cmd = f'git diff {commit1} {commit2} {file_path} \n'
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

    return content

# 示例用法
commits = ['3a2faf9', 'e0adc16', '9c50b1f', '0c444a7']
files_path = ['src/java/org/apache/cassandra/exceptions/ExceptionCode.java',
              'src/java/org/apache/cassandra/exceptions/TransportException.java',
              'src/java/org/apache/cassandra/transport/ProtocolException.java',
              'src/java/org/apache/cassandra/transport/ProtocolVersion.java']

for i in range(0, 4):
    for file_path in files_path:
        diff = get_file_diff(commits[i], commits[i]+'~1', file_path)
        # print(diff)
        dir_name = os.path.dirname(file_path)
        output_dir = os.path.join(d, commits[i], dir_name)
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, os.path.basename(file_path))
        with open(output_file, 'w') as f:
            f.write(diff)
            # print(f'Created file: {output_file}')
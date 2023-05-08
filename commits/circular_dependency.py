import os

scc_path = '../data/scc/'

# 对比两个依赖图是否相同
def dependency_graph_is_changed(file1, file2):
    filename_in_f1 = set()
    filename_in_f2 = set()
    s1 = set()
    s2 = set()
    with open(file1, "r") as f1, open(file2, "r") as f2:
        for line in f1:
            if line.strip().isdigit() and frozenset(filename_in_f1):
                    s1.add(frozenset(filename_in_f1))
                    filename_in_f1.clear()
                    continue
            filename_in_f1.add(os.path.basename(line.strip()))
        s1.add(frozenset(filename_in_f1))

        for line in f2:
            if line.strip().isdigit() and frozenset(filename_in_f2):
                    s2.add(frozenset(filename_in_f2))
                    filename_in_f2.clear()
                    continue
            filename_in_f2.add(os.path.basename(line.strip()))
        s2.add(frozenset(filename_in_f2))

    if s1 != s2:
        # print(s1)
        # print(s2)
        return False
    return True

# 对比所有commits前后的依赖图
for item in os.listdir(scc_path):
    scc_old = scc_path + item + '/old.txt'
    scc_new = scc_path + item + '/new.txt'
    # print(scc_old)
    # print(scc_new)

    # 如果某个commits前后都有强联通分量，则查看commits前后强联通分量是否相同。
    if os.path.isfile(scc_old) and os.path.isfile(scc_new):
        if not dependency_graph_is_changed(scc_old,scc_new):
            print('The dependency before and after ' + item +' is changed')
    # 如果某commits前没有强连通分量，但在commits后有了强连通分量，则说明这个commits创建了一个新的循环依赖。
    elif not os.path.isfile(scc_old) and os.path.isfile(scc_new):
        print('The circular dependency after ' + item + ' is created')

# f_old = '../data/scc/18a7c2b851ce53c4052d10ce4bbe3b3fafec27b1/old.txt'
# f_new = '../data/scc/18a7c2b851ce53c4052d10ce4bbe3b3fafec27b1/new.txt'
# print(dependency_graph_is_changed(f_old,f_new))
# 根据边列表判断子集a中的节点经过符号e到达什么节点
def move(a, e, f):
    s = []
    for i in a:
        for j in range(len(f)):
            if i == f[j][0] and f[j][1] == e:
                s.append(f[j][2])
    return sorted(s)

# 子集划分算法
def operation(nodes,edges):
    # 先将输入的edges每个元组中的节点序号转换为节点
    node_dict = {str(row[1]): row[0] for row in nodes}
    edges = [(list(node_dict.keys())[list(node_dict.values()).index(source)], 
             list(node_dict.keys())[list(node_dict.values()).index(target)], 
             label) 
            for source, target, label in edges]

    # 从 nodes 中提取节点集合 K
    K = [str(node[1]) for node in nodes]
    # 从 edges 中提取符号集合 E
    E = list(set([edge[2] for edge in edges]))
    # 从 nodes 中提取初态集合 S
    S = [str(node[1]) for node in nodes if 'begin' in node[2]]
    # 从 nodes 中提取终态集合 Z
    Z = [str(node[1]) for node in nodes if 'end' in node[3]]
    # 将元组列表转换为二维列表    
    f = [[str(t[0]), t[2], str(t[1])] for t in edges]

    # 划分出状态集：终态和非终态
    a = [] 
    KK=[]
    for x in K:
        if x not in Z:
            a.append(x)
    KK = [a, Z]

    # 划分节点集合
    while len(KK) != len(K):
        flag0 = 0
        for i in range(len(KK)):
            state = KK[i]
            flag1 = 0
            for j in range(len(E)):
                state1 = move(state, E[j], f)  # 判断到达的状态
                flag2 = 0
                for k in range(len(KK)):
                    # 检查集合state1中是否存在不在当前子集KK[k]中的状态
                    if len(set(state1).difference(set(KK[k]))) != 0:
                        flag2 = flag2 + 1
                # 表示state中有可划分的状态
                if flag2 == len(KK):
                    flag1 = flag1 + 1
                    break
            if flag1 == 1:
                ilag = j
                State3 = [state[0]]
                state1 = move(State3, E[ilag], f)
                for k in range(len(KK)):
                    if len(set(state1).difference(set(KK[k]))) == 0:
                        # 标记是非终态还是终态
                        label = k
                        break
                State4 = []
                for j in range(1, len(state)):
                    zz = [state[j]]
                    state1 = move(zz, E[ilag], f)
                    if len(set(state1).difference(set(KK[label]))) == 0:
                        State3.append(state[j])
                    else:
                        State4.append(state[j])
                # 将子集节点进行重新划分
                KK.pop(i)
                KK.extend([State3, State4])
            else:
                flag0 = flag0 + 1
        if flag0 == len(KK):
            break

    # 将相同状态的节点进行合并
    for n in KK:
        while(len(n) >= 2):
            a=n[len(n)-1]
            if n[len(n)-1] in K:
                K.remove(n[len(n)-1])
            if n[len(n)-1] in S:
                S.remove(n[len(n)-1])
            if n[len(n)-1] in Z:
                Z.remove(n[len(n)-1])
            # 更新n的集合
            n = [x for x in n if x != a]
            # 对合并的节点进行边的合并
            for e_n in f:
                if e_n[0] == a:
                    e_n[0] = n[0]
                if e_n[2] == a:
                    e_n[2] = n[0]
    
    # 对合并后的边进行去重得到二维边列表
    f_min = [list(edge) for edge in set(tuple(edge) for edge in f)]

    # 提取新的节点
    all_nodes = set()
    for edge in f_min:
        all_nodes.add(edge[0])
        all_nodes.add(edge[2])
    # 转换为列表形式
    nodes_list = list(all_nodes)
    current_index = 1
    
    # 定义最小化后的节点列表
    nodes_tuples = []
    for node in nodes_list:
        if node in S:
            nodes_tuples.append((0, node, 'begin',''))
        elif node in Z:
            nodes_tuples.append((current_index, node, '','end'))
            current_index += 1
        else:
            nodes_tuples.append((current_index, node, '',''))
            current_index += 1

    # 将二维边列表的节点用序号代替
    dict = {str(row[1]): row[0] for row in nodes_tuples}
    replaced = [[dict[row[0]], row[1], dict[row[2]]] for row in f_min]
    # 将二维列表转换为元组列表,得到最小化后的边列表
    New_edges = [(int(start), int(end), symbol) for start, symbol, end in replaced]

    return  nodes_tuples,New_edges

# 测试DFA最小化
# 两个输入样例：
# 定义节点列表
# nodes = [(0, '1', 'begin'), (1, '2', ''), (2, '3', ''), (3, '4', 'end')]
# nodes = [(0, '0', 'begin',''), (1, '1', '',''), (2, '2', '',''), (3, '3','', 'end'),(4,'4','','end'),(5,'5','','end'),(6,'6','','end')]

# # 定义边列表
# # edges = [(0, 2,'b'), (0,1,'a'), (1,1,'a'), (1,3,'b'), (2,2,'b'), (2,1,'a'), (3,2,'b'), (3,1,'a')]
# edges = [(0, 1,'a'), (0,2,'b'), (1,2,'b'), (2,1,'a'), (1,3,'a'), (2,4,'b'), (3,3,'a'), (4,4,'b'),(3,5,'b'),(5,4,'b'),(4,6,'a'),(5,6,'a'),(6,5,'b'),(6,3,'a')]
    
# # 执行DFA最小化操作

# result = operation(nodes, edges)
# nodes_tuples, New_edges = result

# print("Nodes Tuples:", nodes_tuples)
# print("New Edges:", New_edges)

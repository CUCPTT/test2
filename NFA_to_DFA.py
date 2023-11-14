def nodes_to_with(nodes,edges):#找到当前nodes，可以通过ε到达的所有点(nodes的ε-闭包)
    cnt = 0
    while cnt != len(nodes):
        cnt = len(nodes)
        for i in edges:
            if i[0] in nodes and i[-1] == 'ε' and i[1] not in nodes:
                nodes.append(i[1])
    return nodes


def nfa_to_dfa(nfa_nodes,nfa_edges):
    dfa_nodes = []
    dfa_edges = []

    #引入新的初态和终态，保证最后初态唯一
    add_nodes = []
    add_edges = []
    cnt = len(nfa_nodes)-1
    for i in nfa_nodes:
        if i[2] == 'begin':
            cnt = cnt + 1
            add_nodes.append((cnt,str(cnt),'begin',''))
            add_edges.append((cnt,i[0],'ε'))
            nfa_nodes.remove(i)
            i = (i[0],i[1],'',i[3])
            nfa_nodes.append((i[0],i[1],'',i[3]))
        
        if i[3] == 'end':
            cnt = cnt + 1
            add_nodes.append((cnt,str(cnt),'','end'))
            add_edges.append((i[0],cnt,'ε'))
            nfa_nodes.remove(i)
            nfa_nodes.append((i[0],i[1],i[2],''))


    nfa_nodes += add_nodes
    nfa_edges += add_edges
    nfa_nodes.sort()

    #找到起始点通过ε可以到达的所有点
    nodes_begin = []

    for i in nfa_nodes:
        if i[2] == 'begin':
            nodes_begin.append(i[0])

    nodes0 = nodes_to_with(nodes_begin,nfa_edges)

    temp = [nodes0] #中间变量，用于作为队列
    temp_nodes = [nodes0] #中间变量，储存变化过程中出现过的点
    temp_edges = [] #中间变量，储存变化过程中出现过的边
    edges_without_ = [] #不含ε的边
    chars = [] #所有字符
    for i in nfa_edges:
        if i[2] != 'ε':
            if i[2] not in chars:
                chars.append(i[2])
            edges_without_.append(i)
    # bfs，进行nfa确定化
    while temp != []:
        
        now = temp.pop()
        to = []

        #确定当前状态集，经过每个字符可以到达的状态集
        for i in chars:
            
            for j in edges_without_:
                if j[0] in now and j[2] == i:
                    to.append(j[1])

            to = nodes_to_with(to,nfa_edges)

            if to != [] :
                temp_edges.append([now,to,i])

                if to not in temp_nodes:
                    temp_nodes.append(to)
                    temp.append(to)
                
                to = []


    #确定新节点的编号，赋值于nfa_nodes，temp_edges
    cnt = len(temp_nodes)

    for i in range(0,cnt):
        book = 0
        for j in temp_nodes[i]:
            if nfa_nodes[j][3] == 'end':
                book = 1
                break
        
        if i == 0:
            if book == 1:
                dfa_nodes.append((i,str(i),'begin','end'))
            else:
                dfa_nodes.append((i,str(i),'begin',''))
        else:
            if book == 1:
                dfa_nodes.append((i,str(i),'','end'))
            else:
                dfa_nodes.append((i,str(i),'',''))
            

    for i in temp_edges:
        dfa_edges.append((temp_nodes.index(i[0]),temp_nodes.index(i[1]),i[2]))

    print("DFA_nodes:",dfa_nodes)
    print("DFA_edges:",dfa_edges)

    return dfa_nodes , dfa_edges

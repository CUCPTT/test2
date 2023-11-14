class NFA:
    def __init__(self):
        self.Q = set()                     # 状态集合
        self.sigma = set()                 # 输入字符集合
        self.delta = {}                    # 状态转移函数
        self.q0 = None                     # 初始状态
        self.F = set()                     # 接收状态集合

def is_operand(a):
    return a.isdigit() or a.isalpha()

def str_to_nfa(postfix_expression):
    print(postfix_expression)
    status_id = 0
    st_begin = []
    st_end = []
    nfa_instance = NFA()

    for i in range(len(postfix_expression)):
        if is_operand(postfix_expression[i]):
            nfa_instance.sigma.add(postfix_expression[i])
            pre = status_id
            nfa_instance.Q.add(status_id)
            st_begin.append(status_id)
            status_id += 1
            nxt = status_id
            nfa_instance.Q.add(status_id)
            st_end.append(status_id)
            status_id += 1
            # TODO
            nfa_instance.delta.setdefault(pre, {}).setdefault(postfix_expression[i], []).append(nxt)
        elif postfix_expression[i] == '*':
            pre = st_end.pop()
            nxt = st_begin.pop()
            nfa_instance.delta.setdefault(pre, {}).setdefault('ε', []).append(nxt)
            nfa_instance.Q.add(status_id)
            # pre1 = status_id  改 先赋值，再加一
            pre1 = status_id
            status_id += 1
            nfa_instance.Q.add(status_id)
            # status_id += 1
            # nxt1 = status_id 改 先赋值，再加一
            nxt1 = status_id
            status_id += 1
            nfa_instance.delta.setdefault(pre1, {}).setdefault('ε', []).append(nxt)
            nfa_instance.delta.setdefault(pre, {}).setdefault('ε', []).append(nxt1)
            nfa_instance.delta.setdefault(pre1, {}).setdefault('ε', []).append(nxt1)
            st_begin.append(pre1)
            st_end.append(nxt1)
        elif postfix_expression[i] == '.':
            pre1 = st_begin.pop()
            pre2 = st_begin.pop()
            nxt1 = st_end.pop()
            nxt2 = st_end.pop()
            nfa_instance.delta.setdefault(nxt2, {}).setdefault('ε', []).append(pre1)
            st_begin.append(pre2)
            st_end.append(nxt1)
        elif postfix_expression[i] == '|':
            nfa_instance.Q.add(status_id)
            pre = status_id
            status_id += 1
            nfa_instance.Q.add(status_id)
            nxt = status_id
            status_id += 1

            # TODO 原代码中没有这一句
            if not st_begin or not st_end:
                print("Error: Not enough operands for | operator")
                return nfa_instance

            pre1 = st_begin.pop()
            pre2 = st_begin.pop()
            nxt1 = st_end.pop()
            nxt2 = st_end.pop()

            nfa_instance.delta.setdefault(pre, {}).setdefault('ε', []).append(pre1)
            nfa_instance.delta.setdefault(pre, {}).setdefault('ε', []).append(pre2)
            nfa_instance.delta.setdefault(nxt1, {}).setdefault('ε', []).append(nxt)
            nfa_instance.delta.setdefault(nxt2, {}).setdefault('ε', []).append(nxt)

            st_begin.append(pre)
            st_end.append(nxt)

    nfa_instance.q0 = st_begin[-1]
    nfa_instance.F.add(st_end[-1])
    nfa_instance.sigma.add('ε')
    return nfa_instance

def generate_nfa(nfa_instance):

    nodes = set()
    edges = []

    for state in nfa_instance.Q:
        for symbol in nfa_instance.sigma:
            # 相比于原代吗，可以更安全地处理不存在的键
            if symbol in nfa_instance.delta.get(state, {}):
                for nxt_state in nfa_instance.delta[state][symbol]:
                    if nfa_instance.q0 == state:
                        nodes.add((state, f"{state}", 'begin',''))
                        nodes.add((nxt_state, f"{nxt_state}", '',''))
                        edges.append((state, nxt_state, symbol))
                    # TODO 和原代码不一样
                    if nxt_state in nfa_instance.F:
                        nodes.add((state, f"{state}", '',''))
                        nodes.add((nxt_state, f"{nxt_state}", '','end'))
                        edges.append((state, nxt_state, symbol))
                    if not(nfa_instance.q0 == state or nxt_state in nfa_instance.F):
                        nodes.add((state, f"{state}", '',''))
                        nodes.add((nxt_state, f"{nxt_state}", '',''))
                        edges.append((state, nxt_state, symbol))

    nodes_list = []
    for node_tuple in nodes:
        node_list = list(node_tuple)
        nodes_list.append(node_list)

    # TODO 原代吗中没有
    nodes_list.sort(key=lambda x: x[0])  # 按状态号排序
    nodes_list[0][2] = 'begin'

    formatted_nodes = []
    for node_list in nodes_list:
        node_tuple = tuple(node_list)
        formatted_nodes.append(node_tuple)

    # print(formatted_nodes)

    final_nodes = []

    i = 0

    while i < len(formatted_nodes) - 1:
        current_node = formatted_nodes[i]
        next_node = formatted_nodes[i + 1]

        if current_node[0] == next_node[0]:
            
            if current_node[2] == '' and current_node[3] == '': # 先排除current_node
                final_nodes.append(next_node)
            else:
                final_nodes.append(current_node)
            
            # 移动到下一个元素
            i += 1
        else:
            final_nodes.append(current_node)

        i += 1


    # 处理最后一个元素
    if i == len(formatted_nodes) - 1:
        final_nodes.append(formatted_nodes[-1])
    
    new_nodes = []
    for tuple_node in final_nodes:
        new_nodes.append(list(tuple_node))

    new_nodes[0][2] = 'begin'
    new_nodes[-1][3] = 'end'

    final_nodes = []
    for list_node in new_nodes:
        final_nodes.append(tuple(list_node))

    print("Nodes:", final_nodes)
    print("Edges:", list(set(edges)))

    return final_nodes, edges
    
# if __name__ == "__main__":
#     postfix_expression = ''
#     # postfix_expression = 'a'
#     nfa_instance = str_to_nfa(postfix_expression)
#     generate_nfa(nfa_instance)

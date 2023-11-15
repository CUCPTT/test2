import random
from copy import deepcopy

# 转换输入数据的结构
def convert_to_state_graph(nodes, edges):
    state_graph = {
        'total_states': [str(node[0]) for node in nodes],
        'initial_states': [str(node[0]) for node in nodes if node[2] == 'begin'],
        'termination_states': [str(node[0]) for node in nodes if node[3] == 'end'],
        'state_transition_map': {},
        'cins': []
    }

    for edge in edges:
        state_from, state_to, transition = map(str, edge)

        if transition not in state_graph['cins']:
            state_graph['cins'].append(transition)

        if state_from not in state_graph['state_transition_map']:
            state_graph['state_transition_map'][state_from] = {}

        if transition not in state_graph['state_transition_map'][state_from]:
            state_graph['state_transition_map'][state_from][transition] = state_to
        else:
            # If multiple transitions from the same state with the same input, convert to a list
            if not isinstance(state_graph['state_transition_map'][state_from][transition], list):
                state_graph['state_transition_map'][state_from][transition] = [state_graph['state_transition_map'][state_from][transition]]
            state_graph['state_transition_map'][state_from][transition].append(state_to)

    return state_graph



def hopcroft_algorithm( G ):
    cins                   = set( G['cins'] )
    termination_states     = set( G['termination_states'] ) 
    total_states           = set( G['total_states'] )
    state_transition_map   = G['state_transition_map']
    not_termination_states = total_states - termination_states
 
    def get_source_set( target_set, char ):
        source_set = set()
        for state in total_states:
            try:
                if state_transition_map[state][char] in target_set:
                    source_set.update( state )
            except KeyError:
                pass
        return source_set
 
    P = [ termination_states, not_termination_states ]
    W = [ termination_states, not_termination_states ]
 
    while W:
        
        A = random.choice( W )
        W.remove( A )
 
        for char in cins:
            X = get_source_set( A, char )
            P_temp = []
            
            for Y in P:
                S  = X & Y
                S1 = Y - X
                
                if len( S ) and len( S1 ):
                    P_temp.append( S )
                    P_temp.append( S1 )
                    
                    if Y in W:
                        W.remove( Y )    
                        W.append( S )
                        W.append( S1 )
                    else:
                        if len( S ) <= len( S1 ):
                            W.append( S )
                        else:
                            W.append( S1 )
                else:
                    P_temp.append( Y )
            P = deepcopy( P_temp )
    return P

def get_mindfa(nodes,edges,new_nodes):
    new_nodes = [[int(num) for num in set_of_nums] for set_of_nums in new_nodes]
    # print(new_nodes)
    mindfa_nodes = []
    mindfa_edges = []

    cnt = 0
    #根据新点集，构建新节点
    for i in new_nodes:
        book1 = 0
        book2 = 0
        for j in i:
            if nodes[j][2] == 'begin':
                book1 = 1
            if nodes[j][3] == 'end':
                book2 = 1
        
        node = [cnt,str(cnt)]
        if book1 == 1 :
            node.append('begin')
        else:
            node.append('')

        if book2 == 1 :
            node.append('end')
        else:
            node.append('')
        
        mindfa_nodes.append(tuple(node))
        cnt=cnt+1

    #遍历原边，找到新节点和新边的对应关系
    for i in edges:
        fr = -1
        to = -1
        for j in new_nodes:
            if i[0] in j:
                fr = new_nodes.index(j)
            if i[1] in j:
                to = new_nodes.index(j)
        
        edge = (fr,to,i[2])

        if edge not in mindfa_edges:
            mindfa_edges.append(edge)

    print("mindfa_nodes: ",mindfa_nodes)
    print("mindfa_edges: ",mindfa_edges)

    return mindfa_nodes,mindfa_edges
# # Example usage:
# nodes = [(0, '0', 'begin', ''), (1, '1', '', ''), (2, '2', '', ''), (3, '3', '', ''), (4, '4', '', ''), (5, '5', '', ''), (6, '6', '', ''), (7, '7', '', 'end')]
# edges = [(0, 1, 'a'), (1, 2, 'b'), (2, 3, 'c'), (3, 4, 'a'), (3, 5, 'b'), (5, 4, 'a'), (5, 5, 'b'), (4, 4, 'a'), (4, 6, 'b'), (6, 4, 'a'), (6, 5, 'b'), (6, 7, 'd')]

# nodes = [(0, 'A', 'begin',''), (1, 'B', '',''), (2, 'C', '',''), (3, 'D', '','end')]
# edges = [(0, 2,'b'), (0,1,'a'), (1,1,'a'), (1,3,'b'), (2,2,'b'), (2,1,'a'), (3,2,'b'), (3,1,'a')]

# nodes = [(0, '0', 'begin',''), (1, '1', '',''), (2, '2', '',''), (3, '3', '','end'),(4, '4', '', ''), (5, '5', '', 'end')]
# edges = [(0, 1,'f'), (1,2,'e'),(1,4,'i'), (2,3,'e'), (4,5,'e')]

def DFA_Minimize(nodes, edges):
    state_graph1 = convert_to_state_graph(nodes, edges)
    new_nodes=hopcroft_algorithm( state_graph1)
    return get_mindfa(nodes,edges,new_nodes)


# mindfa_nodes,mindfa_edges= DFA_Minimize(nodes, edges)
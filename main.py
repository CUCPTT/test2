import io
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image
import re
import graphviz
from matplotlib import pyplot as plt
from infix2postfix import infix_to_postfix
from postfix2nfa import str_to_nfa,generate_nfa
from NFA_to_DFA import nfa_to_dfa
from DFA_Minimize import operation

def create_graph(nodes, edges):
    # 创建有向图并设置布局方向为水平
    dot = graphviz.Digraph(graph_attr={'rankdir': 'LR'})

    # 添加节点
    for node in nodes:
        if node[2] == 'begin':
            # 创建一个虚拟节点
            dot.node('begin_node', label='', shape='point')   
            # 从虚拟节点指向目标节点
            dot.edge('begin_node', str(node[0]), arrowhead='onormal') 
        
        # 检查节点是否为"结束"节点，如果是，则添加两个环的标记
        if node[3] == 'end':
            dot.node(str(node[0]), node[1], shape='doublecircle')
        else:
            dot.node(str(node[0]), node[1])



    # 添加边
    for edge in edges:
        dot.edge(str(edge[0]), str(edge[1]), label=edge[2])

    # 渲染图形并获取图像数据
    dot.format = 'png'
    image_data = dot.pipe()

    # 将图像数据加载到PIL图像对象中
    image = Image.open(io.BytesIO(image_data))

    # 显示图像
    plt.imshow(image)
    plt.axis('off')
    plt.show()

def NFA(input_text):
    nodes, edges = generate_nfa(str_to_nfa(infix_to_postfix(input_text)))
    create_graph(nodes, edges)

def DFA(input_text):
    nodes, edges = generate_nfa(str_to_nfa(infix_to_postfix(input_text)))
    nodes, edges = nfa_to_dfa(nodes, edges)
    create_graph(nodes, edges)

def Min_DFA(input_text):
    nodes, edges = generate_nfa(str_to_nfa(infix_to_postfix(input_text)))
    nodes, edges = nfa_to_dfa(nodes, edges)
    nodes, edges = operation(nodes, edges)
    create_graph(nodes, edges)

def submit_button_clicked():
    regex = regex_entry.get()
    option = option_combobox.get()

    # 检查正则表达式是否有效
    try:
        re.compile(regex)
    except re.error:
        messagebox.showerror('Invalid regular expression', 'Invalid regular expression. Please enter a valid one.')
        return

    # 根据选项调用相应的函数
    if option == 'NFA':
        NFA(regex)
    elif option == 'DFA':
        DFA(regex)
    elif option == 'Minimized DFA':
        Min_DFA(regex)
    else:
        option = None
        messagebox.showerror('Invalid option', 'Invalid option. Please select NFA, DFA, or Minimized DFA.')
        return

# 创建主窗口
root = tk.Tk()
root.title('Experiment-2')
root.configure(bg='#FFC0CB')  

# 创建布局
frame = ttk.Frame(root, padding='10', style='My.TFrame')
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# 创建控件
regex_label = ttk.Label(frame, text='INPUT:', style='My.TLabel')
regex_entry = ttk.Entry(frame, width=30)
option_label = ttk.Label(frame, text='SELECT:', style='My.TLabel')
option_combobox = ttk.Combobox(frame, values=['NFA', 'DFA', 'Minimized DFA'], width=25)
submit_button = ttk.Button(frame, text='Submit', command=submit_button_clicked, style='My.TButton')

# 布局控件
regex_label.grid(column=0, row=0, pady=(10, 10))
regex_entry.grid(column=1, row=0, pady=(10, 10))
option_label.grid(column=0, row=1, pady=(10, 10))
option_combobox.grid(column=1, row=1, pady=(10, 10))
submit_button.grid(column=0, row=2, columnspan=2, pady=(10, 20))


# 定义样式
style = ttk.Style()
style.configure('My.TFrame', background='#FFC0CB') 
style.configure('My.TLabel', background='#FFC0CB') 
style.configure('My.TButton', background='#FF69B4')  

# 调整窗口大小
root.geometry("350x200")

# 运行主循环
root.mainloop()


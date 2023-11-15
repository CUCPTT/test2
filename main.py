import io
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import re
import graphviz
from infix2postfix import infix_to_postfix
from postfix2nfa import str_to_nfa, generate_nfa
from NFA_to_DFA import nfa_to_dfa
from DFAMinimize import DFA_Minimize

class App:
    def __init__(self, master):
        self.master = master
        master.title('Experiment-2')
        master.configure(bg='#FFE4E1')

        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.master, padding='10', style='My.TFrame')
        self.frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.regex_label = ttk.Label(self.frame, text='INPUT:', style='My.TLabel')
        self.regex_entry = ttk.Entry(self.frame, width=30)
        self.option_label = ttk.Label(self.frame, text='SELECT:', style='My.TLabel')
        self.option_combobox = ttk.Combobox(self.frame, values=['NFA', 'DFA', 'Minimized DFA'], width=25)
        self.submit_button = ttk.Button(self.frame, text='Submit', command=self.submit_button_clicked, style='My.TButton')

        # 输出图片
        self.image_frame = ttk.Frame(self.master, style='My.TFrame')
        self.image_frame.grid(column=0, row=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 10))

        # 白色画布展示图片
        self.canvas = tk.Canvas(self.image_frame, bg="white", width=500, height=300, bd=2, relief=tk.SOLID)
        self.canvas.pack()

        # 样例正则表达式
        examples = ['a|b', 'a*b', '(a|b)*abb','(a|b)*','abc(a|b)*abd','a*b|a','a(b|c)*','ac(c|d)*','abc(a|c)*(a|d)*']
        self.example_buttons = []
        for i, example in enumerate(examples):
            button_text = f'{example}'
            button = ttk.Button(self.frame, text=button_text, command=lambda ex=example: self.set_example(ex), style='My.TButton')
            button.grid(column=3 + i % 3, row=i // 3, pady=(10, 10), padx=(0, 5))
            self.example_buttons.append(button)

        # 排列
        self.regex_label.grid(column=0, row=0, pady=(10, 10))
        self.regex_entry.grid(column=1, row=0, pady=(10, 10))
        self.option_label.grid(column=0, row=1, pady=(10, 10))
        self.option_combobox.grid(column=1, row=1, pady=(10, 10))
        self.submit_button.grid(column=0, row=2, columnspan=2, pady=(10, 20))

        # 样式
        style = ttk.Style()
        style.configure('My.TFrame', background='#FFE4E1')
        style.configure('My.TLabel', background='#FFE4E1')
        style.configure('My.TButton', background='#FF69B4')

        # 窗口大小
        self.master.geometry("650x550")

    def submit_button_clicked(self):
        regex = self.regex_entry.get()
        option = self.option_combobox.get()

        # 检查输入是否为空
        if not regex:
            messagebox.showerror('Empty regular expression', 'Please enter a regular expression.')
            return

        # 检查输入是否有效
        try:
            re.compile(regex)
        except re.error:
            messagebox.showerror('Invalid regular expression', 'Invalid regular expression. Please enter a valid one.')
            return

        # 调用相应函数
        if option == 'NFA':
            self.NFA(regex)
        elif option == 'DFA':
            self.DFA(regex)
        elif option == 'Minimized DFA':
            self.Min_DFA(regex)
        else:
            option = None
            messagebox.showerror('Invalid option', 'Invalid option. Please select NFA, DFA, or Minimized DFA.')
            return

    def create_graph(self, nodes, edges):
        dot = graphviz.Digraph(graph_attr={'rankdir': 'LR'})

        for node in nodes:
            if node[2] == 'begin':
                dot.node('begin_node', label='', shape='point')
                dot.edge('begin_node', str(node[0]), arrowhead='onormal')

            if node[3] == 'end':
                dot.node(str(node[0]), node[1], shape='doublecircle')
            else:
                dot.node(str(node[0]), node[1])

        for edge in edges:
            dot.edge(str(edge[0]), str(edge[1]), label=edge[2])

        dot.format = 'png'
        image_data = dot.pipe()
        if image_data:
            image = Image.open(io.BytesIO(image_data))
        else:
            image = Image.new("RGB", (1, 1), color="white")

        image.thumbnail((500, 300))

        # 清除之前的图片
        self.canvas.delete("all")

        # 展示新的图片
        img = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img

    def NFA(self, input_text):
        nodes, edges = generate_nfa(str_to_nfa(infix_to_postfix(input_text)))
        self.create_graph(nodes, edges)

    def DFA(self, input_text):
        nodes, edges = generate_nfa(str_to_nfa(infix_to_postfix(input_text)))
        nodes, edges = nfa_to_dfa(nodes, edges)
        self.create_graph(nodes, edges)

    def Min_DFA(self, input_text):
        nodes, edges = generate_nfa(str_to_nfa(infix_to_postfix(input_text)))
        nodes, edges = nfa_to_dfa(nodes, edges)
        nodes, edges = DFA_Minimize(nodes, edges)
        self.create_graph(nodes, edges)

    def set_example(self, example):
        self.regex_entry.delete(0, tk.END)
        self.regex_entry.insert(0, example)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import pdfminer.high_level
import re
import spacy
from spacy import displacy 
import time
from PIL import Image, ImageTk

nlp = spacy.load('ru_core_news_sm')

def extract_text_t(pdf_file: str):
    start_time = time.time()
    with open(pdf_file, 'rb') as pdf:
        pdf_text = pdfminer.high_level.extract_text(pdf_file)
    end_time = time.time()    
    execution_time = end_time - start_time
    print(f"Время получения содержимого файла: {execution_time} секунд")
    return pdf_text

def transfer():
    start_time = time.time()
    l1.configure(state=NORMAL)
    l1.delete('1.0', END)
    text = l2.get('1.0',END)
    text =re.split(r'[;?!.…]+',text.lower())
    text = list(set(text))
    
    for sentence in text:
        doc = nlp(sentence)
        Syntax = ""
        for token in doc:
            if token.pos_ != 'SPACE' and token.pos_ != 'PUNCT':
                Syntax+=token.text + ' '
                Syntax+=token.pos_ + ' '
                Syntax+=token.dep_ + ' '
                Syntax+='\n'
        l1.insert(END,Syntax + '\n\n\n')
        displacy.render(doc, style='dep')
    l1.configure(state=DISABLED)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения программы: {execution_time} секунд")

def insert_text():
    file_name = fd.askopenfilename()
    text = extract_text_t(file_name)
    l2.insert(END,text) 
    
def extract_text():
    file_name = fd.asksaveasfilename(
        filetypes=(("TXT files", "*.txt"),
                   ("HTML files", "*.html;*.htm"),
                   ("All files", "*.*")))
    f = open(file_name, 'w')
    s = l1.get(1.0, END)
    f.write(s)
    f.close()
    
def start(text):
    l1.configure(state=NORMAL)
    inputs_1 = l1.get('1.0', END)
    lines = inputs_1.splitlines()
    count = 0
    for line in lines:
        count+=1
        if text in line:
            buff = line
            lines.remove(line)
            lines.insert(0,buff)
    l1.delete('1.0',END)
    for line in lines:
        l1.insert(END,line + '\n')
    l1.configure(state=DISABLED)
    
def dismiss(window):
    window.grab_release() 
    window.destroy()
 
def click():
    window = Toplevel()
    window.title("Поиск")
    window.geometry("200x200")
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window)) 
    e = Entry(window,width=10)
    button = ttk.Button(window, text="Ввод", command=lambda: start(e.get()))
    e.pack(side= TOP,anchor="center")
    button.pack(anchor="center", expand=1)
    window.grab_set() 
    
    
def desh():
    
    window = Toplevel()
    window.title("Расшифровка")
    window.geometry("1920x1080")
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window))
    window.img = ImageTk.PhotoImage(Image.open("pu.png"))
    panel = Label(window, image=window.img)
    panel.pack(anchor="nw", fill="both", expand="no")
    l3 = Text(window,width=70,bg = 'white', font="Arial" ,wrap = 'word')

    l3.pack(side='left', anchor=S, fill = Y)
    f = open('text.txt', 'r',encoding="utf-8")
    for line in f:
        l3.insert(END, line + '\n')
    window.grab_set()               
    
def support():
    window = Toplevel()
    window.title("Помощь")
    window.geometry("1920x1080")
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window))
    window.img1 = ImageTk.PhotoImage(Image.open("pu2.jpg"))
    window.img2 = ImageTk.PhotoImage(Image.open("pu1.jpg"))
    window.img3 = ImageTk.PhotoImage(Image.open("pu3.jpg"))
    window.img4 = ImageTk.PhotoImage(Image.open("pu4.jpg"))
    panel1 = Label(window, image=window.img1)
    panel2 = Label(window, image=window.img2)
    panel3 = Label(window, image=window.img3)
    panel4 = Label(window, image=window.img4)
    lb1 = Label(window, font="Courier 15", text = '1. Первым делом нам необходимо выбрать файл, с которым будем работать.')
    lb2 = Label(window,font="Courier 15", text = '2. После того, как выбрали файл, при необходимости можно отредактировать \n текст или же сразу запустить синтаксический разбор.')
    lb3 = Label(window,font="Courier 15", text = '3. Получившийся результат может быть не очень понятным пользователю в виду \nнедостатка опыта или же комлексности самого предложения.')
    lb4 = Label(window,font="Courier 15", text = '4. Для избежания данной ситуации пользователь может перейти в раздел Расшифровка,\n чтобы пополнить свои знания или удостоверится в своём понимании.')
    panel1.grid(row = 0, column=0)
    panel2.grid(row = 1, column=0)
    panel3.grid(row = 2, column=0)
    panel4.grid(row = 3, column=0)
    lb1.grid(row = 0, column=1)
    lb2.grid(row = 1, column=1)
    lb3.grid(row = 2, column=1)
    lb4.grid(row = 3, column=1)

    window.grab_set()  
        
root = Tk()

mainmenu = Menu(root) 
root.config(menu=mainmenu)
segmentMenu = Menu(mainmenu, tearoff=0)
segmentMenu.add_command(label="Открыть файл", command=insert_text)
segmentMenu.add_command(label="Сохранить файл", command=extract_text)

mainmenu.add_cascade(label="Файл", menu=segmentMenu)

segmentMenu = Menu(mainmenu, tearoff=0)
segmentMenu.add_command(label="Разбор", command=transfer)
segmentMenu.add_command(label="Расшифровка", command=desh)
segmentMenu.add_command(label="Помощь", command=support)

mainmenu.add_cascade(label="Разбор", menu=segmentMenu)

l1 = Text(width=90,bg = 'white', font="Arial", state=DISABLED, wrap='none')
l2 = Text(width=70,bg = 'white', font="Arial", state=NORMAL ,wrap = 'word')
scrollbar = ttk.Scrollbar(orient="horizontal", command=l1.xview)
scrollbar.pack(side=BOTTOM, fill=X)

l2.pack(side='left', anchor=S, fill = Y)
l1.pack(side='right',anchor=E, fill = Y)
l1["xscrollcommand"]=scrollbar.set

root.mainloop()
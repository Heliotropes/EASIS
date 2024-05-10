from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import pdfminer.high_level
from collections import Counter
import re
import spacy
import pymorphy3
import time
import xml.etree.ElementTree as ET

nlp = spacy.load('ru_core_news_sm')
morph = pymorphy3.MorphAnalyzer()
texts = []
current_text_name = ''
data = []


def extract_text_t(pdf_file: str):
    start_time = time.time()
    with open(pdf_file, 'rb') as pdf:
        pdf_text = pdfminer.high_level.extract_text(pdf_file)
    end_time = time.time()    
    execution_time = end_time - start_time
    print(f"Время получения содержимого файла: {execution_time} секунд")
    return pdf_text

def morph_work(word):
    form = morph.parse(word)[0]
    form2 = str(form[1])     
    form1 = form[2]
    return form1,form2

def lex(word):
    morph_form = morph_work(word)
    label = Label(text=', lex = \'' +morph_form[0], fg="purple")
    l1.window_create(INSERT, window=label)
    
def gr(word):
    morph_form = morph_work(word)
    label = Label(text='\', gr = ' + morph_form[1], fg="green")
    l1.window_create(INSERT, window=label)
    
def count(word, dictionary):
    morph_form = morph_work(word)
    label = Label(text=', count = '+ str(dictionary[morph_form[0]]), fg="red")
    l1.window_create(INSERT, window=label)

def transfer():
    global data
    data = []
    start_time = time.time()
    l1.configure(state=NORMAL)
    l1.delete('1.0', END)
    text = l2.get('1.0',END)
    text =re.split(r'\s+|[,;?!.-»«…]\s*',text.lower())
    text = list(set(text))
    sorted(text)
    text.sort()
    text.pop(0)
    lemmas = []
    for word in text:
        lemmas.append(morph_work(word)[0])
    cnt = Counter(lemmas)
    dictionary = dict(cnt)
    morthy_list = []
    for word in text:
        morph_form = morph_work(word)
        morthy_list.append(morph_form)
        l1.insert(END,word)
        lex(word)
        gr(word)
        count(word, dictionary)
        l1.insert(END,'\n')
    data.append(text)
    data.append(lemmas)
    data.append(morthy_list)
    data.append(dictionary)
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
    
def extract_text_xml():
    file_name = fd.asksaveasfilename(
        filetypes=(("XML", "*.xml"),
                   ("HTML files", "*.html;*.htm"),
                   ("All files", "*.*")))
    first = ET.Element('data')
    count = 0
    for word in data[0]:
        pos = ET.SubElement(first,'word'+str(count + 1))
        text =ET.SubElement(pos,'text')
        lemma =ET.SubElement(pos,'lemma')
        morph =ET.SubElement(pos,'morph')
        number = ET.SubElement(pos,'count')
        text.text = data[0][count]
        lemma.text = data[1][count]
        morph.text = data[2][count][1]
        number.text =str(data[3][data[1][count]])
        count+=1
    tree = ET.ElementTree(first)
    tree.write(file_name, encoding='UTF-8')
 
    
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
    text = l2.get('1.0',END)
    text =re.split(r'\s+|[,;?!.-»«…]\s*',text.lower())
    text = list(set(text))
    sorted(text)
    text.sort()
    text.pop(0)
    lemmas = []
    for word in text:
        lemmas.append(morph_work(word)[0])
    cnt = Counter(lemmas)
    dictionary = dict(cnt)
    for line in lines:
        l1.insert(END,line)
        lex(line)
        gr(line)
        count(line, dictionary)
        l1.insert(END,'\n')
    l1.configure(state=DISABLED)
    
def dismiss(window):
    window.grab_release() 
    window.destroy()

def add_text():
    file_name = fd.askopenfilename()
    text = extract_text_t(file_name)
    global texts
    texts.append([file_name[21:], text])
    
def text_for_name(name):
    for text in texts:
        if text[0] == name:
            return text[1]
        
def on_click_del(event):
    button_text = event.widget.cget('text')
    global texts
    texts.remove([button_text, text_for_name(button_text)])
    
def on_click(event):
    global current_text_name
    button_text = event.widget.cget('text')
    current_text_name = button_text
    l2.delete('1.0', END)
    l2.insert(END,text_for_name(button_text)) 
    
    
def choose():
    global texts
    window = Toplevel()
    window.title("Выбор")
    window.geometry("200x200")
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window)) 
    for text in texts:
        button = ttk.Button(window, text=text[0])
        button.bind('<Button-1>', on_click)
        button.pack(anchor="center", expand=1)
    window.grab_set() 
    
def delete():
    global texts
    window = Toplevel()
    window.title("Удаление")
    window.geometry("200x200")
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window)) 
    for text in texts:
        button = ttk.Button(window, text=text[0])
        button.bind('<Button-1>', on_click_del)
        button.pack(anchor="center", expand=1)
    window.grab_set() 
    
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

def save():
    global texts
    for text in texts:
        if text[0] == current_text_name:
            text[1] = l2.get('1.0', END)   
    
        
root = Tk()

mainmenu = Menu(root) 
root.config(menu=mainmenu)
segmentMenu = Menu(mainmenu, tearoff=0)
segmentMenu.add_command(label="Открыть файл", command=insert_text)
segmentMenu.add_command(label="Сохранить файл", command=extract_text)
segmentMenu.add_command(label="Сохранить файл в xml", command=extract_text_xml)

mainmenu.add_cascade(label="Файл", menu=segmentMenu)

segmentMenu = Menu(mainmenu, tearoff=0)
segmentMenu.add_command(label="Разбор", command=transfer)
segmentMenu.add_command(label="Поиск", command=click)

mainmenu.add_cascade(label="Разбор", menu=segmentMenu)

segmentMenu = Menu(mainmenu, tearoff=0)
segmentMenu.add_command(label="Добавить текст", command=add_text)
segmentMenu.add_command(label="Удалить текст", command=delete)
segmentMenu.add_command(label="Сохранить текст", command=save)
segmentMenu.add_command(label="Выбрать текст", command=choose)

mainmenu.add_cascade(label="Текст", menu=segmentMenu)

l1 = Text(width=90,bg = 'white', font="Arial", state=DISABLED, wrap='none')
l2 = Text(width=70,bg = 'white', font="Arial",state = NORMAL, wrap = 'word')
scrollbar = ttk.Scrollbar(orient="horizontal", command=l1.xview)
scrollbar.pack(side=BOTTOM, fill=X)

l2.pack(side='left', anchor=S, fill = Y)
l1.pack(side='right',anchor=E, fill = Y)
l1["xscrollcommand"]=scrollbar.set

root.mainloop()
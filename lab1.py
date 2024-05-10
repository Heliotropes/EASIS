from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import pdfminer.high_level
import re
import spacy
import pymorphy3
import time

nlp = spacy.load('ru_core_news_sm')
morph = pymorphy3.MorphAnalyzer()

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
    if 'NOUN' in form2:
        if 'nomn' in form2:
            form2+=' (Subject or Predicate)'
        else:
            form2+=' (Object or Adverbial modifier or Attribute)'
    elif 'ADJF' in form2 or 'PRTF' in form2:
        form2+=' (Attribute)'
    elif 'ADJS' in form2 or 'PRTS' in form2 or 'PRED' in form2:
        form2+='(Predicate or Attribute)'
    elif 'COMP' in form2:    
        form2+='(Adverbial modifier or Attribute)'
    elif 'INFN' in form2:
        form2+='(Subject or Predicate or Attribute)'
    elif 'VERB' in form2 :
        form2+='(Predicate)'
    elif 'NPRO' in form2:
        if 'nomn' in form2:
            form2+=' (Subject or Predicate)'
        else:
            form2+=' (Object or Adverbial modifier)' 
    elif 'ADVB' in form2 or 'GRND'in form2:
        form2+='(Adverbial modifier)'        
    form1 = form[2]
    return form1,form2

def transfer():
    start_time = time.time()
    l1.configure(state=NORMAL)
    l1.delete('1.0', END)
    text = l2.get('1.0',END)
    text =re.split(r'\s+|[,;?!.-»«…]\s*',text.lower())
    text = list(set(text))
    text.sort()
    text.pop(0)
    
    for word in text:
        morph_form = morph_work(word)
        l1.insert(END,morph_form[0] + ', ' +word + ' - ' + morph_form[1] + '\n')
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
    
        
root = Tk()

mainmenu = Menu(root) 
root.config(menu=mainmenu)
segmentMenu = Menu(mainmenu, tearoff=0)
segmentMenu.add_command(label="Открыть файл", command=insert_text)
segmentMenu.add_command(label="Сохранить файл", command=extract_text)

mainmenu.add_cascade(label="Файл", menu=segmentMenu)

segmentMenu = Menu(mainmenu, tearoff=0)
segmentMenu.add_command(label="Разбор", command=transfer)
segmentMenu.add_command(label="Поиск", command=click)

mainmenu.add_cascade(label="Разбор", menu=segmentMenu)

l1 = Text(width=90,bg = 'white', font="Arial", state=DISABLED, wrap='none')
l2 = Text(width=70,bg = 'white', font="Arial", wrap = 'word')
scrollbar = ttk.Scrollbar(orient="horizontal", command=l1.xview)
scrollbar.pack(side=BOTTOM, fill=X)

l2.pack(side='left', anchor=S, fill = Y)
l1.pack(side='right',anchor=E, fill = Y)
l1["xscrollcommand"]=scrollbar.set

root.mainloop()
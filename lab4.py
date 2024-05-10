from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import pdfminer.high_level
import re
from nltk.corpus import wordnet
from deep_translator import GoogleTranslator
import time
from PIL import Image, ImageTk

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
        doc = sentence.split()
        synonym = 'SYNONIMS:\n\n'
        antonym = 'ANTONIMS:\n\n'
        for token in doc:
            synonym += token.upper() + ':\n\n'
            antonym += token.upper() + ':\n\n'
            synonyms = [] 
            antonyms = [] 
            for syn in wordnet.synsets(token): 
                for l in syn.lemmas(): 
                    synonyms.append(l.name()) 
                    if l.antonyms(): 
                        antonyms.append(l.antonyms()[0].name())
            for syn in set(synonyms):
                synonym+= syn + '\n'
            for ant in set(antonyms):
                antonym+= ant + '\n'                
            synonym+='\n\n'
            antonym+='\n\n'
        l1.insert(END,synonym + '\n\n\n')
        l1.insert(END,antonym + '\n\n\n')
        
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
    
    
def dismiss(window):
    window.grab_release() 
    window.destroy()
 
def click():
    window = Toplevel()
    window.title("Поиск")
    window.geometry("200x200")
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window)) 
    e = Entry(window,width=10)
    button = ttk.Button(window, text="Ввод")
    e.pack(side= TOP,anchor="center")
    button.pack(anchor="center", expand=1)
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
    lb2 = Label(window,font="Courier 15", text = '2. После того, как выбрали файл, при необходимости можно отредактировать \n текст или же сразу запустить поиск синонимов и антонимов.')
    lb3 = Label(window,font="Courier 15", text = '3. Получившийся результат изложен в довольно понятной пользователю форме,\n например в этом примере понятно что мы искали синонемы слова POOR .')
    lb4 = Label(window,font="Courier 15", text = '4. После получения результата пользователь может сохранить его.')
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

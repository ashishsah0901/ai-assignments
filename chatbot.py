import tkinter as tk
from tkinter import *
import random
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

text_contents=dict()
nltk.download('punkt',quiet=True)
with open('chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    text = fin.read().lower()
sentencelist=nltk.sent_tokenize(text)

def greet_res(text):
    text=text.lower()
    bot_greet=['hi','hello','hola','hey','howdy']
    usr_greet=['hi','hey','hello','hola','greetings','wassup','whats up']
    for word in text.split():
        if word in usr_greet:
            return random.choice(bot_greet)

def index_sort(list_var):
    length=len(list_var)
    list_index=list(range(0,length))
    x=list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp=list_index[i]
                list_index[i]=list_index[j]
                list_index[j]=temp
    return list_index

def bot_ress(usr_input):
    usr_input = usr_input.lower()
    sentencelist.append(usr_input)
    bot_res = ''
    cm = CountVectorizer().fit_transform(sentencelist)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0
    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_res = bot_res + ' ' + sentencelist[index[i]]
            response_flag = 1
            j = j + 1
        if j > 2:
            break
    if response_flag == 0:
        bot_res = bot_res + ' ' + 'I am sorry, I don\'t understand.'
    sentencelist.remove(usr_input)
    return bot_res

def widget_get():
    text_widget = root.nametowidget(textcon)
    return text_widget.get('1.0','end-1c')

exit_list = ['exit','break','quit','see you later','chat with you later','end the chat','bye','ok bye']

def send():
    usr_input = message.get()
    usr_input = usr_input.lower()
    textcon.insert(END, f'User: {usr_input}'+'\n','usr')
    if usr_input in exit_list:
        textcon.config(fg='black')
        textcon.insert(END,"Bot:Ok bye! Chat with you later\n")
        return root.destroy()
    else:
        textcon.config(fg='black')
        if greet_res(usr_input) != None:
            lab=f"Bot: {greet_res(usr_input)}"+'\n'
            textcon.insert(END,lab)
        else:
            lab = f"Bot: {bot_ress(usr_input)}"+'\n'
            textcon.insert(END, lab)

root=tk.Tk()
filename="Untitled.txt"
root.title(f"Chat Bot - Untitled.txt")
root.geometry('500x400')
root.resizable(False, False)
message=tk.StringVar()
chat_win=Frame(root,width=50,height=8)
chat_win.place(x=6,y=6,height=300,width=480)
textcon=tk.Text(chat_win,width=50,height=8)
textcon.pack(fill="both",expand=True)
mes_win=Entry(root,width=30,xscrollcommand=True,textvariable=message)
mes_win.place(x=6,y=310,height=60,width=366)
mes_win.focus()
mssg=mes_win.get()
button=Button(root,text='Send',command=send,width=12,height=5)
button.place(x=376,y=310,height=60,width=110)
content = widget_get()
text_contents[str(textcon)] = hash(content)
root.mainloop()
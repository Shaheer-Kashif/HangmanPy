from tkinter import *
from PIL import ImageTk,Image
import requests,json
import random

root = Tk()
root.title("Hangman")
root.iconbitmap("icons/hangman.ico")

category = ["noun", "verb", "adjective", "adverb"]

logo_large = (Image.open("icons/hangman.ico")).resize((100,100))
logo = ImageTk.PhotoImage(logo_large)

top_frame = Frame(root)
top_frame.pack(side="top", fill="both", expand=True)

LogoWindow = Frame(top_frame,borderwidth=0)
LogoWindow.pack(side="left")

Logo = Label(LogoWindow, image=logo)
Logo.grid(row=0,column=0,padx=15)


LogoText = Frame(top_frame,borderwidth=0)
LogoText.pack(side="left")

GameName = Label(LogoText,text="Hangman",font=("Bebas Neue",42))
GameName.grid(row=0,column=0)

Slogan = Label(LogoText,text="Can you save the poor soul?",font=("Montserrat",12))
Slogan.grid(row=1,column=0)

def wordcheck(guessed_letter):
    global word,word_label,hidden_word
    
    for index,letter in enumerate(word):
        if guessed_letter==letter:
            hidden_word[index] = word[index] 
    word_label.config(text=hidden_word)
    
    

def play():
    global category,hidden_word,word,word_label
    final_category = random.choice(category)
    
    api_req = requests.get("https://api.api-ninjas.com/v1/randomword?type="+final_category, headers={'X-Api-Key': 'l203bJ+LLJJR4qvW9AJtHg==28WMMOp820Oi9cAx'})
    api = json.loads(api_req.content)
    
    word = [x for x in api['word'][0]]
    print(word)

    game_window = Toplevel()
    upperframe = LabelFrame(game_window)
    upperframe.grid(row=0,column=0)
    
    hidden_word = ["_" for letter in word]
        
    word_label = Label(upperframe,text=hidden_word)
    word_label.grid(row=0,column=0)
    
    category_label = Label(upperframe,text=final_category)
    category_label.grid(row=1,column=0)
    
    keyboard = LabelFrame(game_window)
    keyboard.grid(row=1,column=0)
    for i in range(26):
        letter = chr(ord('A') + i)
        locals()["button_"+letter] = Button(keyboard,text=letter,command=lambda le = letter.lower(): wordcheck(le))
        locals()["button_"+letter].grid(row=i//8,column=i%8)
    
    
    
    


ButtonWindow = Frame(root,borderwidth=1)
ButtonWindow.pack(fill="both", expand=True)

playbutton = Button(ButtonWindow,text="Play",font=("Montserrat",14,"bold"),command=play,width=25,background="#27e152",fg="white",borderwidth=0, relief='raised')
playbutton.grid(row=0,column=0,columnspan=2,padx=(25,0),pady=(20,0))

statsbutton = Button(ButtonWindow,text="Stats",font=("Montserrat",14,"bold"),width=25,background="#27aae1",fg="white",borderwidth=0, relief='raised')
statsbutton.grid(row=1,column=0,columnspan=2,padx=(25,0),pady=(10,0))

settings = Button(ButtonWindow,text="Settings",font=("Montserrat",14,"bold"),width=12,background="#27aae1",fg="white",borderwidth=0, relief='raised')
settings.grid(row=2,column=0,padx=(21,0),pady=10)

quit = Button(ButtonWindow,text="Quit",command=quit,font=("Montserrat",14,"bold"),width=11,background="#ff5757",fg="white",borderwidth=0, relief='raised')
quit.grid(row=2,column=1,padx=(12,0),pady=10)



root.mainloop()
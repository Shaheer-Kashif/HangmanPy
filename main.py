from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
from os import system

root = Tk()
root.title("Hangman")
root.iconbitmap("icons/hangman.ico")

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

def play():
    pass


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
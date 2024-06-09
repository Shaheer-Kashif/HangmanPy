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

playbutton = Button(ButtonWindow,text="Play",font=("Montserrat",14,"bold"),command=play,width=40)
playbutton.grid(row=0,column=0,columnspan=2,padx=(45,0))

statsbutton = Button(ButtonWindow,text="Stats",width=40)
statsbutton.grid(row=1,column=0,columnspan=2,padx=(45,0))

settings = Button(ButtonWindow,text="Settings")
settings.grid(row=2,column=0)

quit = Button(ButtonWindow,text="Quit",command=quit)
quit.grid(row=2,column=1)



root.mainloop()
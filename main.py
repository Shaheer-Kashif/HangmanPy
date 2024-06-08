from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
from os import system

root = Tk()
root.title("Hangman")
root.geometry("960x540")
root.iconbitmap("icons/hangman.ico")

logo_large = (Image.open("icons/hangman.ico")).resize((100,100))
logo = ImageTk.PhotoImage(logo_large)

LogoWindow = LabelFrame(root,borderwidth=0)
LogoWindow.grid(row=0,column=0)

Logo = Label(LogoWindow, image=logo)
Logo.grid(row=0,column=0,padx=15)

LogoText = LabelFrame(root,borderwidth=0)
LogoText.grid(row=0,column=1)
GameName = Label(LogoText,text="Hangman",font=("Bebas Neue",42))
GameName.grid(row=0,column=0)

Slogan = Label(LogoText,text="Can you save the poor soul?",font=("Montserrat",10))
Slogan.grid(row=1,column=0)



root.mainloop()
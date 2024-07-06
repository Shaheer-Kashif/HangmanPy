from tkinter import *
from PIL import ImageTk,Image
import requests,json
import random
from tkinter import messagebox

# from tkvideo

root = Tk()
root.title("Hangman")
root.iconbitmap("icons/hangman.ico")

logo = ImageTk.PhotoImage(Image.open("icons/hangman.ico").resize((100,100)))

top_frame = Frame(root)
top_frame.pack(side="top", fill="both", expand=True)

default_image = ImageTk.PhotoImage(Image.open("media/default.png").resize((360,300)))

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

def animate1(path):
    global showAnimation,imageObject,frames
    openImage = Image.open(path)
    frames = openImage.n_frames
    
    imageObject = [PhotoImage(file=path,format=f"gif -index {i}") for i in range(frames)]
    
    count = 0
    showAnimation = None
    animate2(count,path)
    
    
def animate2(count,path):
    global showAnimation
    newImage = imageObject[count]
    
    image_placeholder.configure(image=newImage)
    count += 1
    
    if path == "media/win.gif" or path == "media/loose.gif":
        if count == frames:
            count = 0
            showAnimation = root.after(50, lambda: animate2(count,path))
    else:
        if count != frames:
            showAnimation = root.after(50, lambda: animate2(count,path))
    
    
def wordcheck(guessed_letter):
    global lives,word,hidden_word,word_label,game_window
    globals()["button_"+guessed_letter].config(state=DISABLED)
    if guessed_letter in word:
        for index,letter in enumerate(word):
            if guessed_letter==letter:
                hidden_word[index] = word[index] 
        word_label.config(text=hidden_word)
        
        if "".join(hidden_word) == word:
            animate1("media/win.gif")
            messagebox.showinfo("Congratulations","You guessed the word correctly!")
            game_window.destroy()
    else:
        if lives == 1:
            animate1("media/loose.gif")
            messagebox.showerror("Game Over","All the Lives are lost!")
            game_window.destroy()
        animate1("media/"+str(6-(lives-1))+".gif")
        lives -= 1
        lives_label.config(text="Lives: "+str(lives))
        
    
def play():
    global lives,category,hidden_word,word,word_label,lives_label,game_window,keyboard,default_image,image_placeholder
    
    category = requests.get("https://www.wordgamedb.com/api/v1/categories")
    category = json.loads(category.content)
    
    final_category = random.choice(category)
    
    api_req = requests.get("https://www.wordgamedb.com/api/v1/words/?category="+final_category)
    api = json.loads(api_req.content)
    random_ele = random.randrange(len(api))
    word = api[random_ele]['word']
    hint = api[random_ele]['hint']
    
    lives = 6
    
    game_window = Toplevel()
    
    hangman = LabelFrame(game_window,width=600,height=200)
    hangman.grid(row=0,column=0,rowspan=2)
    
    image_placeholder = Label(hangman,image=default_image)
    image_placeholder.pack()
    
    upperframe = LabelFrame(game_window,width=600,height=200)
    upperframe.grid(row=0,column=1)
    
    hidden_word = ["_" for letter in word]
        
    word_label = Label(upperframe,text=hidden_word,font=("Montserrat",18,"bold"))
    word_label.grid(row=0,column=0)
    
    category_label = Label(upperframe,text="Category: "+final_category)
    category_label.grid(row=1,column=1)
    
    lives_label = Label(upperframe,text="Lives: "+str(lives))
    lives_label.grid(row=2,column=0)
    
    hint_label = Label(upperframe,text="Hint: "+hint)
    hint_label.grid(row=3,column=0)
    
    
    keyboard = LabelFrame(game_window)
    keyboard.grid(row=1,column=1)
    for i in range(26):
        letter = chr(ord('a') + i)
        globals()["button_"+letter] = Button(keyboard,text=letter.upper(),command=lambda le = letter: wordcheck(le),width=5)
        globals()["button_"+letter].grid(row=i//7,column=i%7)
    
    
    
    


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
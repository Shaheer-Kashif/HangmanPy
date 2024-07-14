from tkinter import *
from PIL import ImageTk,Image
import requests,json
import time
from tkinter import messagebox
import pygame
import threading

# from tkvideo

root = Tk()
root.title("Hangman")
root.iconbitmap("icons/hangman.ico")

logo = ImageTk.PhotoImage(Image.open("icons/hangman.ico").resize((100,100)))

top_frame = Frame(root)
top_frame.pack(side="top", fill="both", expand=True)

default_image = ImageTk.PhotoImage(Image.open("media/default.png").resize((360,300)))

quit_button_image = ImageTk.PhotoImage(Image.open("media/icons/logout.png"))
replay_button_image = ImageTk.PhotoImage(Image.open("media/icons/replay.png"))
hint_image = ImageTk.PhotoImage(Image.open("media/icons/light-bulb.png"))
lives_image = ImageTk.PhotoImage(Image.open("media/icons/heart.png"))

# Loading Sounds
pygame.mixer.init()

win_sound = pygame.mixer.Sound('media/win.wav')
lose_sound = pygame.mixer.Sound('media/lose.wav')

wrong_key_sound = pygame.mixer.Sound('media/wrong.wav')
right_key_sound = pygame.mixer.Sound('media/right.wav')


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
        if count < frames:
            showAnimation = root.after(50, lambda: animate2(count,path))
    
def soundplay(sound_type):
    temp = pygame.mixer.Sound('media/'+sound_type+'.wav')
    temp.play()
    
def func_buttons(button_type):
    global hint
    if button_type == 'hint':
        if len(hint) > 7:
            hint = hint[0:7] + hint[7:].replace(" ","\n",1)
        Label(button_frame,text=hint,height=3,font=("montserrat",10)).grid(row=0,column=0,padx=10)
    elif button_type == 'replay':
        game_window.destroy()
        play()
    else:
        game_window.destroy()
        
    
def wordcheck(guessed_letter):
    global lives,word,hidden_word,word_label,game_window
    globals()["button_"+guessed_letter].config(state=DISABLED,disabledforeground="white", bg="#96E0FF")
    if guessed_letter in word:
        t1 = threading.Thread(target=soundplay, args=('right',))
        t1.start()
        for index,letter in enumerate(word):
            if guessed_letter==letter:
                hidden_word[index] = word[index] 
        word_label.config(text=hidden_word)
        
        if "".join(hidden_word) == word:
            animate1("media/win.gif")
            t1 = threading.Thread(target=soundplay, args=('win',))
            t1.start()
            
            replay_text.config(text="Would you like to play again?",font=("Montserrat",12))
            
            yes_button = Button(replay_menu,text="Yes",border=0,width=5,bg="#27e152",fg="white",command=lambda: func_buttons('replay'),font=("montserrat",16,"bold"))
            yes_button.grid(row=1,column=0,pady=5)   
            
            no_button = Button(replay_menu,text="No",border=0,width=5,bg="#ff5757",fg="white",command=lambda: func_buttons('quit'),font=("montserrat",16,"bold"))
            no_button.grid(row=1,column=1,pady=5)      
            
    else:
        lives -= 1
        if lives <= 0:
            animate1("media/loose.gif")
            t1 = threading.Thread(target=soundplay, args=('lose',))
            t1.start()
            
            replay_text.config(text="Would you like to play again?",font=("Montserrat",12))
            
            yes_button = Button(replay_menu,text="Yes",border=0,width=5,bg="#27e152",fg="white",command=lambda: func_buttons('replay'),font=("montserrat",16,"bold"))
            yes_button.grid(row=1,column=0,pady=5)   
            
            no_button = Button(replay_menu,text="No",border=0,width=5,bg="#ff5757",fg="white",command=lambda: func_buttons('quit'),font=("montserrat",16,"bold"))
            no_button.grid(row=1,column=1,pady=5)      
            
        else:
            t1 = threading.Thread(target=soundplay, args=('wrong',))
            t1.start()
            animate1("media/"+str(6-(lives-1))+".gif")
        lives_text.config(text=lives)
        
    
def play():
    global lives,category,hidden_word,word,word_label,lives_text,game_window,keyboard,default_image,image_placeholder,hint,hint_button,button_frame,replay_menu,replay_text
    
    api_req = requests.get("https://www.wordgamedb.com/api/v1/words/random")
    api = json.loads(api_req.content)
    word = api['word']
    hint = api['hint']
    category = api['category']
    
    lives = 6
    
    game_window = Toplevel()
    
    hangman = LabelFrame(game_window,width=600,height=200,border=0)
    hangman.grid(row=0,column=0,rowspan=3)
    
    image_placeholder = Label(hangman,image=default_image)
    image_placeholder.pack()
    
    upperframe = LabelFrame(game_window,width=800,height=300,padx=100,border=0)
    upperframe.grid(row=0,column=1)
    
    hidden_word = ["_" for letter in word]

    word_label = Label(upperframe,text=hidden_word,font=("Montserrat",18,"bold"))
    word_label.grid(row=1,column=0,columnspan=2)
    
    category_frame = LabelFrame(upperframe,border=0)
    category_frame.grid(row=2,column=0,columnspan=2)
    
    category_label = Label(category_frame,text="Category: ",font=("Montserrat",13,"bold"))
    category_label2 = Label(category_frame,text=category,font=("Montserrat",12))
    
    category_label.grid(row=0,column=0)
    category_label2.grid(row=0,column=1)
    
    lives_frame = LabelFrame(upperframe,border=0)
    lives_frame.grid(row=0,column=0,columnspan=2)
    
    lives_label = Label(lives_frame,image=lives_image)
    lives_label.grid(row=0,column=0)
    
    lives_text = Label(lives_frame,text=lives,font=("Montserrat",12,"bold"))
    lives_text.grid(row=0,column=1)
    
    button_frame = LabelFrame(game_window,border=0)
    button_frame.grid(row=1,column=1,pady=10)
    
    hint_button = Button(button_frame,image=hint_image,border=0,command=lambda: func_buttons('hint'))
    hint_button.grid(row=0,column=0,padx=10)
    
    replay_button = Button(button_frame,image=replay_button_image,border=0,command=lambda: func_buttons('replay'))
    replay_button.grid(row=0,column=1,padx=10)
    
    quit_button = Button(button_frame,image=quit_button_image,border=0,command=lambda: func_buttons('quit'))
    quit_button.grid(row=0,column=2,padx=10)
    
    keyboard = LabelFrame(game_window,border=0)
    keyboard.grid(row=2,column=1)
    
    replay_menu = LabelFrame(game_window,border=0)
    replay_menu.grid(row=3,column=0,columnspan=2,pady=10)
            
    replay_text = Label(replay_menu)
    replay_text.grid(row=0,column=0,columnspan=2)
    
    temp = Button(keyboard,text="  ",width=3,border=0,background="#27aae1",foreground="white",font="montserrat")
    temp.grid(row=3,column=1)
    
    for i in range(26):
        letter = chr(ord('a') + i)
        globals()["button_"+letter] = Button(keyboard,text=letter.upper(),command=lambda le = letter: wordcheck(le),width=3,border=0,background="#27aae1",foreground="white",font="montserrat")
        
        if i >= 21:
            globals()["button_"+letter].grid(row=(i+1)//7,column=(i+1)%7,padx=5,pady=5)
        else:
            globals()["button_"+letter].grid(row=i//7,column=i%7,padx=5,pady=5)
    
    
    
LogoWindow = Frame(top_frame,borderwidth=0)
LogoWindow.pack(side="left")

Logo = Label(LogoWindow, image=logo)
Logo.grid(row=0,column=0,padx=15)


LogoText = Frame(top_frame,borderwidth=0)
LogoText.pack(side="left")

GameName = Label(LogoText,text="Hangman",font=("Bebas Neue",42))
GameName.grid(row=0,column=0)

Slogan = Label(LogoText,text="Can you save the poor soul?",font=("Montserrat",11))
Slogan.grid(row=1,column=0)
    
    
ButtonWindow = Frame(root,borderwidth=1)
ButtonWindow.pack(fill="both", expand=True)

playbutton = Button(ButtonWindow,text="Play",font=("Montserrat",14,"bold"),command=play,width=25,bg="#27e152",fg="white",borderwidth=0, relief='raised')
playbutton.grid(row=0,column=0,columnspan=2,padx=(25,0),pady=(20,0))

statsbutton = Button(ButtonWindow,text="Stats",font=("Montserrat",14,"bold"),width=25,background="#27aae1",fg="white",borderwidth=0, relief='raised')
statsbutton.grid(row=1,column=0,columnspan=2,padx=(25,0),pady=(10,0))

settings = Button(ButtonWindow,text="Settings",font=("Montserrat",14,"bold"),width=12,background="#27aae1",fg="white",borderwidth=0, relief='raised')
settings.grid(row=2,column=0,padx=(21,0),pady=10)

quit = Button(ButtonWindow,text="Quit",command=quit,font=("Montserrat",14,"bold"),width=11,background="#ff5757",fg="white",borderwidth=0, relief='raised')
quit.grid(row=2,column=1,padx=(12,0),pady=10)



root.mainloop()
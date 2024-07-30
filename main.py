from tkinter import *
from PIL import ImageTk,Image
import requests,json
import pygame, threading, time
from tkinter import messagebox
from os import remove
from sys import exit

root = Tk()
root.config(padx=10)
root.title("Hangman")

# Loading Hangman Icon
root.iconbitmap("icons/hangman.ico")

window_width = 380
window_height = 300

# Set the window size
root.geometry(f"{window_width}x{window_height}")

# Lock the window size by setting minsize and maxsize to the same value
root.minsize(window_width, window_height)
root.maxsize(window_width, window_height)

# Loading all Relevant Images
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

button_press = pygame.mixer.Sound('media/button_press.mp3')

# Stats Files and Variables
try:
    s1 = open("stats.txt","r")
    stats = s1.readlines()[0]
    win,loss,right,wrong = stats.split(",")
    win = int(win)
    loss = int(loss)
    right = int(right)
    wrong = int(wrong)
except Exception:
    win = 0
    loss = 0
    right = 0
    wrong = 0
    s1 = open("stats.txt","w")
    s1.write(str(win)+","+ str(loss)+","+ str(right)+","+ str(wrong))
    s1.flush()

# Stats Update
def stats_update():
    global win,loss,right,wrong,s1
    s1.close()
    remove("stats.txt")
    s1 = open("stats.txt","w")
    s1.write(str(win)+","+ str(loss)+","+ str(right)+","+ str(wrong))
    s1.flush()
    
# Music Properties
bg_music = pygame.mixer.Sound('media/bg-music.mp3')
    
# defining variables for transition
initial_volume = 0.2
final_volume = 0.05
fade_duration = 2  # 3 seconds
steps = 100
step_duration = fade_duration / steps
transition_game = False
transition_menu = False

bg_music.set_volume(initial_volume)
bg_music.play()

    
# Animation Player of Gifs
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
    try:
        if path == "reset":
            root.after_cancel(showAnimation)
            image_placeholder.config(image=default_image)
        else:
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
    except:
        pass
    
          
# Certain SFX Playing Function  
def soundplay(sound_type):
    sfx = pygame.mixer.Sound('media/'+sound_type+'.wav')
    sfx.set_volume(0.7)
    sfx.play()
    
# Game Function Buttons
def func_buttons(button_type):
    global hint
    stats_update()
    button_press.play()
    if button_type == 'hint':
        if len(hint) > 7:
            hint = hint[0:7] + hint[7:].replace(" ","\n",1)
        Label(button_frame,text=hint,height=3,font=("montserrat",10)).grid(row=0,column=0,padx=10)
    elif button_type == 'replay':
        game_window.destroy()
        play()
        animate2(2,"reset")
    else:
        game_window.destroy()
        

# Game Logic
def wordcheck(guessed_letter):
    global lives,word,hidden_word,word_label,game_window,win,loss,right,wrong
    globals()["button_"+guessed_letter].config(state=DISABLED,disabledforeground="white", bg="#96E0FF")
    if guessed_letter in word:
        right += 1
        t1 = threading.Thread(target=soundplay, args=('right',))
        t1.start()
        for index,letter in enumerate(word):
            if guessed_letter==letter:
                hidden_word[index] = word[index] 
        word_label.config(text=hidden_word)
        
        if "".join(hidden_word) == word:
            
            animate1("media/win.gif")
            win += 1
            t1 = threading.Thread(target=soundplay, args=('win',))
            t1.start()
            
            replay_text.config(text="You Win!, Would you like to play again?",font=("Montserrat",12))
            
            yes_button = Button(replay_menu,text="Yes",border=0,width=5,bg="#27e152",fg="white",command=lambda: func_buttons('replay'),font=("montserrat",16,"bold"))
            yes_button.grid(row=1,column=0,pady=5)   
            
            no_button = Button(replay_menu,text="No",border=0,width=5,bg="#ff5757",fg="white",command=lambda: func_buttons('quit'),font=("montserrat",16,"bold"))
            no_button.grid(row=1,column=1,pady=5)   
            
            stats_update()   
            
    else:
        lives -= 1
        if lives <= 0:
            animate1("media/loose.gif")
            wrong += 1
            loss += 1
            t1 = threading.Thread(target=soundplay, args=('lose',))
            t1.start()
            
            replay_text.config(text="You lose, The word was: "+word+"\nWould you like to play again?",font=("Montserrat",12))
            
            yes_button = Button(replay_menu,text="Yes",border=0,width=5,bg="#27e152",fg="white",command=lambda: func_buttons('replay'),font=("montserrat",16,"bold"))
            yes_button.grid(row=1,column=0,pady=5)   
            
            no_button = Button(replay_menu,text="No",border=0,width=5,bg="#ff5757",fg="white",command=lambda: func_buttons('quit'),font=("montserrat",16,"bold"))
            no_button.grid(row=1,column=1,pady=5)      
            
            stats_update()
            
        else:
            wrong += 1
            t1 = threading.Thread(target=soundplay, args=('wrong',))
            t1.start()
            animate1("media/"+str(6-(lives-1))+".gif")
        lives_text.config(text=lives)
        

# Main Screen Load
def play():
    global game_window,credits_window,stats_window,lives,category,hidden_word,word,word_label,lives_text,game_window,keyboard,default_image,image_placeholder,hint,hint_button,button_frame,replay_menu,replay_text,word
    
    try:
        if game_window.winfo_exists():
            messagebox.showerror("Error","An another instance of the application is already running.")
        raise Exception
    except:
 
        # Check if Stats and Credits Windows are Opened.
        try:
            if stats_window.winfo_exists():
                stats_window.destroy()
            if credits_window.winfo_exists():
                credits_window.destroy()
        except:
            try:
                if credits_window.winfo_exists():
                    credits_window.destroy()
            except:
                pass
            pass
        
        # Check if APi Loads otherwise return an error
        try:
            api_req = requests.get("https://www.wordgamedb.com/api/v1/words/random")
        except:
            messagebox.showerror("Error","There was an issue launching the application, maybe check your Internet?")
            exit()
            
        
        api = json.loads(api_req.content)
        word = api['word']
        hint = api['hint']
        category = api['category']
        
        lives = 6
        
        game_window = Toplevel()
        
        game_window_width = 720
        game_window_height = 430

        # Set the window size
        game_window.geometry(f"{game_window_width}x{game_window_height}")

        # Lock the window size by setting minsize and maxsize to the same value
        game_window.minsize(game_window_width, game_window_height)
        game_window.maxsize(game_window_width, game_window_height)
        
        mus_check = threading.Thread(target=eventcheckbgmusic)
        mus_check.start()
        
        hangman = LabelFrame(game_window,width=600,height=200,border=0)
        hangman.grid(row=0,column=0,rowspan=3)
        
        image_placeholder = Label(hangman,image=default_image)
        image_placeholder.pack()
        
        upperframe = LabelFrame(game_window,width=350,height=100,padx=100,border=0)
        upperframe.grid_propagate(0)
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
        
        button_frame = LabelFrame(game_window,border=0,height=50,width=250)
        button_frame.grid(row=1,column=1,pady=10)
        
        hint_button = Button(button_frame,image=hint_image,border=0,command=lambda: func_buttons('hint'), height=50)
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
            
# Background Music Playing Function
def eventcheckbgmusic():
    global game_window,transition_game,transition_menu
    
    try:
        while True:
            if game_window.winfo_exists():
                if transition_game == False:
                    for step in range(steps):
                        new_volume = initial_volume - (initial_volume - final_volume) * (step + 1) / steps
                        bg_music.set_volume(new_volume)
                        time.sleep(step_duration)
                    transition_game = True
                    transition_menu = False
            else:
                if transition_menu == False:
                    for step in range(steps):
                        new_volume = final_volume - (final_volume - initial_volume) * (step + 1) / steps
                        bg_music.set_volume(new_volume)
                        time.sleep(step_duration)
                    
                    transition_menu = True
                    transition_game = False
            time.sleep(.1)
    except:
        pass
    
# Stats Menu
def stats_menu():
    global stats_window
    stats_window = Toplevel(padx=10,pady=10)
    
    stats_window_width = 215
    stats_window_height = 180

    # Set the window size
    stats_window.geometry(f"{stats_window_width}x{stats_window_height}")

    # Lock the window size by setting minsize and maxsize to the same value
    stats_window.minsize(stats_window_width, stats_window_height)
    stats_window.maxsize(stats_window_width, stats_window_height)
    
    heading = Label(stats_window,text="All Time Stats",font=("Montserrat",20,"bold"),foreground="#27aae1")
    heading.grid(row=0,column=0,columnspan=2)
    
    win_label = Label(stats_window,text="Wins:",font=("Montserrat",12))
    win_label.grid(row=1,column=0,sticky="w")
    
    win_label2 = Label(stats_window,text=str(win),font=("Montserrat",15,"bold"))
    win_label2.grid(row=1,column=1,sticky="e")
    
    lose_label = Label(stats_window,text="Loses:",font=("Montserrat",12))
    lose_label.grid(row=2,column=0,sticky="w")
    
    lose_label = Label(stats_window,text=str(loss),font=("Montserrat",15,"bold"))
    lose_label.grid(row=2,column=1,sticky="e")
    
    right_label = Label(stats_window,text="Right Guesses:",font=("Montserrat",12))
    right_label.grid(row=3,column=0,sticky="w")
    
    right_label2 = Label(stats_window,text=str(right),font=("Montserrat",15,"bold"))
    right_label2.grid(row=3,column=1,sticky="e")
    
    wrong_label = Label(stats_window,text="Wrong Guesses:",font=("Montserrat",12))
    wrong_label.grid(row=4,column=0,sticky="w")
    
    wrong_label = Label(stats_window,text=str(wrong),font=("Montserrat",15,"bold"))
    wrong_label.grid(row=4,column=1,sticky="e")

def credits_menu():
    global credits_window
    credits_window = Toplevel(padx=10,pady=10)
    
    credits_window_width = 270
    credits_window_height = 100

    # Set the window size
    credits_window.geometry(f"{credits_window_width}x{credits_window_height}")

    # Lock the window size by setting minsize and maxsize to the same value
    credits_window.minsize(credits_window_width, credits_window_height)
    credits_window.maxsize(credits_window_width, credits_window_height)
    
    heading = Label(credits_window,text="Made By",font=("Montserrat",20,"bold"),foreground="#27aae1")
    heading.grid(row=0,column=0,columnspan=2)
    
    name_label = Label(credits_window,text="Shaheer Codes",font=("Montserrat",24))
    name_label.grid(row=1,column=0)
    
def main_buttons(type):
    button_press.play()
    if type == "play":
        play()
    elif type == "stats":
        stats_menu()
    elif type == "credits":
        credits_menu()
    

    
    
# Main Menu
LogoWindow = Frame(top_frame,borderwidth=0)
LogoWindow.pack(side="left")

Logo = Label(LogoWindow, image=logo)
Logo.grid(row=0,column=0,padx=15)

LogoText = Frame(top_frame,borderwidth=0)
LogoText.pack(side="left")

GameName = Label(LogoText,text="Hangman",font=("Montserrat",31))
GameName.grid(row=0,column=0)

Slogan = Label(LogoText,text="Can you save the poor soul?",font=("Montserrat",11))
Slogan.grid(row=1,column=0)
    
ButtonWindow = Frame(root,borderwidth=1)
ButtonWindow.pack(fill="both", expand=True)

playbutton = Button(ButtonWindow,text="Play",font=("Montserrat",14,"bold"),command= lambda: main_buttons("play"),width=25,bg="#27e152",fg="white",borderwidth=0, relief='raised')
playbutton.grid(row=0,column=0,columnspan=2,padx=(25,0),pady=(20,0))

statsbutton = Button(ButtonWindow,text="Stats",font=("Montserrat",14,"bold"),command= lambda: main_buttons("stats"), width=25,background="#27aae1",fg="white",borderwidth=0, relief='raised')
statsbutton.grid(row=1,column=0,columnspan=2,padx=(25,0),pady=(10,0))

settings = Button(ButtonWindow,text="Credits",font=("Montserrat",14,"bold"),command= lambda: main_buttons("credits"),width=12,background="#27aae1",fg="white",borderwidth=0, relief='raised')
settings.grid(row=2,column=0,padx=(24,0),pady=10)

quit = Button(ButtonWindow,text="Quit",command=exit,font=("Montserrat",14,"bold"),width=11,background="#ff5757",fg="white",borderwidth=0, relief='raised')
quit.grid(row=2,column=1,padx=(14,0),pady=10)


root.mainloop()
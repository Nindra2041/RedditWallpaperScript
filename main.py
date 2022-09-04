#!/usr/bin/python3
from pynput.keyboard import Key, Listener, KeyCode
import os
import praw
from tkinter import *
from tkinter import messagebox as msg

reddit = praw.Reddit(
    client_id="your client id",
    client_secret="your client secret",
    user_agent="script desc"
)


state = True
SUB = 'sunset'

def setBkgOpt(conf):
    #print(conf['value'])
    os.system(conf['value'])
def conf():
    root = Tk()
    root.title('Config')
    posR = int(root.winfo_screenwidth() / 2 - 500 / 2)
    posD = int(root.winfo_screenheight() / 2 - 300 / 2)
    root.geometry(f"500x300+{posR}+{posD}")
    title = Label(root, text="\nConfig", font=("Arial", 19, "underline")).pack()
    value = StringVar()

    rb1 = Radiobutton(
        root,
        text='Default (zoom)',
        value='gsettings reset org.gnome.desktop.background picture-options',
        variable=value,
        command=lambda : setBkgOpt(rb1)
    )
    rb2 = Radiobutton(
        root,
        text='Scaled (see whole pic)',
        value='gsettings set org.gnome.desktop.background picture-options \"scaled\"',
        variable=value,
        command=lambda: setBkgOpt(rb2)
    )
    rb3 = Radiobutton(
        root,
        text='Centered',
        value='gsettings set org.gnome.desktop.background picture-options \"centered\"',
        variable=value,
        command=lambda: setBkgOpt(rb3)
    )
    rb1.pack()
    rb2.pack()
    rb3.pack()

    confBtn = btn = Button(root, text='Save and Exit', command=lambda: [root.destroy()]).pack()
    infoBtn = btn = Button(root, text='Back', command=lambda: [root.destroy(), info()]).pack()

def info():
    root = Tk()
    posR = int(root.winfo_screenwidth()/2 - 500/2)
    posD = int(root.winfo_screenheight()/2 - 300/2)
    root.geometry(f"500x300+{posR}+{posD}")
    root.title('Help + Options')
    title = Label(root, text ="\nWallpaper Help",
                  font=("Arial", 19, "underline")).pack()
    help_text = Label(root, text='Commands:\nRight Alt: Change Wallpaper\nHome Key: Toggle the ability to change wallpaper\nF12: Reset wallpaper\nEsc: Reset wallpaper and exit\n',
                      font=("Arial", 15)).pack()
    confBtn = btn = Button(root, text = 'Config', command = lambda:[conf(), root.destroy()]).pack()
    root.mainloop()
    #root.withdraw()
    #msg.showinfo("Wallpaper Help","Commands:\nRight Alt: Change Wallpaper\nHome Key: Toggle the ability to change wallpaper\nF12: Reset wallpaper\nEsc: Reset wallpaper and exit")

def on_press(key):
    print(key)
    #only check valid keys
    if key != Key.alt_r and key != KeyCode.from_char('/') and key != Key.home and key != Key.esc and key != Key.end:
        return

    global state

    #check if wallpaper can be changed
    if state:
        rnd = reddit.subreddit(SUB).random()
        #set to random wallpaper off reddit
        if key == Key.alt_r:
            is_pic = False
            while not is_pic:
                if rnd.url[-4:] == ".jpg" or rnd.url[-4:] == ".png" or rnd.url[-5:] == ".jpeg":
                    is_pic = True
                    os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri " + rnd.url)
                    #uncomment this line if you want to view the whole image
                    #os.system("gsettings set org.gnome.desktop.background picture-options \"scaled\"")
                else:
                    #get random image and retry
                    rnd = reddit.subreddit(SUB).random()
        if key == KeyCode.from_char('/'):
            info()

    #toggle state
    if key == Key.home:
        if state:
            state = False
        else:
            state = True
    #set wallpaper to default
    if key == Key.f12:
        os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri /usr/share/backgrounds/warty-final-ubuntu.png")
        os.system("gsettings set org.gnome.desktop.background picture-options \"zoom\"")
    #exit program and change to default
    if key == Key.esc:
        os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri /usr/share/backgrounds/warty-final-ubuntu.png")
        os.system("gsettings set org.gnome.desktop.background picture-options \"zoom\"")
        exit(0)
    #exit program without changing wallpaper
    if key == Key.end:
        exit(0)

with Listener(on_press=on_press) as listen:
    listen.join()
#!/usr/bin/python3
from pynput.keyboard import Key, Listener, KeyCode
import os
import praw
import tkinter
from tkinter import messagebox as msg
#put your information into variable
reddit = praw.Reddit(
     client_id="your client id",
     client_secret="your client secret",
     user_agent="script desc"
)
state = True
def on_press(key):
    global state
    #check if wallpaper can be changed
    if state:
        rnd = reddit.subreddit('earthporn').random()
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
                    rnd = reddit.subreddit('earthporn').random()
        if key == KeyCode.from_char('/'):
            root = tkinter.Tk()
            root.withdraw()
            msg.showinfo("Wallpaper Help", "Commands:\nRight Alt: Change Wallpaper\nHome Key: Toggle the ability to change wallpaper\nF12: Reset wallpaper\nEsc: Reset wallpaper and exit")
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

with Listener(on_press=on_press) as listen:
    listen.join()